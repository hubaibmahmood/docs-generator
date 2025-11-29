"""Markdown module for rendering and file writing."""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def write_markdown_to_file(file_path: Path, content: str) -> None:
    """Writes a Markdown string to a specified file, creating directories if necessary."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        logger.info(f"Successfully wrote Markdown to {file_path}")
    except Exception as e:
        logger.error(f"Error writing Markdown to {file_path}: {e}")
        raise
