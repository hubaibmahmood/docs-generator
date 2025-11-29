import os
import shutil
import unittest
from unittest.mock import MagicMock, patch

from src.analysis.orchestrator import AnalysisOrchestrator
from src.models.analysis import CodeAnalysisResult, FileAnalysis, FunctionElement


class TestAnalysisOrchestrator(unittest.TestCase):

    def setUp(self):
        self.test_repo_dir = "/tmp/test_orchestrator_repo"
        os.makedirs(self.test_repo_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_repo_dir):
            shutil.rmtree(self.test_repo_dir)

    @patch('src.analysis.orchestrator.clone_repository')
    @patch('src.analysis.orchestrator.ParserFactory')
    def test_analyze_repository_success(self, MockParserFactory, mock_clone_repository):
        # Arrange
        orchestrator = AnalysisOrchestrator()
        repo_url = "https://github.com/test/repo"

        # Mock cloning
        mock_repo = MagicMock()
        mock_repo.working_dir = self.test_repo_dir
        mock_clone_repository.return_value = mock_repo

        dummy_file_name = "test_file.py"
        dummy_file_path_abs = os.path.join(self.test_repo_dir, dummy_file_name)
        with open(dummy_file_path_abs, "w") as f:
            f.write("def hello(): pass")

        # Mock ParserFactory
        mock_parser_instance = MagicMock()
        mock_file_analysis = FileAnalysis(
            file_path=dummy_file_path_abs,
            file_type="Python",
            language="Python",
            elements=[FunctionElement(name="hello", docstring=None, return_type=None)],
            dependencies=[],
            is_binary=False,
            errors=[],
        )
        mock_parser_instance.parse.return_value = mock_file_analysis
        MockParserFactory.get_parser.return_value = mock_parser_instance

        # Act
        result = orchestrator.analyze_repository(repo_url, self.test_repo_dir)

        # Assert
        mock_clone_repository.assert_called_once_with(repo_url, self.test_repo_dir)
        MockParserFactory.get_parser.assert_called()
        mock_parser_instance.parse.assert_called_once_with(dummy_file_path_abs)
        self.assertIsInstance(result, CodeAnalysisResult)
        self.assertEqual(len(result.file_analysis), 1)
        self.assertIn(dummy_file_name, result.file_analysis)
        self.assertEqual(result.file_analysis[dummy_file_name].elements[0].name, "hello")
        self.assertEqual(len(result.errors), 0)

    @patch('src.analysis.orchestrator.clone_repository', side_effect=Exception("Clone failed"))
    @patch('src.analysis.orchestrator.ParserFactory')
    def test_analyze_repository_clone_failure(self, MockParserFactory, mock_clone_repository):
        # Arrange
        orchestrator = AnalysisOrchestrator()
        repo_url = "invalid_url"

        # Act
        result = orchestrator.analyze_repository(repo_url, self.test_repo_dir)

        # Assert
        mock_clone_repository.assert_called_once_with(repo_url, self.test_repo_dir)
        MockParserFactory.get_parser.assert_not_called()
        self.assertIsInstance(result, CodeAnalysisResult)
        self.assertEqual(len(result.file_analysis), 0)
        self.assertEqual(len(result.errors), 1)
        self.assertIn("Clone failed", result.errors[0].error)

    @patch('src.analysis.orchestrator.clone_repository')
    @patch('src.analysis.orchestrator.ParserFactory')
    def test_analyze_repository_parse_failure(self, MockParserFactory, mock_clone_repository):
        # Arrange
        orchestrator = AnalysisOrchestrator()
        repo_url = "https://github.com/test/repo"

        mock_repo = MagicMock()
        mock_repo.working_dir = self.test_repo_dir
        mock_clone_repository.return_value = mock_repo

        dummy_file_name = "error_file.py"
        dummy_file_path_abs = os.path.join(self.test_repo_dir, dummy_file_name)
        with open(dummy_file_path_abs, "w") as f:
            f.write("def error_func(): return a +")

        # Mock ParserFactory to return a parser that fails
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse.side_effect = Exception("Syntax error")
        MockParserFactory.get_parser.return_value = mock_parser_instance

        # Act
        result = orchestrator.analyze_repository(repo_url, self.test_repo_dir)

        # Assert
        mock_clone_repository.assert_called_once_with(repo_url, self.test_repo_dir)
        MockParserFactory.get_parser.assert_called()
        mock_parser_instance.parse.assert_called_once_with(dummy_file_path_abs)
        self.assertIsInstance(result, CodeAnalysisResult)
        self.assertEqual(len(result.file_analysis), 0)
        self.assertEqual(len(result.errors), 1)
        self.assertIn("Syntax error", result.errors[0].error)

if __name__ == '__main__':
    unittest.main()
