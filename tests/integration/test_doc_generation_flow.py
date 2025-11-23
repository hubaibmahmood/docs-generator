from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.document_generator.engine import DocumentGeneratorEngine, process_file
from src.models.analysis import CodeAnalysisResult, FileAnalysis
from src.models.doc_gen import GeneratedDocumentation, ProcessingResult


@pytest.fixture
def sample_analysis_result():
    file_analysis_mock = FileAnalysis(
        file_path="test_file.py",
        file_type="python",
        language="python",
        elements=[],
        dependencies=[],
    )
    return CodeAnalysisResult(
        file_tree={"test_file.py": {}},
        file_analysis={"test_file.py": file_analysis_mock},
        errors=[],
    )


@pytest.mark.asyncio
async def test_process_file_success(sample_analysis_result, tmp_path):
    """Test successful file processing."""
    # Create a dummy file
    test_file = tmp_path / "test_file.py"
    long_content = "def foo():\n    pass\n" + "# " * 50
    test_file.write_text(long_content)

    # Mock generate_documentation_from_job
    with patch("src.document_generator.engine.generate_documentation_from_job", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = GeneratedDocumentation(summary="Summary", api_reference="API", examples="Examples")

        # We also need to mock write_markdown_to_file
        with patch("src.document_generator.engine.write_markdown_to_file") as mock_write:
            result = await process_file(
                "test_file.py", 
                sample_analysis_result, 
                base_dir=tmp_path, 
                output_dir=tmp_path / "docs"
            )

            assert result.status == "success"
            assert result.file_path == "test_file.py"
            mock_gen.assert_called_once()
            mock_write.assert_called_once()


@pytest.mark.asyncio
async def test_engine_orchestration(sample_analysis_result):
    """Test the engine orchestrating the batch process."""
    engine = DocumentGeneratorEngine()

    with patch("src.document_generator.engine.process_file", new_callable=AsyncMock) as mock_process:
        mock_process.return_value = ProcessingResult(
            file_path="test_file.py", doc_path="docs/test_file.md", status="success"
        )

        batch_result = await engine.generate_documentation(sample_analysis_result)

        assert batch_result.total_files == 1
        assert batch_result.processed == 1
        assert batch_result.failed == 0
        # Check call args without insisting on exact match of defaults if they are passed as kwargs
        mock_process.assert_called_once()
        args, kwargs = mock_process.call_args
        assert args[0] == "test_file.py"
        assert args[1] == sample_analysis_result
