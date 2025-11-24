from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.models.analysis import CodeAnalysisResult, FileAnalysis, ClassElement, FunctionElement
import json

class DocumentationStrategy(ABC):
    """Abstract base class for documentation generation strategies."""

    @property
    @abstractmethod
    def section_name(self) -> str:
        pass

    @property
    @abstractmethod
    def output_filename(self) -> str:
        pass

    @abstractmethod
    def gather_context(self, analysis: CodeAnalysisResult) -> str:
        """Extracts relevant information from the analysis result."""
        pass

    @abstractmethod
    def get_prompt(self, context: str) -> str:
        """Constructs the prompt for the AI Agent."""
        pass

    def _format_elements(self, elements: List[Any]) -> str:
        """Helper to format elements for context."""
        output = []
        for el in elements:
            if isinstance(el, ClassElement):
                output.append(f"Class: {el.name}")
                if el.docstring:
                    output.append(f"  Doc: {el.docstring[:100]}...")
                for method in el.methods:
                    output.append(f"  Method: {method.name} -> {method.return_type}")
            elif isinstance(el, FunctionElement):
                output.append(f"Function: {el.name} -> {el.return_type}")
                if el.docstring:
                    output.append(f"  Doc: {el.docstring[:100]}...")
        return "\n".join(output)


class ReadmeStrategy(DocumentationStrategy):
    section_name = "Project Overview"
    output_filename = "README.md"

    def gather_context(self, analysis: CodeAnalysisResult) -> str:
        # Summarize file tree and key files
        file_list = list(analysis.file_analysis.keys())
        return f"Total Files: {len(file_list)}\nFile List:\n" + "\n".join(file_list[:50])

    def get_prompt(self, context: str) -> str:
        return (
            "Generate a README.md for this project.\n"
            "Include:\n"
            "1. Project Title (Infer from directory name or files)\n"
            "2. High-level Description\n"
            "3. Key Features (Infer from file names like 'api', 'models')\n"
            "4. Project Structure Summary\n\n"
            f"Context:\n{context}"
        )


class ArchitectureStrategy(DocumentationStrategy):
    section_name = "Architecture"
    output_filename = "architecture.md"

    def gather_context(self, analysis: CodeAnalysisResult) -> str:
        # Use file tree and core modules
        # Filter for 'src' or 'app' or 'lib'
        core_files = [f for f in analysis.file_analysis.keys() if "/" in f] 
        return f"File Structure:\n" + "\n".join(core_files)

    def get_prompt(self, context: str) -> str:
        return (
            "Generate an architecture.md document.\n"
            "Describe the system design, modules, and data flow based on the file structure.\n"
            "Identify layers (e.g., API, Service, Data).\n\n"
            f"Context:\n{context}"
        )


class ApiReferenceStrategy(DocumentationStrategy):
    section_name = "API Reference"
    output_filename = "api-reference.md"

    def gather_context(self, analysis: CodeAnalysisResult) -> str:
        # Heuristic: Include files with 'api', 'route', 'controller' in path
        # OR functions starting with 'get_', 'post_', 'create_', 'update_' in likely API files
        relevant_content = []
        for file_path, file_data in analysis.file_analysis.items():
            if any(k in file_path.lower() for k in ['api', 'route', 'controller', 'view']):
                relevant_content.append(f"File: {file_path}")
                relevant_content.append(self._format_elements(file_data.elements))
        
        if not relevant_content:
             return "No obvious API files found (checked for 'api', 'route', 'controller')."
        return "\n".join(relevant_content)

    def get_prompt(self, context: str) -> str:
        return (
            "Generate an api-reference.md document.\n"
            "List all API endpoints found in the context.\n"
            "Group them by module/file.\n"
            "If no APIs are clearly identifiable, state that.\n\n"
            f"Context:\n{context}"
        )


class DataModelsStrategy(DocumentationStrategy):
    section_name = "Data Models"
    output_filename = "database-models.md"

    def gather_context(self, analysis: CodeAnalysisResult) -> str:
        # Heuristic: Include files with 'model', 'schema', 'entity' in path
        relevant_content = []
        for file_path, file_data in analysis.file_analysis.items():
            if any(k in file_path.lower() for k in ['model', 'schema', 'entity', 'dto']):
                 relevant_content.append(f"File: {file_path}")
                 relevant_content.append(self._format_elements(file_data.elements))
        
        return "\n".join(relevant_content)

    def get_prompt(self, context: str) -> str:
        return (
            "Generate a database-models.md document.\n"
            "List all data models/schemas found.\n"
            "Describe their attributes and methods if available.\n\n"
            f"Context:\n{context}"
        )

class GettingStartedStrategy(DocumentationStrategy):
    section_name = "Getting Started"
    output_filename = "getting-started.md"
    
    def gather_context(self, analysis: CodeAnalysisResult) -> str:
        # Look for config files
        relevant_files = ['pyproject.toml', 'requirements.txt', 'Dockerfile', 'docker-compose.yml', 'Makefile', 'package.json']
        found = []
        for f in relevant_files:
            if f in analysis.file_analysis:
                 found.append(f"Found {f}")
                 # Ideally we'd have content, but analysis might not have it. 
                 # We assume standard python setup if pyproject.toml exists.
        
        return "\n".join(found)

    def get_prompt(self, context: str) -> str:
         return (
            "Generate a getting-started.md document.\n"
            "Provide installation instructions based on the detected files (e.g., 'pip install', 'poetry install').\n"
            "Explain how to run the project if inferable.\n\n"
            f"Context:\n{context}"
        )

def get_all_strategies() -> List[DocumentationStrategy]:
    return [
        ReadmeStrategy(),
        GettingStartedStrategy(),
        ArchitectureStrategy(),
        ApiReferenceStrategy(),
        DataModelsStrategy(),
    ]
