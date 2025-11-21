from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
import uuid
from typing import Dict, Any
import logging

from src.analysis.orchestrator import AnalysisOrchestrator
from src.models.analysis import CodeAnalysisResult, AnalysisError
import tempfile
import asyncio
import shutil # Import shutil for rmtree

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory store for task status and results (for simplicity, replace with a proper DB/cache in production)
repo_analysis_tasks: Dict[str, Dict[str, Any]] = {}

class RepositoryAnalysisRequest(BaseModel):
    url: str

@router.post("/analyze", status_code=status.HTTP_202_ACCEPTED)
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
    
    repo_analysis_tasks[task_id] = {
        "status": "PENDING",
        "result": None,
        "errors": [],
        "repo_url": request.url
    }

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
            logger.warning(f"Task {task_id}: Analysis completed with errors. Errors: {[err.error for err in analysis_result.errors]}")
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
            shutil.rmtree(temp_dir)
            logger.info(f"Task {task_id}: Cleaned up temporary directory: {temp_dir}")

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
