# Quickstart: Code Analysis Engine

This guide provides instructions on how to set up and run the Code Analysis Engine service locally.

## Prerequisites

- Python 3.12+
- `uv` package manager
- A running shell/terminal

## 1. Setup and Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/hubaibmahmood/docs-generator.git
    cd docs-generator
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    Create a `requirements.txt` file with the following content:
    ```txt
    fastapi
    uvicorn
    GitPython
    tree-sitter
    ```
    Then, install the dependencies using `uv`:
    ```bash
    uv pip install -r requirements.txt
    ```
    You will also need to set up the `tree-sitter` parsers. For example, for Python:
    ```bash
    # This step will be automated in the implementation phase
    git clone https://github.com/tree-sitter/tree-sitter-python.git vendor/tree-sitter-python
    ```

## 2. Running the Service

Once the dependencies are installed, you can run the API service using `uvicorn`.

```bash
uvicorn src.api.main:app --reload --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

## 3. Using the API

You can interact with the service using any HTTP client, such as `curl`.

### a. Submit a Repository for Analysis

Send a POST request to the `/analyze` endpoint with the GitHub URL.

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
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

The response will show the current status:
```json
{
  "status": "IN_PROGRESS"
}
```

### c. Retrieve the Result

Once the status is `SUCCESS`, you can get the full analysis from the `/result/{task_id}` endpoint.

```bash
curl "http://127.0.0.1:8000/result/some-unique-task-id"
```

The response will be the complete `CodeAnalysisResult` JSON object as defined in the `data-model.md`.