import unittest
from unittest.mock import patch, MagicMock
from src.analysis.repository import clone_repository
from src.common.exceptions import RepositoryError
import git

class TestRepository(unittest.TestCase):

    @patch('git.Repo.clone_from')
    def test_clone_repository_success(self, mock_clone_from):
        # Arrange
        repo_url = "https://github.com/test/repo"
        destination = "/tmp/test_repo"
        mock_repo = MagicMock()
        mock_clone_from.return_value = mock_repo

        # Act
        repo = clone_repository(repo_url, destination)

        # Assert
        mock_clone_from.assert_called_once_with(repo_url, destination)
        self.assertEqual(repo, mock_repo)

    @patch('git.Repo.clone_from', side_effect=git.exc.GitCommandError("clone", "fatal: repository not found"))
    def test_clone_repository_failure(self, mock_clone_from):
        # Arrange
        repo_url = "invalid_url"
        destination = "/tmp/test_repo"

        # Act & Assert
        with self.assertRaises(RepositoryError) as context:
            clone_repository(repo_url, destination)
        
        self.assertTrue("Failed to clone repository" in str(context.exception))
        mock_clone_from.assert_called_once_with(repo_url, destination)

if __name__ == '__main__':
    unittest.main()
