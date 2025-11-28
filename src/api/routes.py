import asyncio
import logging
import shutil  # Import shutil for rmtree
import tempfile
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.analysis.orchestrator import AnalysisOrchestrator
from src.document_generator.engine import DocumentGeneratorEngine
from src.models.analysis import AnalysisError, CodeAnalysisResult
from src.models.doc_gen import BatchGenerationResult

# Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory store for task status and results (for simplicity, replace with a proper DB/cache in production)
repo_analysis_tasks: dict[str, dict[str, Any]] = {}


class RepositoryAnalysisRequest(BaseModel):
    """Request model for repository analysis."""

    url: str


# @router.post("/analyze", status_code=status.HTTP_202_ACCEPTED)
async def analyze_repository(request: RepositoryAnalysisRequest):
    """
    Initiates the analysis of a repository in the background.

    Args:
        request (RepositoryAnalysisRequest): The request object containing the repository URL.

    Returns:
        dict: A dictionary containing the task ID for the analysis job.
    """
    task_id = str(uuid.uuid4())
    logger.info(f"Received analysis request for URL: {request.url}. Assigning task ID: {task_id}")

    repo_analysis_tasks[task_id] = {"status": "PENDING", "result": None, "errors": [], "repo_url": request.url}

    asyncio.create_task(run_analysis_in_background(task_id, request.url))

    return {"task_id": task_id}


async def run_analysis_in_background(task_id: str, repo_url: str):
    """
    Runs the repository analysis in a background task.

    Args:
        task_id (str): The ID of the task.
        repo_url (str): The URL of the repository to analyze.
    """
    orchestrator = AnalysisOrchestrator()
    temp_dir = None
    try:
        logger.info(f"Task {task_id}: Changing status to IN_PROGRESS.")
        repo_analysis_tasks[task_id]["status"] = "IN_PROGRESS"

        temp_dir = tempfile.mkdtemp()
        logger.info(f"Task {task_id}: Cloned repository to temporary directory: {temp_dir}")

        analysis_result: CodeAnalysisResult = orchestrator.analyze_repository(repo_url, temp_dir)

        if analysis_result.errors:
            logger.warning(f"Task {task_id}: Analysis completed with errors. Errors: {analysis_result.errors}")
            repo_analysis_tasks[task_id]["status"] = "FAILED"
            repo_analysis_tasks[task_id]["errors"] = [err.model_dump() for err in analysis_result.errors]
        else:
            logger.info(f"Task {task_id}: Analysis completed successfully.")
            repo_analysis_tasks[task_id]["status"] = "SUCCESS"
            repo_analysis_tasks[task_id]["result"] = analysis_result.model_dump()

    except Exception as e:
        logger.exception(f"Task {task_id}: An unexpected error occurred during background analysis for {repo_url}.")
        repo_analysis_tasks[task_id]["status"] = "FAILED"
        repo_analysis_tasks[task_id]["errors"].append(AnalysisError(file_path=repo_url, error=str(e)).model_dump())
    finally:
        if temp_dir:
            try:
                shutil.rmtree(temp_dir)
                logger.info(f"Task {task_id}: Cleaned up temporary directory: {temp_dir}")
            except FileNotFoundError:
                pass
            except Exception as e:
                logger.warning(f"Task {task_id}: Failed to clean up temp dir {temp_dir}: {e}")


@router.get("/status/{task_id}")
async def get_analysis_status(task_id: str):
    """
    Retrieves the status of an analysis task.

    Args:
        task_id (str): The ID of the task to check.

    Returns:
        dict: A dictionary containing the task status and any errors.

    Raises:
        HTTPException: If the task ID is not found.
    """
    logger.info(f"Received status request for task ID: {task_id}")
    task = repo_analysis_tasks.get(task_id)
    if not task:
        logger.warning(f"Status request for unknown task ID: {task_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task ID not found")
    return {"task_id": task_id, "status": task["status"], "errors": task["errors"]}


