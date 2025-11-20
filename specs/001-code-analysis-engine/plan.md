# Implementation Plan: Code Analysis Engine

**Branch**: `001-code-analysis-engine` | **Date**: 2025-11-21 | **Spec**: [specs/001-code-analysis-engine/spec.md](specs/001-code-analysis-engine/spec.md)
**Input**: Feature specification from `/specs/001-code-analysis-engine/spec.md`

## Summary

This plan outlines the architecture for the **Code Analysis Engine**. The engine will accept a GitHub repository URL, clone it, and perform a detailed analysis of its structure and source code. The primary output will be a single, structured JSON object detailing the file tree, a deep analysis of each file's contents (functions, classes, dependencies), and a list of any parsing errors.

The technical approach will use **Python 3.12+**. Code parsing for multiple languages (Python, Java, JS, C) will be handled by the **`tree-sitter`** framework, and repository cloning will be managed using the **`GitPython`** library, as documented in the [research.md](research.md) file.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: `uv`, `GitPython`, `tree-sitter`, `tree-sitter-python` bindings, `pyyaml` (for API spec), `fastapi` (for API), `uvicorn` (for serving)
**Storage**: N/A (analysis is in-memory, output is JSON)
**Testing**: `pytest`
**Target Platform**: Linux server (for execution)
**Project Type**: Single project (CLI/API service)
**Performance Goals**: Correctness is the priority. For V1, the engine should handle a 100k LOC repository in under 10 minutes.
**Constraints**: Must handle syntax errors gracefully and not crash on large repositories.
**Scale/Scope**: The engine will be the core of a larger document generation system. It must be modular enough to support new languages and analysis types in the future.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [X] **Test-Driven Development**: The plan requires a full test suite (`unit`, `integration`, `contract`).
- [X] **Python 3.12+ with Type Hints**: The technical context specifies Python 3.12+ and type hints are mandated.
- [X] **Clean and Readable Code**: The proposed structure promotes separation of concerns.
- [X] **Document with ADRs**: Important decisions from `research.md` will be candidates for ADRs.
- [X] **SOLID, DRY, KISS**: The modular design (services, models, parser) adheres to these principles.
- [X] **Function contracts**: All new code will follow this rule.
- [X] **PEP 8 and Line Length**: Linters will enforce this.
- [X] **No Magic Numbers**: Constants will be used for exclusion patterns, retry counts, etc.
- [X] **All tests must pass**: This is a quality requirement.
- [X] **80% code coverage**: This is a quality requirement.
- [X] **Dataclasses for data structures**: The `data-model.md` will define these.

## Project Structure

### Documentation (this feature)

```text
specs/001-code-analysis-engine/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── contracts/
│   └── api.yaml         # Phase 1 output
└── tasks.md             # To be created by /sp.tasks
```

### Source Code (repository root)

```text
src/
├── analysis/
│   ├── __init__.py
│   ├── orchestrator.py    # Main service to coordinate cloning and analysis
│   ├── repository.py      # Handles cloning and file traversal
│   └── parsing/
│       ├── __init__.py
│       ├── factory.py     # Creates the correct parser for a given language
│       ├── base_parser.py # Abstract base class for all parsers
│       └── python_parser.py # Example implementation for Python with tree-sitter
├── models/
│   ├── __init__.py
│   └── analysis.py        # Dataclasses for the JSON output structure
├── api/
│   ├── __init__.py
│   ├── main.py            # FastAPI application entry point
│   └── routes.py          # API endpoints (e.g., /analyze)
└── common/
    ├── __init__.py
    ├── exceptions.py      # Custom exception classes
    └── constants.py       # Project-wide constants

tests/
├── integration/
│   └── test_analysis_orchestrator.py
└── unit/
    ├── analysis/
    │   ├── test_repository.py
    │   └── parsing/
    │       └── test_python_parser.py
    └── models/
        └── test_analysis.py
```

**Structure Decision**: A **single project** structure was chosen. The system is a self-contained service (whether accessed via API or CLI), so a monolithic structure under `src/` is simplest and aligns with the project type. The code is organized by function: `analysis` for the core logic, `models` for the data structures, `api` for the service interface, and `common` for shared utilities.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None*    |            |                                     |
