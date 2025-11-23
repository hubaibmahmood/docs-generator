# Quickstart: AI Processing Engine

## Prerequisites

- Python 3.12+
- `uv` package manager
- `GEMINI_API_KEY` environment variable set.

## Installation

```bash
uv pip install -r requirements.txt
```

## Usage (CLI)

The engine can be invoked programmatically or via the API.

### Python API

```python
import asyncio
from src.document_generator.engine import DocumentGenerator
from src.models.analysis import CodeAnalysisResult

async def main():
    # 1. Load analysis result (from Step 1)
    # analysis_data = ... load from json ...
    analysis_result = CodeAnalysisResult(**analysis_data)

    # 2. Initialize Generator
    generator = DocumentGenerator()

    # 3. Run generation
    result = await generator.generate_docs(analysis_result, output_dir="docs/")
    
    print(f"Processed: {result.processed}, Failed: {result.failed}")

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