import fnmatch
import logging
import os
import re
from typing import Any

from src.analysis.parsing.factory import ParserFactory
from src.analysis.repository import clone_repository  # This will be unused in analyze_local_path
from src.common.constants import DEFAULT_EXCLUSION_PATTERNS
from src.common.exceptions import ParsingError, RepositoryError
from src.models.analysis import AnalysisError, CodeAnalysisResult, FileAnalysis

logger = logging.getLogger(__name__)

class AnalysisOrchestrator:
    """
    Orchestrates the code analysis process by coordinating repository cloning and file parsing.
    """
    def __init__(self):
        """
        Initializes the orchestrator. Parsers are registered in the factory.
        """
        pass # Parsers are registered in factory.py

    def _perform_analysis(self, base_path: str, repo_name: str) -> CodeAnalysisResult:
        """Internal method to perform the actual file walking and parsing."""
        analysis_result = CodeAnalysisResult()
        file_analysis_map = {}
        file_tree_dict: dict[str, Any] = {"name": repo_name, "path": "/", "children": []}

        # Determine exclusion patterns
        exclusion_patterns = list(DEFAULT_EXCLUSION_PATTERNS)
        has_specify = os.path.isdir(os.path.join(base_path, ".specify"))
        has_gemini = os.path.isdir(os.path.join(base_path, ".gemini"))

        if has_specify and has_gemini:
            logger.info("Detected Spec-Driven project structure (.specify and .gemini found). Excluding 'specs' and 'history' directories.")
            exclusion_patterns.extend(["specs", "history"])

        for root, dirs, files in os.walk(base_path):
            # Filter directories in-place to prevent os.walk from traversing them
            # Also filter out symlinks to directories to prevent traversal
            dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in exclusion_patterns)
                       and not os.path.islink(os.path.join(root, d))]

            # Filter files to ignore them
            files = [f for f in files if not any(fnmatch.fnmatch(f, pattern) for pattern in exclusion_patterns)]

            relative_root = os.path.relpath(root, base_path)
            current_level_in_tree = file_tree_dict

            # Navigate or create the correct level in the file_tree_dict
            if relative_root != ".":
                path_parts = relative_root.split(os.sep)
                for part in path_parts:
                    found = False
                    for child in current_level_in_tree["children"]:
                        if child["name"] == part and child["type"] == "dir":
                            current_level_in_tree = child
                            found = True
                            break
                    if not found:
                        new_dir = {"name": part, "path": os.path.join(current_level_in_tree["path"], part), "type": "dir", "children": []}
                        current_level_in_tree["children"].append(new_dir)
                        current_level_in_tree = new_dir

            for dir_name in dirs:
                # Double check it's not a link (though dirs[:] filter handles traversal, we also want to exclude from tree)
                if os.path.islink(os.path.join(root, dir_name)):
                     logger.warning(f"Skipping symlink directory: {os.path.join(root, dir_name)}")
                     continue

                current_level_in_tree["children"].append({
                    "name": dir_name,
                    "path": os.path.join(current_level_in_tree["path"], dir_name),
                    "type": "dir",
                    "children": []
                })

            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Skip file symlinks
                if os.path.islink(file_path):
                    logger.warning(f"Skipping symlink file: {file_path}")
                    continue

                relative_file_path = os.path.relpath(file_path, base_path)

                parser = ParserFactory.get_parser(file_path)
                is_binary = False
                content: str | None = None

                # Read file content if it's not likely binary (simple check)
                if not is_binary:
                    try:
                        # Check file size first (skip if > 1MB)
                        if os.path.getsize(file_path) < 1 * 1024 * 1024:
                            with open(file_path, encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                    except Exception:
                        # If reading fails (e.g. binary file not detected earlier), ignore content
                        pass

                if parser:
                    logger.debug(f"Parsing file: {relative_file_path} with {type(parser).__name__}")
                    try:
                        file_analysis = parser.parse(file_path)
                        file_analysis.file_path = relative_file_path # Use relative path in the analysis object
                        file_analysis.content = content
                        file_analysis_map[relative_file_path] = file_analysis
                        if file_analysis.errors:
                            logger.warning(f"File {relative_file_path} parsed with errors: {[err.error for err in file_analysis.errors]}")
                            analysis_result.errors.extend(file_analysis.errors)
                    except ParsingError as e:
                        logger.error(f"ParsingError for file {relative_file_path}: {e}")
                        analysis_result.errors.append(AnalysisError(file_path=relative_file_path, error=f"Parsing error: {e}"))
                    except Exception as e:
                        logger.exception(f"Unexpected error while parsing file {relative_file_path}")
                        analysis_result.errors.append(AnalysisError(file_path=relative_file_path, error=f"Unexpected parsing error: {e}"))
                else:
                    is_binary = True
                    # Even if no parser, we might have read content if it was small and text-like
                    # But usually 'is_binary=True' means we treat it as binary.
                    # However, 'ParserFactory.get_parser' returning None doesn't guarantee it's binary, just unknown extension.
                    # Let's check if we successfully read content.
                    final_is_binary = is_binary if content is None else False

                    logger.info(f"No parser found for file: {relative_file_path}. Treating as binary={final_is_binary}.")
                    file_analysis_map[relative_file_path] = FileAnalysis(
                        file_path=relative_file_path,
                        file_type="Binary" if final_is_binary else "Unknown",
                        language="N/A",
                        elements=[],
                        dependencies=[],
                        is_binary=final_is_binary,
                        content=content,
                        errors=[AnalysisError(file_path=relative_file_path, error="No suitable parser found.")]
                    )

                current_level_in_tree["children"].append({
                    "name": file_name,
                    "path": os.path.join(relative_root, file_name) if relative_root != "." else file_name,
                    "type": "file",
                    "is_binary": is_binary
                })

        analysis_result.file_analysis = file_analysis_map
        analysis_result.file_tree = file_tree_dict
        return analysis_result

    def analyze_repository(self, repo_url: str, output_dir: str) -> CodeAnalysisResult:
        """
        Analyzes a git repository given its URL.

        Args:
            repo_url (str): The URL of the git repository to analyze.
            output_dir (str): The local directory where the repository should be cloned.

        Returns:
            CodeAnalysisResult: The result of the analysis, including file tree and extracted elements.
        """
        logger.info(f"Starting analysis for repository: {repo_url}")
        analysis_result = CodeAnalysisResult()

        try:
            logger.info(f"Cloning repository {repo_url} to {output_dir}")
            repo = clone_repository(repo_url, output_dir)
            cloned_repo_actual_path = repo.working_dir
            logger.info(f"Repository cloned to: {cloned_repo_actual_path}")

            # Extract repository name from URL for a more meaningful file_tree root
            match = re.search(r'/([^/]+?)(?:\.git)?$', repo_url)
            repo_name = match.group(1) if match else os.path.basename(cloned_repo_actual_path)

            analysis_result = self._perform_analysis(cloned_repo_actual_path, repo_name)
            logger.info(f"Finished analysis for repository: {repo_url}")

        except RepositoryError as e:
            logger.error(f"RepositoryError during analysis of {repo_url}: {e}")
            analysis_result.errors.append(AnalysisError(file_path=repo_url, error=f"Repository error: {e}"))
        except Exception as e:
            logger.exception(f"An unexpected error occurred during orchestration for {repo_url}")
            analysis_result.errors.append(AnalysisError(file_path=repo_url, error=f"An unexpected error occurred during orchestration: {e}"))

        return analysis_result

    def analyze_local_path(self, local_path: str) -> CodeAnalysisResult:
        """
        Analyzes a local directory directly, without attempting to clone.

        Args:
            local_path (str): The path to the local directory to analyze.

        Returns:
            CodeAnalysisResult: The result of the analysis.
        """
        logger.info(f"Starting analysis for local path: {local_path}")
        repo_name = os.path.basename(local_path)
        analysis_result = self._perform_analysis(local_path, repo_name)
        logger.info(f"Finished analysis for local path: {local_path}")
        return analysis_result
