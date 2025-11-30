# Docgen AI: Intelligent Code Documentation Generator

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/frontend-React-61DAFB.svg)](https://react.dev/)

Docgen AI is an intelligent platform designed to automate the generation of technical documentation for software projects. It analyzes your codebase, understands its structure and logic, and leverages an AI agent to produce comprehensive, accurate, and up-to-date documentation in Markdown format.

## ✨ Features

-   **AI-Powered Documentation Generation**: Automatically generates detailed Markdown documentation from source code.
-   **Code Analysis**: Deeply analyzes repository structure, functions, classes, and dependencies.
-   **Multi-language Support**: Designed to be extensible for various programming languages (currently Python).
-   **Authentication System**: Secure user registration and login with token-based authentication (HTTP-only cookies).
-   **Interactive Web Interface**: A user-friendly React frontend to interact with the documentation generation process.
-   **Scalable Architecture**: Built with FastAPI for a robust and performant backend.
-   **Local Development**: Supports SQLite for local database operations.

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:

-   **Python 3.12+**: For the backend services.
-   **uv**: A fast Python package installer and dependency resolver.
-   **Node.js & npm (or yarn)**: For the frontend development.

### Environment Variables

Create a `.env` file in the root of the project with the following variable:

```
APP_ENCRYPTION_KEY="your_url_safe_base64_32_byte_key"
```

This key is essential for encrypting sensitive data, such as user-provided API keys, before they are stored in the database.

**Generating `APP_ENCRYPTION_KEY`**:
You can generate a URL-safe base64-encoded 32-byte key using a Python script:

```python
import os
import base64
key = base64.urlsafe_b64encode(os.urandom(32)).decode()
print(key)
```

Run this script and copy the output into your `.env` file for `APP_ENCRYPTION_KEY`.

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/hubaibmahmood/docs-generator.git
cd docs-generator
```

#### 2. Backend Setup

```bash
# Create and activate a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install backend dependencies using uv
uv pip install .

# Apply database migrations
alembic upgrade head
```

#### 3. Frontend Setup

```bash
cd docgen-ai
npm install # or yarn install
cd ..
```

### Running the Application

#### 1. Start the Backend API

From the project root directory:

```bash
source .venv/bin/activate # if not already active
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend API will be available at `http://localhost:8000`.

#### 2. Start the Frontend Development Server

From the project root directory:

```bash
cd docgen-ai
npm run dev # or yarn dev
```

The frontend application will typically open in your browser at `http://localhost:5173` (or another port if 5173 is in use).

## 💡 Usage

### Web Interface

Navigate to the frontend application URL (e.g., `http://localhost:5173`) in your web browser. You can:

1.  **Register/Login**: Create an account or log in to access the documentation generation features.
2.  **Submit Repository URL**: Provide a GitHub repository URL for analysis and documentation generation.
3.  **View Generated Docs**: Monitor the status and view the generated Markdown documentation directly in the browser.

### API Endpoints (Brief Overview)

The backend provides a RESTful API for interacting with the documentation generation engine.

-   `POST /auth/register`: Register a new user.
-   `POST /auth/token`: Authenticate user and get an access token.
-   `POST /process`: Submit a GitHub repository URL for processing.
-   `GET /status/{task_id}`: Check the status of a documentation generation job.
-   `GET /result/{task_id}`: Retrieve the result (summary and file paths) of a completed job.
-   `GET /docs/raw/{file_path:path}`: Retrieve raw content of a generated documentation file.

For detailed API documentation, refer to the OpenAPI docs at `/docs` or `/redoc` when the backend is running.

## 🔒 Security Considerations


-   **URL Validation**: Robust URL validation and sanitization are implemented to prevent SSRF and path traversal attacks.

## 🤝 Contributing

We welcome contributions! Please see our `CONTRIBUTING.md` (to be created) for details on how to contribute, report bugs, and suggest features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/hubaibmahmood/docs-generator).
