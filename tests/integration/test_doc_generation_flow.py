from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pathlib import Path

from src.document_generator.engine import DocumentGeneratorEngine, process_section
from src.document_generator.strategies import ReadmeStrategy
from src.models.analysis import CodeAnalysisResult, FileAnalysis
from src.models.doc_gen import GeneratedSection, ProcessingResult, DocSectionJob


@pytest.fixture
def sample_analysis_result():
    file_analysis_mock = FileAnalysis(
        file_path="src/api/main.py",
        file_type="python",
        language="python",
        elements=[],
        dependencies=[],
    )
    return CodeAnalysisResult(
        file_tree={"src": {"api": {"main.py": {}}}},
        file_analysis={"src/api/main.py": file_analysis_mock},
        errors=[],
    )


@pytest.mark.asyncio
async def test_process_section_success(sample_analysis_result, tmp_path):
    """Test successful section processing."""
    
    strategy = ReadmeStrategy()
    
    # Mock generate_section
    with patch("src.document_generator.engine.generate_section", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = GeneratedSection(content="# README Content", title="Project Overview")

        # We also need to mock write_markdown_to_file
        with patch("src.document_generator.engine.write_markdown_to_file") as mock_write:
            result = await process_section(
                strategy, 
                sample_analysis_result, 
                output_dir=tmp_path / "generated-docs"
            )

            assert result.status == "success"
            assert result.section_name == "Project Overview"
            mock_gen.assert_called_once()
            mock_write.assert_called_once()


@pytest.mark.asyncio
async def test_engine_orchestration(sample_analysis_result):
    """Test the engine orchestrating the batch process."""
    engine = DocumentGeneratorEngine()

    with patch("src.document_generator.engine.process_section", new_callable=AsyncMock) as mock_process:
        mock_process.return_value = ProcessingResult(
            section_name="Project Overview", output_path="docs/README.md", status="success"
        )

        batch_result = await engine.generate_documentation(sample_analysis_result)

        # Check that we processed sections (strategies count)
        # We have 5 default strategies
        assert batch_result.total_sections >= 1 
        assert batch_result.processed == len(batch_result.results)
        
        assert mock_process.call_count >= 1