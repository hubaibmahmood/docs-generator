import pytest
from src.models.analysis import CodeAnalysisResult, FileAnalysis, AnalysisError
# from src.document_generator.validator import validate_analysis_result # This will cause an error as it's not implemented yet.


def test_validate_analysis_result_valid():
    """Test that a valid CodeAnalysisResult passes validation."""
    file_analysis_mock = FileAnalysis(
        file_path="test_file.py",
        file_type="python",
        language="python",
        elements=[],
        dependencies=[],
    )
    valid_result = CodeAnalysisResult(
        file_tree={"test_file.py": {}},
        file_analysis={"test_file.py": file_analysis_mock},
        errors=[],
    )
    # This function is not yet implemented, so this import will fail
    from src.document_generator.validator import validate_analysis_result
    assert validate_analysis_result(valid_result) is True


def test_validate_analysis_result_empty_file_analysis():
    """Test that a CodeAnalysisResult with empty file_analysis fails validation."""
    empty_analysis_result = CodeAnalysisResult(
        file_tree={"test_file.py": {}},
        file_analysis={},
        errors=[],
    )
    from src.document_generator.validator import validate_analysis_result
    assert validate_analysis_result(empty_analysis_result) is False


def test_validate_analysis_result_with_errors():
    """Test that a CodeAnalysisResult with errors fails validation."""
    error_result = CodeAnalysisResult(
        file_tree={},
        file_analysis={},
        errors=[AnalysisError(file_path="bad_file.py", error="Syntax error")],
    )
    from src.document_generator.validator import validate_analysis_result
    assert validate_analysis_result(error_result) is False


def test_validate_analysis_result_empty_object():
    """Test that an empty CodeAnalysisResult object fails validation."""
    empty_object_result = CodeAnalysisResult(
        file_tree={},
        file_analysis={},
        errors=[],
    )
    from src.document_generator.validator import validate_analysis_result
    assert validate_analysis_result(empty_object_result) is False
