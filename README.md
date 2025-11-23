# Code Analysis and Documentation Generation Engine

This service analyzes a given software repository, understands the code structure, and uses an AI agent to automatically generate technical documentation in Markdown format.

## Prerequisites

- Python 3.12+
- `uv` package manager
- A running shell/terminal

### Environment Variables

Before running the service, you need to set up your environment variables. Create a `.env` file in the root of the project:

```
GEMINI_API_KEY="your_google_ai_studio_api_key"
```
Replace `"your_google_ai_studio_api_key"` with your actual API key.

## 1. Setup and Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/hubaibmahmood/docs-generator.git
    cd docs-generator
    ```

2.  **Create and Activate a Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    Install all required dependencies directly from the `pyproject.toml` file using `uv`.
    ```bash
    uv pip install .
    ```
    This will install all packages, including `fastapi`, `openai-agents`, and `tree-sitter` language packs.

## 2. Running the Service

Once the dependencies are installed, you can run the API service using `uvicorn`.

```bash
uvicorn src.api.main:app --reload --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

## 3. Workflow: Generating Documentation

The primary workflow involves submitting a repository for processing, which includes both analysis and documentation generation.

### a. Submit a Repository for Processing

Send a POST request to the `/process` endpoint with the GitHub URL.

```bash
curl -X POST "http://127.0.0.1:8000/process" \
     -H "Content-Type: application/json" \
     -d 
{
           "url": "https://github.com/hubaibmahmood/docs-generator"
         }
```

The response will contain a `task_id`:
```json
{
  "task_id": "some-unique-task-id"
}
```

### b. Check Job Status

Use the `task_id` to poll the `/status/{task_id}` endpoint.

```bash
curl "http://127.0.0.1:8000/status/some-unique-task-id"
```

The response will show the current status (`PENDING`, `IN_PROGRESS`, `SUCCESS`, or `FAILED`).
```json
{
  "task_id": "some-unique-task-id",
  "status": "IN_PROGRESS",
  "errors": []
}
```

### c. Retrieve the Result and Find Files

Once the status is `SUCCESS`, you can get the summary from the `/result/{task_id}` endpoint.

```bash
curl "http://127.0.0.1:8000/result/some-unique-task-id"
```

The response will be a `BatchGenerationResult` JSON object, summarizing the outcome of the documentation generation process.

**Most importantly, the generated documentation files will be saved to the `generated_docs/` directory** at the root of the project. The directory structure will mirror the original repository's structure.

For example, if the repository contained a file at `src/utils/helpers.py`, its generated documentation will be located at `generated_docs/src/utils/helpers.md`.
