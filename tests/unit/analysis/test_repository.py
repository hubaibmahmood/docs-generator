import unittest
from unittest.mock import MagicMock, patch

import git

from src.analysis.repository import clone_repository
from src.common.exceptions import RepositoryError


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
        repo_url = "https://github.com/test/invalid_repo"
        destination = "/tmp/test_repo"

        # Act & Assert
        with self.assertRaises(RepositoryError) as context:
            clone_repository(repo_url, destination)

        self.assertTrue("Failed to clone repository" in str(context.exception))
        mock_clone_from.assert_called_once_with(repo_url, destination)

    def test_clone_repository_invalid_protocol(self):
        # Arrange
        repo_url = "ftp://github.com/test/repo"
        destination = "/tmp/test_repo"

        # Act & Assert
        with self.assertRaises(RepositoryError) as context:
            clone_repository(repo_url, destination)

        self.assertTrue("Invalid repository URL protocol" in str(context.exception))

    def test_clone_repository_command_injection(self):
        # Arrange
        repo_url = "https://github.com/test/repo/--upload-pack=touch /tmp/pwned"
        destination = "/tmp/test_repo"

        # Act & Assert
        with self.assertRaises(RepositoryError) as context:
            clone_repository(repo_url, destination)

        self.assertTrue("potential command injection" in str(context.exception))

    def test_clone_repository_invalid_characters(self):
        # Arrange
        repo_url = "https://github.com/test/repo; rm -rf /"
        destination = "/tmp/test_repo"

        # Act & Assert
        with self.assertRaises(RepositoryError) as context:
            clone_repository(repo_url, destination)

        self.assertTrue("illegal characters" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
