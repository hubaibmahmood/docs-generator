import logging
from pathlib import Path

from src.document_generator.agent import generate_section
from src.document_generator.markdown import write_markdown_to_file
from src.document_generator.strategies import get_all_strategies, DocumentationStrategy
from src.document_generator.validator import validate_analysis_result
from src.models.analysis import CodeAnalysisResult
from src.models.doc_gen import BatchGenerationResult, DocSectionJob, ProcessingResult

logger = logging.getLogger(__name__)


async def process_section(
    strategy: DocumentationStrategy,
    analysis_result: CodeAnalysisResult,
    output_dir: Path = Path("generated-docs"),
    write_to_disk: bool = True,
) -> ProcessingResult:
    """
    Processes a single documentation section: gathers context, calls agent, saves result.
    """
    try:
        # 1. Gather Context
        context_content = strategy.gather_context(analysis_result)
        if not context_content:
            logger.info(f"Skipping section {strategy.section_name}: No context found.")
            return ProcessingResult(
                section_name=strategy.section_name,
                output_path="",
                status="skipped",
                error="No context found (e.g., no API routes)",
            )

        # 2. Create Job
        prompt_instruction = strategy.get_prompt(context_content)
        job = DocSectionJob(
            section_name=strategy.section_name,
            output_filename=strategy.output_filename,
            context_content=context_content,
            prompt_instruction=prompt_instruction,
        )

        # 3. Generate Content
        generated_section = await generate_section(job)
        content = generated_section.content

        # 4. Save to Disk
        doc_path_str = ""
        if write_to_disk:
            doc_path = output_dir / strategy.output_filename
            write_markdown_to_file(doc_path, content)
            logger.info(f"Successfully generated {strategy.section_name} to {doc_path}")
            doc_path_str = str(doc_path)

        return ProcessingResult(
            section_name=strategy.section_name,
            output_path=doc_path_str,
            status="success",
            markdown_content=content,
        )

    except Exception as e:
        logger.error(f"Error processing section {strategy.section_name}: {e}")
        return ProcessingResult(
            section_name=strategy.section_name,
            output_path="",
            status="failed",
            error=str(e),
        )


class DocumentGeneratorEngine:
    """Orchestrator for the cohesive document generation process."""

    async def generate_documentation(
        self,
        analysis_result: CodeAnalysisResult,
        base_dir: Path = Path("."),
        output_dir: Path = Path("generated-docs"),
        write_to_disk: bool = True,
    ) -> BatchGenerationResult:
        """Main entry point: accepts analysis, processes strategies, returns batch result."""
        
        if not validate_analysis_result(analysis_result):
             logger.warning("Invalid analysis result received. Skipping documentation generation.")
             return BatchGenerationResult(
                total_sections=0, processed=0, skipped=0, failed=0, results=[]
            )

        strategies = get_all_strategies()
        total_sections = len(strategies)
        results: list[ProcessingResult] = []

        logger.info(f"Starting cohesive documentation generation for {total_sections} sections.")

        for strategy in strategies:
            result = await process_section(
                strategy, analysis_result, output_dir=output_dir, write_to_disk=write_to_disk
            )
            results.append(result)

        processed = sum(1 for r in results if r.status == "success")
        skipped = sum(1 for r in results if r.status == "skipped")
        failed = sum(1 for r in results if r.status == "failed")

        return BatchGenerationResult(
            total_sections=total_sections,
            processed=processed,
            skipped=skipped,
            failed=failed,
            results=results,
            source_analysis=analysis_result
        )
