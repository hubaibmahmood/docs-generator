"""Validator module for input validation."""
from src.models.analysis import CodeAnalysisResult


def validate_analysis_result(result: CodeAnalysisResult) -> bool:
    """
    Validates a CodeAnalysisResult object.

    A CodeAnalysisResult is considered valid if:
    - It contains at least one file analysis entry.
    - It does not contain any critical errors.
    """
    if not result.file_analysis:
        return False
    if result.errors:
        return False
    return True
