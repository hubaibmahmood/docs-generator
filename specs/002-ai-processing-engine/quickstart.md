# Quickstart: AI Processing Engine

## Prerequisites

- Python 3.12+
- `uv` package manager
- `GEMINI_API_KEY` environment variable set.

## Installation

```bash
uv pip install -e .
```

## Usage (CLI)

The engine can be invoked programmatically or via the API.

### Python API

```python
import asyncio
import json
from src.document_generator.engine import DocumentGeneratorEngine
from src.models.analysis import CodeAnalysisResult

async def main():
    # 1. Load analysis result (from Step 1 output)
    # For example, assume analysis.json contains the CodeAnalysisResult structure
    with open("analysis.json", "r") as f:
        analysis_data = json.load(f)
    
    analysis_result = CodeAnalysisResult(**analysis_data)

    # 2. Initialize Generator
    generator = DocumentGeneratorEngine()

    # 3. Run generation
    # This will write markdown files to the docs/ directory by default
    result = await generator.generate_documentation(analysis_result)
    
    print(f"Total: {result.total_files}")
    print(f"Processed: {result.processed}")
    print(f"Skipped: {result.skipped}")
    print(f"Failed: {result.failed}")

if __name__ == "__main__":
    asyncio.run(main())
```

### HTTP API

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @analysis.json
```

```