@router.get("/result/{task_id}")
async def get_analysis_result(task_id: str):
    """
    Retrieves the result of a completed analysis task.

    Args:
        task_id (str): The ID of the completed task.

    Returns:
        dict: The analysis result.

    Raises:
        HTTPException: If the task ID is not found or the task is not complete.
    """
    logger.info(f"Received result request for task ID: {task_id}")
    task = repo_analysis_tasks.get(task_id)
    if not task:
        logger.warning(f"Result request for unknown task ID: {task_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task ID not found")
    if task["status"] != "SUCCESS":
        logger.info(f"Result request for task ID {task_id} failed: status is {task['status']}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not yet complete or failed")
    return task["result"]


# @router.post("/generate", response_model=BatchGenerationResult)
async def generate_docs(analysis_result: CodeAnalysisResult):
    """Generates documentation based on code analysis results."""
    engine = DocumentGeneratorEngine()
    return await engine.generate_documentation(analysis_result)


@router.post("/process", status_code=status.HTTP_202_ACCEPTED)
async def process_repository(request: RepositoryAnalysisRequest):
    """
    Initiates the full processing pipeline (analysis + generation) for a repository.

    Args:
        request (RepositoryAnalysisRequest): The request object containing the repository URL.

    Returns:
        dict: A dictionary containing the task ID for the processing job.
    """
    task_id = str(uuid.uuid4())
    logger.info(f"Received process request for URL: {request.url}. Assigning task ID: {task_id}")

    repo_analysis_tasks[task_id] = {
        "status": "PENDING",
        "result": None,  # Will hold BatchGenerationResult
        "errors": [],
        "repo_url": request.url,
        "output_dir": None,
    }

    asyncio.create_task(run_processing_in_background(task_id, request.url))

    return {"task_id": task_id}


async def run_processing_in_background(task_id: str, repo_url: str):
    """
    Runs the full repository processing pipeline in a background task.

    Clone -> Analyze -> Generate Docs -> Store Result -> Cleanup Input
    """
    orchestrator = AnalysisOrchestrator()
    engine = DocumentGeneratorEngine()
    temp_input_dir = None

    try:
        logger.info(f"Process Task {task_id}: Changing status to IN_PROGRESS.")
        repo_analysis_tasks[task_id]["status"] = "IN_PROGRESS"

        # 1. Setup Input
        temp_input_dir = tempfile.mkdtemp()
        logger.info(f"Process Task {task_id}: Cloned repository to temporary input directory: {temp_input_dir}")

        # 2. Analyze
        analysis_result: CodeAnalysisResult = orchestrator.analyze_repository(repo_url, temp_input_dir)

        if analysis_result.errors:
            logger.warning(f"Process Task {task_id}: Analysis had errors: {analysis_result.errors}")
            # We continue if there are partial results? Or fail?
            # CodeAnalysisResult usually returns whatever it found.
            # If no file analysis, we fail.
            if not analysis_result.file_analysis:
                repo_analysis_tasks[task_id]["status"] = "FAILED"
                repo_analysis_tasks[task_id]["errors"] = [err.model_dump() for err in analysis_result.errors]
                return

        # 3. Generate Docs
        logger.info(f"Process Task {task_id}: Starting documentation generation.")
        batch_result: BatchGenerationResult = await engine.generate_documentation(
            analysis_result,
            base_dir=Path(temp_input_dir),
            output_dir=Path("generated-docs"),
            write_to_disk=True,
        )

        logger.info(
            f"Process Task {task_id}: Generation complete. "
            f"Processed: {batch_result.processed}, Failed: {batch_result.failed}"
        )

        repo_analysis_tasks[task_id]["status"] = "SUCCESS"
        repo_analysis_tasks[task_id]["result"] = batch_result.model_dump()

    except Exception as e:
        logger.exception(f"Process Task {task_id}: An unexpected error occurred during background processing.")
        repo_analysis_tasks[task_id]["status"] = "FAILED"
        repo_analysis_tasks[task_id]["errors"].append(AnalysisError(file_path=repo_url, error=str(e)).model_dump())
    finally:
        if temp_input_dir:
            try:
                shutil.rmtree(temp_input_dir)
                logger.info(f"Process Task {task_id}: Cleaned up temporary input directory: {temp_input_dir}")
            except FileNotFoundError:
                pass
            except Exception as e:
                logger.warning(f"Process Task {task_id}: Failed to clean up temp dir {temp_input_dir}: {e}")
