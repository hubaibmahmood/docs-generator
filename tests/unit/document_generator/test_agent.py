import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import json
from src.models.doc_gen import DocumentJob, GeneratedDocumentation
from src.models.analysis import FileAnalysis, CodeAnalysisResult
from agents import ModelBehaviorError


@pytest.fixture
def sample_document_job():
    file_analysis_mock = FileAnalysis(
        file_path="test_file.py",
        file_type="python",
        language="python",
        elements=[],
        dependencies=[],
    )
    code_analysis_result_mock = CodeAnalysisResult(
        file_tree={"test_file.py": {}},
        file_analysis={"test_file.py": file_analysis_mock}
    )
    return DocumentJob(
        file_path="test_file.py",
        content="def my_function(): pass",
        context={"project_name": "test_project"},
        analysis=code_analysis_result_mock,
    )


@pytest.mark.asyncio
async def test_generate_documentation_malformed_json(sample_document_job):
    """Test handling of malformed JSON output from the LLM."""
    
    # Mock Runner.run_streamed to return malformed JSON
    # Mock Runner.run_streamed to return malformed JSON
    with patch("src.document_generator.agent.Runner.run_streamed", new_callable=MagicMock) as mock_run:
        mock_result = MagicMock()
        mock_result = MagicMock()
        async def async_gen():
            yield MagicMock(data=MagicMock(delta='{"summary": "Incomplete JSON...'))
        mock_result.stream_events.return_value = async_gen()
        mock_run.return_value = mock_result
        
        from src.document_generator.agent import generate_documentation_from_job
        
        # Should raise ValueError or handle it (implementation choice)
        # The current implementation raises ValueError
        with pytest.raises(ValueError, match="Failed to parse JSON"):
            await generate_documentation_from_job(sample_document_job)


@pytest.mark.asyncio
async def test_generate_documentation_context_overflow(sample_document_job):
    """Test handling of context window overflow (mocked error)."""
    
    # Mock Runner.run_streamed to raise ModelBehaviorError or similar for token limit
    # OpenAI/Agents usually raise a specific error or just truncate.
    # Here we simulate an error that we want to handle.
    
    # Mock Runner.run_streamed to return malformed JSON
    with patch("src.document_generator.agent.Runner.run_streamed", new_callable=MagicMock) as mock_run:
        mock_result = MagicMock()
        mock_run.side_effect = Exception("Context window exceeded") # Generic for now
        
        from src.document_generator.agent import generate_documentation_from_job
        
        # Expectation: Should we retry with less context? 
        # For now, let's just ensure the error propagates or is handled if we implemented handling.
        # We haven't implemented handling yet, so expect failure.
        with pytest.raises(Exception, match="Context window exceeded"):
            await generate_documentation_from_job(sample_document_job)