from abc import ABC, abstractmethod
from typing import Set

from src.models.analysis import FileAnalysis

class BaseParser(ABC):
    @property
    @abstractmethod
    def supported_file_extensions(self) -> Set[str]:
        """Returns a set of file extensions that this parser supports (e.g., {'.py', '.pyw'})."""
        pass

    @abstractmethod
    def parse(self, file_path: str) -> FileAnalysis:
        """
        Parses a file and extracts code elements.

        Args:
            file_path (str): The path of the file to parse.

        Returns:
            FileAnalysis: The analysis result.
        """
        pass
