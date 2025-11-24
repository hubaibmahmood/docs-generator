import pytest
from pathlib import Path
from src.models.doc_gen import GeneratedDocumentation
# from src.document_generator.markdown import render_to_markdown, write_markdown_to_file # Not implemented yet


@pytest.fixture
def sample_generated_documentation():
    return GeneratedDocumentation(
        summary="This is a summary of the module.",
        api_reference="""
## Functions

### `my_function(arg1: str, arg2: int) -> bool`
A function that does something.

```python
def my_function(arg1: str, arg2: int) -> bool:
    return True
```
""",
        examples="""
## Example Usage

```python
import my_module
result = my_module.my_function("test", 123)
print(result)
```
"""
    )

def test_render_to_markdown(sample_generated_documentation):
    """Test that GeneratedDocumentation can be rendered to a Markdown string."""
    from src.document_generator.markdown import render_to_markdown
    markdown_output = render_to_markdown(sample_generated_documentation)
    assert isinstance(markdown_output, str)
    assert "This is a summary of the module." in markdown_output
    assert "## Functions" in markdown_output
    assert "## Example Usage" in markdown_output
    assert "```python" in markdown_output

def test_write_markdown_to_file(tmp_path, sample_generated_documentation):
    """Test that a Markdown string can be written to a file."""
    from src.document_generator.markdown import render_to_markdown, write_markdown_to_file
    markdown_content = render_to_markdown(sample_generated_documentation)
    output_path = tmp_path / "docs" / "test_module.md"
    write_markdown_to_file(output_path, markdown_content)

    assert output_path.exists()
    assert output_path.read_text() == markdown_content

def test_write_markdown_to_file_creates_directories(tmp_path, sample_generated_documentation):
    """Test that write_markdown_to_file creates necessary directories."""
    from src.document_generator.markdown import render_to_markdown, write_markdown_to_file
    markdown_content = render_to_markdown(sample_generated_documentation)
    output_path = tmp_path / "nested" / "dirs" / "test_module.md"
    write_markdown_to_file(output_path, markdown_content)

    assert output_path.exists()
    assert output_path.parent.is_dir()
    assert output_path.read_text() == markdown_content
