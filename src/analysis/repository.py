import os
import shutil
import git
import logging

from src.common.exceptions import RepositoryError

logger = logging.getLogger(__name__)

def clone_repository(repo_url: str, destination: str) -> git.Repo:
    """
    Clones a Git repository from a URL to a destination.
    Raises RepositoryError on failure.
    """
    logger.info(f"Attempting to clone repository {repo_url} to {destination}")
    try:
        repo = git.Repo.clone_from(repo_url, destination)
        logger.info(f"Successfully cloned {repo_url} to {destination}")
        return repo
    except git.exc.GitCommandError as e:
        logger.error(f"GitCommandError while cloning {repo_url}: {e.stderr.strip()}")
        if os.path.exists(destination):
            shutil.rmtree(destination)
            logger.info(f"Cleaned up partial clone directory: {destination}")
        raise RepositoryError(f"Failed to clone repository {repo_url}: {e.stderr.strip()}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred while cloning {repo_url}")
        if os.path.exists(destination):
            shutil.rmtree(destination)
            logger.info(f"Cleaned up partial clone directory due to unexpected error: {destination}")
        raise RepositoryError(f"An unexpected error occurred while cloning {repo_url}: {e}")