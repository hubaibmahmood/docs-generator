# Feature Specification: AI Processing Engine

**Feature Branch**: `002-ai-processing-engine`
**Created**: 2025-11-23
**Status**: Draft
**Input**: User description: "Implement Step 2: AI Processing Engine to generate documentation from code using OpenAI Agents SDK and Gemini 2.5 Flash."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Cohesive Project Documentation (Priority: P1)

As a developer, I want the system to analyze my entire project and generate a structured, cohesive set of documentation files (README, Architecture, API, etc.) instead of disjointed file-by-file documents, so that I have a ready-to-publish documentation site.

**Why this priority**: This is the new core value proposition.

**Independent Test**: Run the generator on the `document-generator` codebase itself. Assert that `generated-docs/README.md`, `generated-docs/architecture.md`, etc., are created and contain aggregated content.

**Acceptance Scenarios**:

1.  **Given** a codebase analysis, **When** the engine runs, **Then** it MUST generate a `README.md` containing a high-level project overview, purpose, and key features.
2.  **Given** a codebase analysis, **When** the engine runs, **Then** it MUST generate `getting-started.md` with installation and setup instructions (inferred from `pyproject.toml`, `requirements.txt`, etc.).
3.  **Given** the codebase structure, **When** the engine runs, **Then** it MUST generate `architecture.md` describing the system design, modules, and data flow.
4.  **Given** the code analysis finding API routes (e.g., FastAPI, Flask), **When** processing, **Then** it MUST aggregate ALL endpoints into a single `api-reference.md`.
5.  **Given** the code analysis finding data models (e.g., Pydantic, SQLAlchemy), **When** processing, **Then** it MUST aggregate ALL models into `database-models.md`.
6.  **Given** the code analysis finding services/business logic, **When** processing, **Then** it MUST aggregate them into `services.md`.
7.  **Given** configuration files or env var usage, **When** processing, **Then** it MUST generate `configuration.md`.
8.  **Given** usage examples found in docstrings or tests, **When** processing, **Then** it MUST generate feature-based examples in `examples/<feature>.md`.

### User Story 2 - Intelligent Aggregation (Priority: P2)

As a reader, I want related information (like all API endpoints) to be in one place, rather than scattered across multiple files matching the source code structure.

**Why this priority**: Usability of the generated docs.

**Acceptance Scenarios**:
1.  **Given** multiple source files defining API routes, **When** generating `api-reference.md`, **Then** the system MUST combine them into a single logical document, grouped by tag or router.

### Edge Cases

- **No APIs found**: `api-reference.md` should state "No API endpoints detected" or be omitted (decision: state it).
- **No Models found**: `database-models.md` should state "No data models detected".
- **Context Limit**: If the aggregated content is too large for one prompt, the system needs a strategy (e.g., summarize chunks then aggregate, or separate prompts for each section).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST perform a multi-pass or aggregated analysis of the codebase to generate cohesive documents.
- **FR-002**: The system MUST generate the following specific files in the output directory:
    - `README.md`
    - `getting-started.md`
    - `architecture.md`
    - `api-reference.md`
    - `database-models.md`
    - `services.md`
    - `configuration.md`
    - `examples/*.md`
- **FR-003**: The `api-reference.md` generation MUST identify and aggregate route definitions from all analyzed files.
- **FR-004**: The `database-models.md` generation MUST identify and aggregate class definitions that appear to be data models (Pydantic, ORM).
- **FR-005**: The `services.md` generation MUST identify business logic classes/functions.
- **FR-006**: The system MUST use the provided `Gemini 2.5 Flash` model.
- **FR-007**: The system MUST support "map-reduce" or similar strategies if the context for a single section (e.g., "All APIs") exceeds the model's context window, OR rely on the `code-analysis-engine`'s structured output to feed targeted context.
- **FR-008**: The output MUST be standard Markdown.

### Constraints

- **Tech Stack**: The implementation MUST use the `openai-agents-python` SDK.
- **Model Provider**: The implementation MUST use the `gemini-2.5-flash` model via the Google Generative Language API (compatible endpoint).
- **Output Format**: The output files MUST be in Markdown (`.md`) format.

### Key Entities

- **Project Knowledge Graph**: The aggregated understanding of the codebase (from Step 1 analysis).
- **Section Job**: A task to generate one of the cohesive documents (e.g., "Generate API Reference").

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The `generated-docs/` directory contains all 7 core files + `examples/` folder.
- **SC-002**: `api-reference.md` contains endpoints from at least 2 different source files (if applicable in the target repo).
- **SC-003**: `README.md` contains a non-empty "Overview" section.
- **SC-004**: The generation process completes without error for the `document-generator` repo itself.