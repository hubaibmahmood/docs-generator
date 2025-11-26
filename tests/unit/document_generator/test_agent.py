import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import json
from src.models.doc_gen import DocSectionJob, GeneratedSection
from src.document_generator.agent import generate_section
from src.models.analysis import FileAnalysis, CodeAnalysisResult
from agents import ModelBehaviorError


@pytest.fixture
def sample_doc_section_job():
    return DocSectionJob(
        section_name="Test Section",
        output_filename="test_section.md",
        context_content="This is some test context for the AI.",
        prompt_instruction="Generate documentation based on the context."
    )





@pytest.mark.asyncio
async def test_generate_documentation_context_overflow(sample_doc_section_job):
    """Test handling of context window overflow (mocked error)."""
    
    with patch("src.document_generator.agent.Runner.run", new_callable=MagicMock) as mock_run:
        mock_run.side_effect = Exception("Context window exceeded") # Generic for now
        
        with pytest.raises(Exception, match="Context window exceeded"):
            await generate_section(sample_doc_section_job)