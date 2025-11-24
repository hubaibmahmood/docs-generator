# Research: AI Processing Engine

**Feature**: AI Processing Engine (Step 2)
**Date**: 2025-11-23
**Status**: Completed

## Decisions

### 1. SDK and Model Integration
- **Decision**: Use the standard `openai` Python library (v1.x+) configured with Google's OpenAI-compatible endpoint (`https://generativelanguage.googleapis.com/v1beta/openai/`) to access `gemini-2.5-flash`.
- **Rationale**: The spec requires "OpenAI Agents SDK" and "Gemini 2.5 Flash". Google provides an OpenAI-compatible endpoint for Gemini. This allows using the robust OpenAI SDK client patterns while leveraging the specific model required.
- **Alternatives**: 
  - `google-generativeai` SDK: Rejected due to explicit constraint to use "OpenAI Agents SDK" (interpreted as OpenAI client/patterns).
  - `langchain` / `llamaindex`: Rejected to keep dependencies minimal and stick to the "OpenAI Agents SDK" constraint.

### 2. Input Data Validation
- **Decision**: Reuse the existing `CodeAnalysisResult` dataclass from `src.models.analysis` for schema validation.
- **Rationale**: The input is the output of Step 1. The `CodeAnalysisResult` is already defined and Pydantic/Dataclass compatible.
- **Implementation**: `src.document_generator.validator.validate_analysis_result(data: dict) -> CodeAnalysisResult`.

### 3. Concurrency Model
- **Decision**: Use `asyncio` with `asyncio.Semaphore` to limit concurrency.
- **Rationale**: Requirement "Process files one by one using async IO" (Sequential Async) and "Sequential processing" implies a limit of 1 (or strict sequence). However, "process files one by one" usually means concurrency=1.
- **Correction**: The Clarifications say "Sequential Async: Process files one by one". This means concurrency = 1. I will implement a loop `for file in files: await process(file)`.

### 4. Project Structure
- **Decision**: Implement core logic in `src/document_generator/`.
- **Components**:
  - `engine.py`: Main orchestrator.
  - `agent.py`: Wraps the OpenAI client interactions.
  - `markdown.py`: Handles markdown generation/saving.

## Unknowns Resolved

- **Input Schema**: Found in `src/models/analysis.py` (Step 1).
- **Trivial File Detection**: Heuristic will be:
  - File size < 10 bytes? OR
  - `AST` check (from Step 1 data) shows 0 classes and 0 functions?
  - Decision: Use Step 1 `elements` list. If `elements` is empty AND file size is small (< 50 chars), skip.

## Open Questions (None)
All items resolved.
