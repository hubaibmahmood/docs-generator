# Actionable Tasks: Code Analysis Engine

**Feature**: Code Analysis Engine | **Plan**: [plan.md](plan.md) | **Spec**: [spec.md](spec.md)

This document breaks down the implementation of the Code Analysis Engine into a series of dependency-ordered, testable tasks.

## Implementation Strategy

The implementation will follow a **TDD (Test-Driven Development)** and **MVP-first** approach. We will start with User Story 1, which is the core functionality. Each task is designed to be small, independently testable, and reversible.

**Suggested MVP Scope**: User Story 1 (Tasks T009-T022) is the minimum viable product. It delivers the core analysis functionality.

## Phase 1: Setup (Project Initialization)

These tasks establish the project structure and install dependencies. They do not have direct tests but are validated by the successful execution of subsequent tasks.

- [X] T001 Run `uv init --package` to create the project.
- [X] T002 Create the initial project directory structure as defined in `plan.md`.
- [X] T003 Initialize a Python virtual environment and install primary dependencies: `fastapi`, `uvicorn`, `GitPython`, `tree-sitter`, `pyyaml`, `pytest`.
- [X] T004 Create `src/common/constants.py` and define exclusion patterns for files/directories.
- [X] T005 Create `src/common/exceptions.py` for custom exception classes.

## Phase 2: Foundational (Models and Core API)

This phase sets up the data structures and the basic API shell, which are prerequisites for all user stories.

- [X] T006 [P] Create `tests/unit/models/test_analysis.py` to test the dataclasses.
- [X] T007 Implement all dataclasses (`CodeAnalysisResult`, `FileAnalysis`, `AnalysisError`, etc.) in `src/models/analysis.py` as defined in `data-model.md`.
- [X] T008 Create the basic FastAPI application in `src/api/main.py` and `src/api/routes.py`.
- [X] T009 [P] [US1] Create contract test for `POST /analyze` endpoint in `tests/integration/test_api.py`.

## Phase 3: User Story 1 (P1) - Core Code Analysis

**Goal**: Provide a GitHub URL and receive a structured JSON output of the repository's analysis.
**Independent Test Criteria**: A test that provides a sample repository URL and asserts that the final JSON output matches a pre-defined, expected structure.

### User Story 1: Test Definitions

- [X] T010 [P] [US1] Write unit tests for `repository.py` cloning functionality in `tests/unit/analysis/test_repository.py`.
- [X] T011 [P] [US1] Write unit tests for `python_parser.py` in `tests/unit/analysis/parsing/test_python_parser.py`.
- [X] T012 [P] [US1] Write integration tests for the `AnalysisOrchestrator` in `tests/integration/test_analysis_orchestrator.py`.

### User Story 1: Implementation Tasks

- [X] T013 [US1] Implement the repository cloning logic in `src/analysis/repository.py` using `GitPython`.
- [X] T014 [US1] Implement the abstract base class `BaseParser` in `src/analysis/parsing/base_parser.py`.
- [X] T015 [US1] Implement the `PythonParser` in `src/analysis/parsing/python_parser.py` using `tree-sitter`.
- [X] T016 [US1] Implement the parser factory in `src/analysis/parsing/factory.py` to select the correct parser based on file type.
- [X] T017 [US1] Implement the main `AnalysisOrchestrator` in `src/analysis/orchestrator.py` to coordinate cloning and analysis.
- [X] T018 [US1] Implement the `POST /analyze` endpoint in `src/api/routes.py` to trigger the analysis.
- [X] T019 [US1] Implement the `GET /status/{task_id}` endpoint in `src/api/routes.py`.
- [X] T020 [US1] Implement the `GET /result/{task_id}` endpoint in `src/api/routes.py`.

## Phase 4: Polish & Cross-Cutting Concerns

These tasks address final touches and non-functional requirements.

- [X] T021 Add comprehensive logging to all services.
- [X] T022 Create a `README.md` with setup and usage instructions based on `quickstart.md`.
- [X] T023 Set up linting with `ruff` and formatting with `black`.

## Dependencies

- **Phase 1** must be completed before **Phase 2**.
- **Phase 2** must be completed before **Phase 3**.
- Within **Phase 3 (US1)**, tests should be written before implementation tasks.

## Parallel Execution

- Tasks marked with `[P]` can be worked on in parallel.
- For User Story 1, the tests (`T010`, `T011`, `T012`) can be developed in parallel.
- The API endpoints (`T018`, `T019`, `T020`) can be developed in parallel after the orchestrator is complete.
