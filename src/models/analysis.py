from typing import Any

from pydantic import BaseModel, Field


class MethodElement(BaseModel):
    """Represents a method within a class."""
    name: str
    docstring: str | None = None
    return_type: str | None = None

class FunctionElement(BaseModel):
    """Represents a standalone function."""
    name: str
    docstring: str | None = None
    return_type: str | None = None

class ClassElement(BaseModel):
    """Represents a class."""
    name: str
    docstring: str | None = None
    methods: list[MethodElement] = Field(default_factory=list)

# ExtractedElement can be a FunctionElement or ClassElement for now,
# and can be extended with other element types in the future.
ExtractedElement = FunctionElement | ClassElement

class Dependency(BaseModel):
    """Represents a single dependency from a manifest file."""
    package_name: str
    source_file: str
    version_specifier: str | None = None

class AnalysisError(BaseModel):
    """Represents a failure to parse a specific file."""
    file_path: str
    error: str

class FileAnalysis(BaseModel):
    """Contains the detailed analysis for a single file."""
    file_path: str
    file_type: str
    language: str
    elements: list[ExtractedElement] = Field(default_factory=list)
    dependencies: list[Dependency] = Field(default_factory=list)
    is_binary: bool = False
    content: str | None = None
    errors: list[AnalysisError] = Field(default_factory=list)

class CodeAnalysisResult(BaseModel):
    """The main object returned by the analysis service."""
    file_tree: dict[str, Any] = Field(default_factory=dict)
    file_analysis: dict[str, "FileAnalysis"] = Field(default_factory=dict)
    errors: list[AnalysisError] = Field(default_factory=list)
