

from pydantic import BaseModel, Field

from src.models.analysis import CodeAnalysisResult


class DocSectionJob(BaseModel):
    """Represents a job to generate a specific documentation section."""
    section_name: str  # e.g., "api-reference", "README"
    output_filename: str # e.g., "api-reference.md", "README.md"
    context_content: str # Aggregated context (code summaries, lists of routes, etc.)
    prompt_instruction: str # Specific instruction for this section


class GeneratedSection(BaseModel):
    """The raw markdown output from the AI Agent."""
    content: str
    title: str | None = None


class ProcessingResult(BaseModel):
    """The result of processing a single section."""
    section_name: str
    output_path: str
    status: str # "success", "skipped", "failed"
    error: str | None = None
    markdown_content: str | None = None


class BatchGenerationResult(BaseModel):
    """The aggregate result of the entire generation process."""
    total_sections: int
    processed: int
    skipped: int
    failed: int
    results: list[ProcessingResult] = Field(default_factory=list)
    source_analysis: CodeAnalysisResult | None = None

class UserGeminiApiKey(BaseModel):
    api_key: str
