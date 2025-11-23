import logging  # Added import
from pathlib import Path

from src.document_generator.agent import generate_documentation_from_job
from src.document_generator.markdown import render_to_markdown, write_markdown_to_file
from src.document_generator.validator import validate_analysis_result
from src.models.analysis import CodeAnalysisResult
from src.models.doc_gen import BatchGenerationResult, DocumentJob, ProcessingResult

logger = logging.getLogger(__name__) # Added logger initialization


async def process_file(
    file_path: str,
    analysis_result: CodeAnalysisResult,
    base_dir: Path = Path("."),
    output_dir: Path = Path("docs"),
    write_to_disk: bool = True,
) -> ProcessingResult:
    """
    Processes a single file: reads content, calls agent, saves documentation.

    Includes trivial file detection.
    """
    try:
        # Check if file exists relative to base_dir
        path = base_dir / file_path
        if not path.exists():
            logger.warning(f"File not found: {path}") # Added logging
            return ProcessingResult(
                file_path=file_path,
                doc_path="",
                status="failed",
                error=f"File not found: {file_path}",
            )

        # Read content
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Error reading file {path}: {e}") # Added logging
            return ProcessingResult(
                file_path=file_path,
                doc_path="",
                status="failed",
                error=f"Error reading file: {e}",
            )

        # Trivial file detection (T030, T031)
        file_analysis = analysis_result.file_analysis.get(file_path)
        # Heuristic: no elements extracted AND very small content (e.g., just imports or comments)
        if file_analysis and not file_analysis.elements and len(content.strip()) < 50:
            logger.info(f"Skipping trivial file: {file_path}")
            return ProcessingResult(
                file_path=file_path,
                doc_path="",
                status="skipped",
                error="File considered trivial (no elements and small content)",
            )

        # Create Job
        job = DocumentJob(
            file_path=file_path,
            content=content,
            context={"project_name": "Unknown"}, # Placeholder context
            analysis=analysis_result,
        )

        # Generate Documentation
        generated_doc = await generate_documentation_from_job(job)

        # Render and Save
        markdown_content = render_to_markdown(generated_doc)
        
        doc_path_str = ""
        if write_to_disk:
            # Determine output path
            doc_path = output_dir / file_path
            # Change extension to .md
            doc_path = doc_path.with_suffix(".md")

            write_markdown_to_file(doc_path, markdown_content)
            logger.info(f"Successfully generated documentation for {file_path} to {doc_path}") # Added logging
            doc_path_str = str(doc_path)

        return ProcessingResult(
            file_path=file_path,
            doc_path=doc_path_str,
            status="success",
            markdown_content=markdown_content,
        )

    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return ProcessingResult(
            file_path=file_path,
            doc_path="",
            status="failed",
            error=str(e),
        )


class DocumentGeneratorEngine:
    """Orchestrator for the document generation process."""

    async def generate_documentation(
        self,
        analysis_result: CodeAnalysisResult,
        base_dir: Path = Path("."),
        output_dir: Path = Path("docs"),
        write_to_disk: bool = True,
    ) -> BatchGenerationResult:
        """Main entry point: accepts analysis, processes files, returns batch result."""
        if not validate_analysis_result(analysis_result):
             logger.warning("Invalid analysis result received. Skipping documentation generation.") # Added logging
             return BatchGenerationResult(
                total_files=0, processed=0, skipped=0, failed=0, results=[]
            )

        files_to_process = list(analysis_result.file_analysis.keys())
        total_files = len(files_to_process)
        results: list[ProcessingResult] = []

        # Process sequentially for now (can be parallelized later)
        for file_path in files_to_process:
            result = await process_file(
                file_path, analysis_result, base_dir=base_dir, output_dir=output_dir, write_to_disk=write_to_disk
            )
            results.append(result)

        processed = sum(1 for r in results if r.status == "success")
        skipped = sum(1 for r in results if r.status == "skipped")
        failed = sum(1 for r in results if r.status == "failed")

        return BatchGenerationResult(
            total_files=total_files,
            processed=processed,
            skipped=skipped,
            failed=failed,
            results=results,
        )