import pytest

from src.analysis.repository import _validate_repo_url
from src.common.exceptions import RepositoryError


class TestSecurityVectors:
    """
    Verifies that the backend validator blocks known attack vectors.
    """

    def test_command_injection_patterns(self):
        vectors = [
            "https://github.com/user/repo; rm -rf /",
            "https://github.com/user/repo && echo 'pwned'",
            "https://github.com/user/repo | cat /etc/passwd",
            "--upload-pack=touch /tmp/pwned",
            "-oProxyCommand=calc",
        ]
        for url in vectors:
            with pytest.raises(RepositoryError) as excinfo:
                _validate_repo_url(url)
            assert "Invalid repository URL" in str(excinfo.value)

    def test_ssrf_patterns(self):
        vectors = [
            "http://localhost:8080/git",
            "http://127.0.0.1:22/user/repo",
            "http://0.0.0.0:8000/",
            "http://[::1]:80/",
        ]
        for url in vectors:
            with pytest.raises(RepositoryError) as excinfo:
                _validate_repo_url(url)
            # The error message might vary (Blocked access vs Invalid URL) but it MUST raise RepositoryError
            assert isinstance(excinfo.value, RepositoryError)

    def test_protocol_attacks(self):
        vectors = [
            "file:///etc/passwd",
            "ftp://example.com/repo.git",
            "gopher://example.com/1",
            "dict://example.com/d:word",
        ]
        for url in vectors:
            with pytest.raises(RepositoryError) as excinfo:
                _validate_repo_url(url)
            assert "Invalid repository URL protocol" in str(excinfo.value)

    def test_path_traversal(self):
        vectors = [
            "https://github.com/../../etc/passwd",
            "https://github.com/user/repo/../../../",
            "/etc/passwd",
            "../../../../tmp",
        ]
        for url in vectors:
            with pytest.raises(RepositoryError) as excinfo:
                _validate_repo_url(url)
            assert "Invalid repository URL" in str(excinfo.value)

    def test_credential_leaks(self):
        vectors = [
            "https://user:password@github.com/org/repo.git",
            "https://token@github.com/org/repo.git",
        ]
        for url in vectors:
            with pytest.raises(RepositoryError) as excinfo:
                _validate_repo_url(url)
            assert "Embedded credentials are not allowed" in str(excinfo.value)

    def test_valid_urls(self):
        """Ensure valid URLs are still allowed."""
        valid_urls = [
            "https://github.com/hubaibmahmood/docgen-ai",
            "https://gitlab.com/user/project.git",
            "git@github.com:user/repo.git",
            "ssh://git@github.com/user/repo.git",
        ]
        for url in valid_urls:
            try:
                _validate_repo_url(url)
            except RepositoryError as e:
                pytest.fail(f"Valid URL blocked: {url} - Error: {e}")
