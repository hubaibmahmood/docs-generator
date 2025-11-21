# src/common/exceptions.py

class CodeAnalysisException(Exception):
    """Base exception for all code analysis related errors."""
    pass

class RepositoryError(CodeAnalysisException):
    """Raised when there is an issue with repository operations (e.g., cloning)."""
    pass

class ParsingError(CodeAnalysisException):
    """Raised when a file cannot be parsed."""
    pass

class TaskError(CodeAnalysisException):
    """Raised when there is an error in task management or status."""
    pass
