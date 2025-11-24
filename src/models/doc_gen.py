from pydantic import BaseModel, Field
from typing import List, Optional


class DocSectionJob(BaseModel):
    """Represents a job to generate a specific documentation section."""
    section_name: str  # e.g., "api-reference", "README"
    output_filename: str # e.g., "api-reference.md", "README.md"
    context_content: str # Aggregated context (code summaries, lists of routes, etc.)
    prompt_instruction: str # Specific instruction for this section


class GeneratedSection(BaseModel):
    """The raw markdown output from the AI Agent."""
    content: str
    title: Optional[str] = None


class ProcessingResult(BaseModel):
    """The result of processing a single section."""
    section_name: str
    output_path: str
    status: str # "success", "skipped", "failed"
    error: Optional[str] = None
    markdown_content: Optional[str] = None


from src.models.analysis import CodeAnalysisResult

class BatchGenerationResult(BaseModel):
    """The aggregate result of the entire generation process."""
    total_sections: int
    processed: int
    skipped: int
    failed: int
    results: List[ProcessingResult] = Field(default_factory=list)
    source_analysis: Optional[CodeAnalysisResult] = None
