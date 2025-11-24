# Architectural Plan: Cohesive Documentation Generation

**Feature Branch**: `002-ai-processing-engine`
**Status**: Draft

## 1. Scope and Objectives

The goal is to transform the document generator from a "file-by-file" mirroring tool into a "cohesive project documentation" generator. The system will ingest the entire project's code analysis and produce a structured documentation site (README, Architecture, APIs, etc.).

### In Scope
- Refactoring `DocumentGeneratorEngine` to support "Section-Based" generation.
- Implementing specific "Context Strategies" for each section (e.g., Aggregating all API routes for `api-reference.md`).
- Updating the `DocGenAgent` prompt to handle diverse document types (Overview vs. API List vs. Setup Guide).
- Generating the target file structure:
    - `README.md`, `getting-started.md`, `architecture.md`, `api-reference.md`, `database-models.md`, `services.md`, `configuration.md`, `examples/*.md`.

### Out of Scope
- Generating unrelated files (e.g., `CONTRIBUTING.md` unless implicitly part of Getting Started).
- Interactive documentation websites (we generate Markdown files only).
- Parsing non-Python files (Step 1 analysis is already Python-focused).

## 2. Architecture & Design

### 2.1. Core Components

1.  **`DocumentGeneratorEngine` (Orchestrator)**:
    - **Current**: Iterates `analysis.files`, calls `process_file`.
    - **New**: Defines a list of `DocumentationSection` jobs. Iterates through these sections.
    - **Logic**:
        ```python
        sections = [
            ReadmeSection(),
            GettingStartedSection(),
            ArchitectureSection(),
            ApiReferenceSection(),
            ...
        ]
        for section in sections:
            context = section.gather_context(analysis_result)
            content = await agent.generate(section.prompt, context)
            write_file(section.output_path, content)
        ```

2.  **`SectionStrategy` (New Pattern)**:
    - Abstract base class defining how to `gather_context` and `format_prompt` for a specific document type.
    - **`ApiReferenceStrategy`**: Filters analysis for classes/functions decorated with `@app.get`, `@route`, etc.
    - **`ModelsStrategy`**: Filters for `BaseModel` (Pydantic) or `declarative_base` (SQLAlchemy) subclasses.
    - **`ArchitectureStrategy`**: Uses the entire file dependency graph + high-level folder structure.

3.  **`DocGenAgent` (Updated)**:
    - Needs a more flexible `system_instruction`. Instead of "Generate summary/api/examples for this file", it should be "Generate a technical document of type {type} based on the provided project context."
    - Output format might need to be simple Markdown string rather than strict JSON `GeneratedDocumentation` (Summary/API/Examples), OR we adapt the JSON schema to be generic (e.g., `title`, `content`).
    - **Decision**: Switch to returning **Raw Markdown** (or a simple wrapper) for maximum flexibility, since an "API Reference" looks very different from a "README".

### 2.2. Data Flow

1.  **Input**: `CodeAnalysisResult` (JSON graph of files, classes, functions).
2.  **Context Gathering**: Engine selects relevant subset of analysis for the target file (e.g., "Only files in `src/api`").
3.  **Prompting**:
    - "You are a Technical Writer. Generate `api-reference.md`."
    - "Context: [List of 50 API endpoints with signatures...]"
    - "Format: Group by Tag."
4.  **Generation**: LLM produces Markdown.
5.  **Output**: Write to `generated-docs/api-reference.md`.

## 3. Key Decisions

### 3.1. Context Window Management
*   **Challenge**: `CodeAnalysisResult` for a large project might exceed 1M tokens? (Unlikely for metadata, but possible with raw code).
*   **Decision**: We will send **Metadata Only** (signatures, docstrings, dependencies) from the analysis result, NOT the full raw source code of every file, unless specifically needed for small sections. The `CodeAnalysisResult` structure is already optimized for this.
*   **Fallback**: If metadata is too large, we split by module (e.g., `api-reference-part1.md`), but for V1 we assume it fits (Gemini Flash has ~1M context).

### 3.2. Output Schema
*   **Previous**: Rigid JSON `(summary, api, examples)`.
*   **New**: Flexible. The Agent should return the full file content.
*   **Validation**: Check if output is non-empty and looks like Markdown.

## 4. Implementation Plan

1.  **Refactor Models**: Update `DocumentJob` to support "Section" mode (or create `SectionJob`).
2.  **Implement Strategies**: Create classes for each target file type (`README`, `API`, etc.) that know how to filter `CodeAnalysisResult`.
3.  **Update Agent**: Modify `src/document_generator/agent.py` to accept a generic prompt and return Markdown.
4.  **Update Engine**: Rewrite `generate_documentation` loop to iterate strategies.
5.  **Tests**: Update integration tests to check for the new file list.

## 5. Risks
- **Hallucination**: Aggregating "all APIs" might lead to inventing endpoints if the analysis is fuzzy.
    - *Mitigation*: Strict instruction to "Only list APIs found in the context".
- **Context Limit**: Very large repos might break the "Single Architecture Doc" approach.
    - *Mitigation*: Gemini 1.5/2.5 Flash has massive context; we leverage that.