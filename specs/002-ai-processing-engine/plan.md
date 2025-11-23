# Implementation Plan: AI Processing Engine

**Branch**: `002-ai-processing-engine` | **Date**: 2025-11-23 | **Spec**: [specs/002-ai-processing-engine/spec.md](../spec.md)
**Input**: Feature specification from `/specs/002-ai-processing-engine/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The AI Processing Engine (Step 2) automates the generation of documentation by processing the structural analysis from Step 1. It uses the OpenAI Agents SDK to interact with the Gemini 2.5 Flash model (via Google's OpenAI-compatible endpoint). The system reads raw source files, prompts the agent with project context, and generates structured Markdown documentation (Overview, API Reference, Usage Examples) while handling large files, concurrency, and errors gracefully.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: `uv`, `openai` (Python SDK), `asyncio`
**Storage**: Filesystem (for input source and output docs)
**Testing**: `pytest` (AsyncIO)
**Target Platform**: Local Execution / API Server
**Project Type**: Python Service / Library
**Performance Goals**: Process files < 2000 lines in < 60s.
**Constraints**: Must use OpenAI Agents SDK with Gemini 2.5 Flash.
**Scale/Scope**: Scalable to medium repositories (~10k LOC).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Test-Driven Development**: Tests will be written first.
- [x] **Python 3.12+ with Type Hints**: Verified.
- [x] **Clean and Readable Code**: Will follow principles.
- [x] **Document with ADRs**: Research captured decisions.
- [x] **SOLID, DRY, KISS**: Architecture separates concerns (Engine, Agent, storage).
- [x] **Function contracts**: Will use type hints and docstrings.
- [x] **PEP 8 and Line Length**: Will enforce with ruff/black.
- [x] **No Magic Numbers**: Constants will be used.
- [x] **All tests must pass**: CI requirement.
- [x] **80% code coverage**: CI requirement.
- [x] **Dataclasses for data structures**: Using Pydantic/Dataclasses for models.

## Project Structure

### Documentation (this feature)

```text
specs/002-ai-processing-engine/
├── plan.md              # This file
├── research.md          # Phase 0 output (Decisions & Unknowns)
├── data-model.md        # Phase 1 output (Entities)
├── quickstart.md        # Phase 1 output (Usage)
├── contracts/           # Phase 1 output (API)
│   └── api.yaml
└── tasks.md             # Phase 2 output (Tasks)
```

### Source Code
```text
src/
├── document_generator/
│   ├── __init__.py
│   ├── engine.py           # Core orchestration logic (Async)
│   ├── agent.py            # AI interaction (OpenAI SDK + Gemini)
│   ├── markdown.py         # Markdown rendering and file writing
│   └── validator.py        # Input validation logic
├── models/
│   └── doc_gen.py          # New data models (DocumentJob, Results)
└── api/
    └── routes.py           # Updated with /generate endpoint

tests/
├── unit/
│   └── document_generator/
│       ├── test_engine.py
│       ├── test_agent.py
│       └── test_markdown.py
└── integration/
    └── test_doc_generation_flow.py
```

**Structure Decision**: Modular "Clean Architecture" approach. `engine` orchestrates, `agent` handles external AI service, `markdown` handles IO/Formatting. Models are shared.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       |            |                                     |
