import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.common.security.redactor import SecretRedactor
from src.models.analysis import ClassElement, CodeAnalysisResult, FileAnalysis, FunctionElement


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
    def gather_context_raw(self, analysis: CodeAnalysisResult) -> str:
        """
        Extracts relevant information from the analysis result.
        Subclasses must implement this instead of gather_context.
        """
        pass

    def gather_context(self, analysis: CodeAnalysisResult) -> str:
        """
        Public method to gather and automatically redact context.
        """
        raw_context = self.gather_context_raw(analysis)
        return SecretRedactor.redact(raw_context)

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

    def gather_context_raw(self, analysis: CodeAnalysisResult) -> str:
        """Summarize file tree and key files"""
        file_list = list(analysis.file_analysis.keys())
        context = f"Total Files: {len(file_list)}\nFile List:\n" + "\n".join(file_list[:50])

        # Include existing README content if available to preserve original intent/badges
        for file_path, file_data in analysis.file_analysis.items():
            if file_path.lower() == "readme.md" and file_data.content:
                context += (
                    f"\n\n--- Original README.md Content ---\n{file_data.content[:5000]}\n--- End Original README ---"
                )
                break

        return context

    def get_prompt(self, context: str) -> str:
        return (
            "Generate a comprehensive README.md for this project.\n"
            "Include:\n"
            "1. Project Title & Description (Use original README as a base if available)\n"
            "2. High-level Description\n"
            "3. Key Features (Infer from file names and original README)\n"
            "4. Project Structure Summary\n"
            "- DO NOT include installation, setup, or running instructions. This will be covered in 'Getting Started'.\n\n"
            f"Context:\n{context}"
        )


class ArchitectureStrategy(DocumentationStrategy):
    section_name = "Architecture"
    output_filename = "architecture.md"

    def gather_context_raw(self, analysis: CodeAnalysisResult) -> str:
        """Use file tree and core modules"""
        # Filter for 'src' or 'app' or 'lib'
        core_files = [f for f in analysis.file_analysis.keys() if "/" in f]
        context = f"File Structure:\n" + "\n".join(core_files)

        # Add content of key files to provide architectural context
        context += "\n\nKey File Contents:\n"
        count = 0
        for f in core_files:
            # Heuristic: prioritize typical entry points or core logic
            if any(x in f.lower() for x in ["main", "app", "server", "config", "models", "routes"]) and count < 10:
                if f in analysis.file_analysis and analysis.file_analysis[f].content:
                    context += f"\n--- {f} ---\n{analysis.file_analysis[f].content[:2000]}\n"
                    count += 1

        return context

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

    def gather_context_raw(self, analysis: CodeAnalysisResult) -> str:
        """Heuristic: Include files with 'api', 'route', 'controller' in path"""
        # OR functions starting with 'get_', 'post_', 'create_', 'update_' in likely API files
        relevant_content = []
        for file_path, file_data in analysis.file_analysis.items():
            if any(k in file_path.lower() for k in ["api", "route", "controller", "view"]):
                relevant_content.append(f"File: {file_path}")
                if file_data.content:
                    relevant_content.append(f"Content:\n{file_data.content[:5000]}")
                else:
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

    def gather_context_raw(self, analysis: CodeAnalysisResult) -> str:
        """Heuristic: Include files with 'model', 'schema', 'entity' in path"""
        relevant_content = []
        for file_path, file_data in analysis.file_analysis.items():
            if any(k in file_path.lower() for k in ["model", "schema", "entity", "dto"]):
                relevant_content.append(f"File: {file_path}")
                if file_data.content:
                    relevant_content.append(f"Content:\n{file_data.content[:3000]}")
                else:
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

    def gather_context_raw(self, analysis: CodeAnalysisResult) -> str:
        """Look for config files"""
        relevant_files = [
            "pyproject.toml",
            "requirements.txt",
            "Dockerfile",
            "docker-compose.yml",
            "Makefile",
            "package.json",
            "README.md",
        ]
        found = []
        for f in relevant_files:
            if f in analysis.file_analysis:
                file_data = analysis.file_analysis[f]
                found.append(f"Found {f}")
                if file_data.content:
                    # Include content to help with specific instructions
                    found.append(f"--- Content of {f} ---\n{file_data.content[:3000]}\n--- End of {f} ---")

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
