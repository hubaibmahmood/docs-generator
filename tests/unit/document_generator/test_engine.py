import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from pathlib import Path # Added import
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

@pytest.fixture
def mock_generate_documentation_from_job():
    async def _mock_generate_documentation_from_job(*args, **kwargs):
        return GeneratedDocumentation(
            summary="Mock Summary", api_reference="Mock API", examples="Mock Examples"
        )
    return AsyncMock(side_effect=_mock_generate_documentation_from_job)


@pytest.mark.asyncio
async def test_trivial_file_detection_empty_elements(mock_generate_documentation_from_job):
    """Test that files with no extracted elements are skipped."""
    
    file_analysis = FileAnalysis(
        file_path="trivial.py",
        file_type="python",
        language="python",
        elements=[], # Empty elements
        dependencies=[]
    )
    
    analysis_result = CodeAnalysisResult(
        file_tree={},
        file_analysis={"trivial.py": file_analysis}
    )
    
    with patch("src.document_generator.engine.generate_documentation_from_job", new=mock_generate_documentation_from_job):
        # Create mocks for base_dir and output_dir
        mock_base_dir = MagicMock()
        mock_output_dir = MagicMock()
        
        # Mock the file path object
        mock_file_path = MagicMock()
        mock_file_path.exists.return_value = True
        mock_file_path.read_text.return_value = "import os"
        mock_file_path.with_suffix.return_value = MagicMock(spec=Path)
        
        # Setup base_dir / "trivial.py" -> mock_file_path
        def truediv_side_effect(other):
            if str(other) == "trivial.py":
                return mock_file_path
            return MagicMock()
        mock_base_dir.__truediv__.side_effect = truediv_side_effect

        # Mock write_markdown_to_file
        with patch("src.document_generator.engine.write_markdown_to_file") as mock_write:
            result = await process_file(
                "trivial.py", 
                analysis_result, 
                base_dir=mock_base_dir, 
                output_dir=mock_output_dir
            )
            
            assert result.status == "skipped"
            mock_generate_documentation_from_job.assert_not_called()
            mock_write.assert_not_called()

@pytest.mark.asyncio
async def test_engine_orchestration(sample_analysis_result, mock_generate_documentation_from_job):
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
        # Corrected assertion to include default arguments
        mock_process.assert_called_once()
        call_args = mock_process.call_args
        assert call_args[0][0] == "test_file.py"
        assert call_args[0][1] == sample_analysis_result
        assert str(call_args[1]['base_dir']) == "."
        assert str(call_args[1]['output_dir']) == "docs"