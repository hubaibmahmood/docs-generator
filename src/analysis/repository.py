import os
import shutil
import git
import logging
import re
import socket
import ipaddress
from urllib.parse import urlparse

from src.common.exceptions import RepositoryError

logger = logging.getLogger(__name__)

def _validate_repo_url(repo_url: str) -> str:
    """
    Validates the repository URL to prevent command injection, SSRF, and ensure it's a valid Git URL.
    Returns the normalized URL.
    """
    # 0. Length check
    if len(repo_url) > 2048:
        raise RepositoryError("Invalid repository URL. URL exceeds maximum length of 2048 characters.")

    # 1. Protocol check
    if not (repo_url.startswith("http://") or repo_url.startswith("https://") or 
            repo_url.startswith("git@") or repo_url.startswith("ssh://")):
        raise RepositoryError(f"Invalid repository URL protocol. Must be http, https, ssh, or git@. URL: {repo_url}")

    # 2. Command injection check (prevent flags)
    if repo_url.startswith("-") or "--" in repo_url:
        raise RepositoryError(f"Invalid repository URL. Contains potential command injection patterns. URL: {repo_url}")

    # 3. Character whitelist check (Extended)
    # Block control characters strictly
    if re.search(r"[\x00-\x1f\x7f]", repo_url):
        raise RepositoryError("Invalid repository URL. Contains control characters.")
    
    if not re.match(r"^[a-zA-Z0-9\-_\.\/\:@]+$", repo_url):
        raise RepositoryError(f"Invalid repository URL. Contains illegal characters. URL: {repo_url}")

    # 4. Path traversal check
    if re.search(r"(?:^|/)\.\.(?:/|$)", repo_url):
        raise RepositoryError(f"Invalid repository URL. Path traversal detected. URL: {repo_url}")

    # 5. Credential check (Prevent user:pass@)
    if "@" in repo_url:
        # Allow git@github.com (SSH style)
        if not (repo_url.startswith("git@") or repo_url.startswith("ssh://git@")):
             # For http/https, @ implies auth. 
             # Regex to check if it's http(s)://user:pass@host or http(s)://user@host
             if re.search(r"^https?://[^/]+@", repo_url):
                 raise RepositoryError("Invalid repository URL. Embedded credentials are not allowed for security reasons.")

    # 6. Normalization (Handle double slashes)
    # Remove double slashes in path, but preserve protocol slashes (//)
    # Split protocol
    parts = repo_url.split("://", 1)
    if len(parts) == 2:
        protocol, rest = parts
        # Replace multiple slashes with single slash in 'rest'
        normalized_rest = re.sub(r"/{2,}", "/", rest)
        normalized_url = f"{protocol}://{normalized_rest}"
    else:
        # For git@ or ssh without :// (though ssh usually has it)
        normalized_url = re.sub(r"/{2,}", "/", repo_url)
    
    # 7. SSRF Prevention: Resolve hostname and check for private/reserved IPs
    try:
        parsed = urlparse(normalized_url)
        hostname = parsed.hostname
        
        if not hostname:
             # Fallback for git@ or ssh:// formats if urlparse fails to get hostname cleanly
             if "@" in normalized_url and ":" in normalized_url:
                 hostname = normalized_url.split("@")[1].split(":")[0]
             else:
                 pass

        if hostname:
            try:
                ip_str = socket.gethostbyname(hostname)
                ip = ipaddress.ip_address(ip_str)
                
                if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
                    raise RepositoryError(f"Blocked access to private/local network address: {hostname} ({ip_str})")
                    
            except socket.gaierror:
                pass
                
    except ValueError as e:
        raise RepositoryError(f"Invalid IP address format derived from hostname: {e}")
    except Exception as e:
        if isinstance(e, RepositoryError):
            raise e
        logger.warning(f"SSRF check warning during hostname parsing: {e}")
        
    return normalized_url

def _sanitize_git_error(error_msg: str) -> str:
    """
    Removes sensitive local path information from Git error messages.
    """
    # Remove "Cloning into '...'"
    sanitized = re.sub(r"Cloning into '[^']+'\.\.\.\s*", "", error_msg)
    # Remove other potential absolute paths (Unix-style)
    sanitized = re.sub(r"(?<!\w)/[a-zA-Z0-9_\-\.]+(?:/[a-zA-Z0-9_\-\.]+)+", "[REDACTED_PATH]", sanitized)
    return sanitized

def clone_repository(repo_url: str, destination: str) -> git.Repo:
    """
    Clones a Git repository from a URL to a destination.
    Raises RepositoryError on failure.
    """
    normalized_url = _validate_repo_url(repo_url)

    logger.info(f"Attempting to clone repository {normalized_url} to {destination}")
    try:
        repo = git.Repo.clone_from(normalized_url, destination)
        logger.info(f"Successfully cloned {normalized_url} to {destination}")
        return repo
    except git.exc.GitCommandError as e:
        error_output = e.stderr.strip()
        logger.error(f"GitCommandError while cloning {normalized_url}: {error_output}")
        
        sanitized_error = _sanitize_git_error(error_output)
        
        if os.path.exists(destination):
            shutil.rmtree(destination)
            logger.info(f"Cleaned up partial clone directory: {destination}")
        raise RepositoryError(f"Failed to clone repository: {sanitized_error}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred while cloning {normalized_url}")
        if os.path.exists(destination):
            shutil.rmtree(destination)
            logger.info(f"Cleaned up partial clone directory due to unexpected error: {destination}")
        raise RepositoryError(f"An unexpected error occurred while cloning {normalized_url}: {e}")