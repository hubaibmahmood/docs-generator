from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union, Any

class MethodElement(BaseModel):
    """Represents a method within a class."""
    name: str
    docstring: Optional[str] = None
    return_type: Optional[str] = None

class FunctionElement(BaseModel):
    """Represents a standalone function."""
    name: str
    docstring: Optional[str] = None
    return_type: Optional[str] = None

class ClassElement(BaseModel):
    """Represents a class."""
    name: str
    docstring: Optional[str] = None
    methods: List[MethodElement] = Field(default_factory=list)

# ExtractedElement can be a FunctionElement or ClassElement for now,
# and can be extended with other element types in the future.
ExtractedElement = Union[FunctionElement, ClassElement]

class Dependency(BaseModel):
    """Represents a single dependency from a manifest file."""
    package_name: str
    source_file: str
    version_specifier: Optional[str] = None

class AnalysisError(BaseModel):
    """Represents a failure to parse a specific file."""
    file_path: str
    error: str

class FileAnalysis(BaseModel):
    """Contains the detailed analysis for a single file."""
    file_path: str
    file_type: str
    language: str
    elements: List[ExtractedElement] = Field(default_factory=list)
    dependencies: List[Dependency] = Field(default_factory=list)
    is_binary: bool = False
    errors: List[AnalysisError] = Field(default_factory=list)

class CodeAnalysisResult(BaseModel):
    """The main object returned by the analysis service."""
    file_tree: Dict[str, Any] = Field(default_factory=dict)
    file_analysis: Dict[str, "FileAnalysis"] = Field(default_factory=dict)
    errors: List[AnalysisError] = Field(default_factory=list)
