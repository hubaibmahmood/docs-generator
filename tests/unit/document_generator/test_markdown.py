import pytest
from pathlib import Path
from src.document_generator.markdown import write_markdown_to_file


@pytest.fixture
def sample_markdown_content():
    return """# Test Document
This is a test document with some **markdown** formatting.

## Section 1
- Item 1
- Item 2

```python
def hello_world():
    print("Hello, world!")
```
"""

def test_write_markdown_to_file(tmp_path, sample_markdown_content):
    """Test that a Markdown string can be written to a file."""
    output_path = tmp_path / "docs" / "test_module.md"
    write_markdown_to_file(output_path, sample_markdown_content)

    assert output_path.exists()
    assert output_path.read_text() == sample_markdown_content

def test_write_markdown_to_file_creates_directories(tmp_path, sample_markdown_content):
    """Test that write_markdown_to_file creates necessary directories."""
    output_path = tmp_path / "nested" / "dirs" / "test_module.md"
    write_markdown_to_file(output_path, sample_markdown_content)

    assert output_path.exists()
    assert output_path.parent.is_dir()
    assert output_path.read_text() == sample_markdown_content
