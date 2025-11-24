import pytest
from src.models.doc_gen import (
    DocSectionJob, # New
    GeneratedSection, # New
    ProcessingResult,
    BatchGenerationResult,
)
from src.models.analysis import FileAnalysis, CodeAnalysisResult


def test_doc_section_job_instantiation():
    """Test DocSectionJob can be instantiated."""
    job = DocSectionJob(
        section_name="Project Overview",
        output_filename="README.md",
        context_content="File tree: ...",
        prompt_instruction="Generate a project overview."
    )
    assert job.section_name == "Project Overview"
    assert job.output_filename == "README.md"
    assert job.context_content == "File tree: ..."
    assert job.prompt_instruction == "Generate a project overview."

def test_generated_section_instantiation():
    """Test GeneratedSection can be instantiated."""
    section = GeneratedSection(content="## My Section")
    assert section.content == "## My Section"
    assert section.title is None

def test_processing_result_instantiation():
    """Test ProcessingResult can be instantiated."""
    result = ProcessingResult(
        section_name="Project Overview", output_path="docs/README.md", status="success"
    )
    assert result.section_name == "Project Overview"
    assert result.output_path == "docs/README.md"
    assert result.status == "success"
    assert result.error is None

    failed_result = ProcessingResult(
        section_name="API Reference",
        output_path="docs/api.md",
        status="failed",
        error="API parsing error",
    )
    assert failed_result.status == "failed"
    assert failed_result.error == "API parsing error"


def test_batch_generation_result_instantiation():
    """Test BatchGenerationResult can be instantiated."""
    source_analysis_mock = CodeAnalysisResult(file_tree={}, file_analysis={})
    result1 = ProcessingResult(
        section_name="Project Overview", output_path="docs/README.md", status="success"
    )
    result2 = ProcessingResult(
        section_name="API Reference", output_path="docs/api.md", status="skipped"
    )

    batch_result = BatchGenerationResult(
        total_sections=2,
        processed=1,
        skipped=1,
        failed=0,
        results=[result1, result2],
        source_analysis=source_analysis_mock
    )
    assert batch_result.total_sections == 2
    assert batch_result.processed == 1
    assert batch_result.skipped == 1
    assert batch_result.failed == 0
    assert len(batch_result.results) == 2
    assert isinstance(batch_result.results[0], ProcessingResult)
    assert batch_result.source_analysis == source_analysis_mock
