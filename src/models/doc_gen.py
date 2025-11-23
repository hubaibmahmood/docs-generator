from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from src.models.analysis import FileAnalysis, CodeAnalysisResult


class DocumentJob(BaseModel):
    """Represents a single file processing task."""
    file_path: str
    content: str
    context: Dict[str, Any] = Field(default_factory=dict)
    analysis: CodeAnalysisResult


class GeneratedDocumentation(BaseModel):
    """The structured output from the AI Agent (before saving)."""
    summary: str
    api_reference: str
    examples: str


class ProcessingResult(BaseModel):
    """The result of processing a single file."""
    file_path: str
    doc_path: str
    status: str # "success", "skipped", "failed"
    error: Optional[str] = None
    markdown_content: Optional[str] = None


class BatchGenerationResult(BaseModel):
    """The aggregate result of the entire generation process."""
    total_files: int
    processed: int
    skipped: int
    failed: int
    results: List[ProcessingResult] = Field(default_factory=list)