from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.document_generator.engine import DocumentGeneratorEngine, process_section
from src.document_generator.strategies import DocumentationStrategy
from src.models.analysis import CodeAnalysisResult, FileAnalysis
from src.models.doc_gen import GeneratedSection, ProcessingResult


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
def mock_generate_section_success():
    async def _mock_generate_section(*args, **kwargs):
        return GeneratedSection(content="Mock Generated Content")
    return AsyncMock(side_effect=_mock_generate_section)


@pytest.mark.asyncio
async def test_process_section_skipped_on_empty_context(sample_analysis_result):
    """Test that process_section skips if DocumentationStrategy.gather_context returns empty."""

    mock_strategy = MagicMock(spec=DocumentationStrategy)
    mock_strategy.section_name = "Test Section"
    mock_strategy.output_filename = "test_section.md"
    mock_strategy.gather_context.return_value = "" # Simulate no context

    with patch("src.document_generator.engine.generate_section") as mock_generate_section:
        result = await process_section(mock_strategy, sample_analysis_result)

        assert result.status == "skipped"
        assert "No context found" in result.error
        mock_generate_section.assert_not_called()

@pytest.mark.asyncio
async def test_engine_orchestration(sample_analysis_result):
    """Test the engine orchestrating the batch process."""
    engine = DocumentGeneratorEngine()

    mock_strategies = [MagicMock(spec=DocumentationStrategy) for _ in range(3)]
    for i, strat in enumerate(mock_strategies):
        strat.section_name = f"Strategy {i}"
        strat.output_filename = f"strategy_{i}.md"
        strat.gather_context.return_value = f"Context for strategy {i}"
        strat.get_prompt.return_value = f"Prompt for strategy {i}"

    with patch("src.document_generator.engine.get_all_strategies", return_value=mock_strategies):
        with patch("src.document_generator.engine.process_section", new_callable=AsyncMock) as mock_process_section:
            mock_process_section.side_effect = [
                ProcessingResult(section_name=s.section_name, output_path=s.output_filename, status="success", markdown_content="content")
                for s in mock_strategies
            ]

            batch_result = await engine.generate_documentation(sample_analysis_result)

            assert batch_result.total_sections == 3
            assert batch_result.processed == 3
            assert batch_result.skipped == 0
            assert batch_result.failed == 0
            assert len(batch_result.results) == 3
            assert batch_result.source_analysis == sample_analysis_result

            assert mock_process_section.call_count == 3
            for i, strat in enumerate(mock_strategies):
                call_args = mock_process_section.call_args_list[i]
                assert call_args[0][0] == strat
                assert call_args[0][1] == sample_analysis_result
