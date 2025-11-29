import asyncio
import logging
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.analysis.orchestrator import AnalysisOrchestrator
from src.api.auth import get_current_active_user
from src.common.security.encryption import decrypt_data, encrypt_data
from src.database import get_db
from src.document_generator.engine import DocumentGeneratorEngine
from src.models.analysis import AnalysisError, CodeAnalysisResult
from src.models.doc_gen import BatchGenerationResult, UserGeminiApiKey
from src.models.sql_user import User, UserApiKey

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory store for task status and results (for simplicity, replace with a proper DB/cache in production)
repo_analysis_tasks: dict[str, dict[str, Any]] = {}


class RepositoryAnalysisRequest(BaseModel):
    """Request model for repository analysis."""

    url: str


@router.post("/process", status_code=status.HTTP_202_ACCEPTED)
async def process_repository(
    request: RepositoryAnalysisRequest,
    db: Session = Depends(get_db),  # Inject DB session
    current_user: User = Depends(get_current_active_user),  # Inject current user
):
    """
    Initiates the full processing pipeline (analysis + generation) for a repository.

    Args:
        request (RepositoryAnalysisRequest): The request object containing the repository URL.
        db (Session): The database session.
        current_user (User): The authenticated user.

    Returns:
        dict: A dictionary containing the task ID for the processing job.
    """
    task_id = str(uuid.uuid4())
    logger.info(f"Received process request for URL: {request.url}. Assigning task ID: {task_id}")

    repo_analysis_tasks[task_id] = {
        "status": "PENDING",
        "result": None,
        "errors": [],
        "repo_url": request.url,
        "output_dir": None,
    }

    # Retrieve API key for the current user from the database
    stmt = select(UserApiKey).where(UserApiKey.user_id == current_user.id, UserApiKey.key_type == "gemini")
    user_api_key_entry = db.execute(stmt).scalars().first()

    dynamic_api_key = None
    if user_api_key_entry:
        try:
            dynamic_api_key = decrypt_data(user_api_key_entry.encrypted_api_key)
            logger.info(f"Process Task {task_id}: Using Gemini API key from database for user {current_user.id}.")
        except Exception as e:
            logger.error(f"Process Task {task_id}: Failed to decrypt API key for user {current_user.id}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to decrypt API key.")
    else:
        logger.warning(f"Process Task {task_id}: No Gemini API key found for user {current_user.id}.")
        # Raise an error if no API key is found, enforcing BYOK
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Gemini API Key not found. Please set it in your settings.",
        )

    asyncio.create_task(run_processing_in_background(task_id, request.url, api_key=dynamic_api_key))

    return {"task_id": task_id}


async def run_processing_in_background(task_id: str, repo_url: str, api_key: str | None = None):
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
            api_key=api_key,  # Pass the dynamically retrieved API key
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


# New endpoint for API key management
@router.post("/api/v1/settings/gemini-api-key", status_code=status.HTTP_200_OK)
async def set_user_gemini_api_key(
    user_api_key: UserGeminiApiKey,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Allows an authenticated user to set or update their Gemini API key.
    The key is encrypted before being stored in the database.
    """
    encrypted_key = encrypt_data(user_api_key.api_key)

    # Check if an entry already exists for this user and key type
    stmt = select(UserApiKey).where(UserApiKey.user_id == current_user.id, UserApiKey.key_type == "gemini")
    db_api_key = db.execute(stmt).scalars().first()

    if db_api_key:
        db_api_key.encrypted_api_key = encrypted_key
        logger.info(f"Updated Gemini API key for user {current_user.id}.")
    else:
        new_api_key_entry = UserApiKey(
            user_id=current_user.id,
            key_type="gemini",
            encrypted_api_key=encrypted_key,
        )
        db.add(new_api_key_entry)
        logger.info(f"Set new Gemini API key for user {current_user.id}.")

    db.commit()
    db.refresh(current_user)  # Refresh user object to include any new relationships if needed

    return {"message": "Gemini API key saved successfully."}


@router.get("/api/v1/settings/gemini-api-key-status", status_code=status.HTTP_200_OK)
async def get_user_gemini_api_key_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Checks if an authenticated user has a Gemini API key configured.
    """
    stmt = select(UserApiKey).where(UserApiKey.user_id == current_user.id, UserApiKey.key_type == "gemini")
    user_api_key_entry = db.execute(stmt).scalars().first()

    if user_api_key_entry:
        return {"configured": True}
    return {"configured": False}
