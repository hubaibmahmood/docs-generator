"""Markdown module for rendering and file writing."""

import logging  # Added import
from pathlib import Path

from src.models.doc_gen import GeneratedDocumentation

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)  # Added logger initialization


def render_to_markdown(doc: GeneratedDocumentation) -> str:
    """Renders a GeneratedDocumentation object into a Markdown string."""
    logger.info("Rendering GeneratedDocumentation to Markdown.")
    summary_content = doc.summary.replace(r'\n', '\n')
    api_reference_content = doc.api_reference.replace(r'\n', '\n')
    examples_content = doc.examples.replace(r'\n', '\n')

    markdown_string = f"# Summary\n\n{summary_content}\n\n"
    if api_reference_content:
        markdown_string += f"# API Reference\n\n{api_reference_content}\n\n"
    if examples_content:
        markdown_string += f"# Examples\n\n{examples_content}\n\n"
    return markdown_string


def write_markdown_to_file(file_path: Path, content: str) -> None:
    """Writes a Markdown string to a specified file, creating directories if necessary."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        logger.info(f"Successfully wrote Markdown to {file_path}")
    except Exception as e:
        logger.error(f"Error writing Markdown to {file_path}: {e}")
        raise
