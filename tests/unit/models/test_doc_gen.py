import pytest
from src.models.doc_gen import (
    DocumentJob,
    GeneratedDocumentation,
    ProcessingResult,
    BatchGenerationResult,
)
from src.models.analysis import FileAnalysis, CodeAnalysisResult


def test_document_job_instantiation():
    """Test DocumentJob can be instantiated."""
    file_analysis_mock = FileAnalysis(
        file_path="test_file.py",
        file_type="python",
        language="python",
        elements=[],
        dependencies=[],
    )
    code_analysis_result_mock = CodeAnalysisResult(
        file_tree={}, file_analysis={"test_file.py": file_analysis_mock}
    )

    job = DocumentJob(
        file_path="test_file.py",
        content="def hello(): pass",
        context={"project_name": "test"},
        analysis=code_analysis_result_mock,
    )
    assert job.file_path == "test_file.py"
    assert job.content == "def hello(): pass"
    assert job.context == {"project_name": "test"}
    assert isinstance(job.analysis, CodeAnalysisResult)


def test_generated_documentation_instantiation():
    """Test GeneratedDocumentation can be instantiated."""
    doc = GeneratedDocumentation(
        summary="Summary of the file.",
        api_reference="API details.",
        examples="Code examples.",
    )
    assert doc.summary == "Summary of the file."
    assert doc.api_reference == "API details."
    assert doc.examples == "Code examples."


def test_processing_result_instantiation():
    """Test ProcessingResult can be instantiated."""
    result = ProcessingResult(
        file_path="test_file.py", doc_path="docs/test_file.md", status="success"
    )
    assert result.file_path == "test_file.py"
    assert result.doc_path == "docs/test_file.md"
    assert result.status == "success"
    assert result.error is None

    failed_result = ProcessingResult(
        file_path="fail_file.py",
        doc_path="docs/fail_file.md",
        status="failed",
        error="Parsing error",
    )
    assert failed_result.status == "failed"
    assert failed_result.error == "Parsing error"


def test_batch_generation_result_instantiation():
    """Test BatchGenerationResult can be instantiated."""
    result1 = ProcessingResult(
        file_path="file1.py", doc_path="docs/file1.md", status="success"
    )
    result2 = ProcessingResult(
        file_path="file2.py", doc_path="docs/file2.md", status="skipped"
    )

    batch_result = BatchGenerationResult(
        total_files=2, processed=1, skipped=1, failed=0, results=[result1, result2]
    )
    assert batch_result.total_files == 2
    assert batch_result.processed == 1
    assert batch_result.skipped == 1
    assert batch_result.failed == 0
    assert len(batch_result.results) == 2
    assert isinstance(batch_result.results[0], ProcessingResult)
