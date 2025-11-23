# Tasks: AI Processing Engine

**Input**: Design documents from `/specs/002-ai-processing-engine/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The feature specification implies the generation of tests as part of the TDD approach.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 [P] Create `src/document_generator/__init__.py` if it doesn't exist.
- [ ] T002 [P] Create `src/document_generator/engine.py` for orchestration logic.
- [ ] T003 [P] Create `src/document_generator/agent.py` for AI interaction.
- [ ] T004 [P] Create `src/document_generator/markdown.py` for Markdown rendering and file writing.
- [ ] T005 [P] Create `src/document_generator/validator.py` for input validation.
- [ ] T006 [P] Create `src/models/doc_gen.py` for new data models.
- [ ] T007 [P] Install `openai` Python SDK (add to `pyproject.toml` and run `uv pip install -e .`).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented. This includes shared models and validation.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Foundational Tasks

- [ ] T008 Implement `DocumentJob`, `GeneratedDocumentation`, `ProcessingResult`, and `BatchGenerationResult` dataclasses in `src/models/doc_gen.py`.
- [ ] T009 Write RED unit tests for `src/models/doc_gen.py` in `tests/unit/models/test_doc_gen.py`.
- [ ] T010 Implement input validation logic for `CodeAnalysisResult` in `src/document_generator/validator.py`.
- [ ] T011 Write RED unit tests for `src/document_generator/validator.py` in `tests/unit/document_generator/test_validator.py`.
- [ ] T012 Configure `openai` client in `src/document_generator/agent.py` to use `gemini-2.5-flash` with Google's OpenAI-compatible endpoint, including API key handling.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Generate Documentation for Source File (Priority: P1) 🎯 MVP

**Goal**: Automatically generate a comprehensive documentation file for a given source code file.

**Independent Test**: Can be tested by providing a single Python file (e.g., `src/main.py`) and asserting that a corresponding Markdown file (e.g., `docs/src/main.md`) is created with the correct content structure.

### Tests for User Story 1

- [ ] T013 [US1] Write RED unit tests for `src/document_generator/markdown.py` (e.g., rendering structured JSON to Markdown, file writing) in `tests/unit/document_generator/test_markdown.py`.
- [ ] T014 [US1] Write RED unit tests for core `Agent` logic (e.g., prompt construction, parsing LLM output) in `tests/unit/document_generator/test_agent.py`.
- [ ] T015 [US1] Write RED integration tests for the `DocumentGeneratorEngine` (orchestration of a single file) in `tests/integration/test_doc_generation_flow.py`.

### Implementation for User Story 1

- [ ] T016 [US1] Implement Markdown rendering and file writing logic in `src/document_generator/markdown.py`.
- [ ] T017 [US1] Implement core AI agent interaction (prompt construction for `GeneratedDocumentation` structure) in `src/document_generator/agent.py`.
- [ ] T018 [US1] Implement file reading logic in `src/document_generator/engine.py`.
- [ ] T019 [US1] Implement orchestration in `src/document_generator/engine.py` to:
    - Accept `CodeAnalysisResult`.
    - Iterate through files.
    - Read raw file content.
    - Call the AI agent to generate documentation.
    - Use Markdown writer to save the output to `docs/` mirroring source structure.
    - Handle `ProcessingResult` and `BatchGenerationResult`.
- [ ] T020 [US1] Add a new endpoint `POST /generate` to `src/api/routes.py` that accepts `CodeAnalysisResult` and returns `BatchGenerationResult`, integrating with `DocumentGeneratorEngine`.

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Context-Aware Generation (Priority: P2)

**Goal**: Documentation reflects the broader project context.

**Independent Test**: Create a file that imports a class from another module. Run the engine. Check if the output documentation correctly references the imported class's origin or context.

### Tests for User Story 2

- [ ] T021 [US2] Write RED unit tests for `Agent` logic that verifies project context is properly included in the prompt and utilized for context-aware generation in `tests/unit/document_generator/test_agent.py`.

### Implementation for User Story 2

- [ ] T022 [US2] Modify `src/document_generator/agent.py` to include `Project Structure` from `CodeAnalysisResult` in the system prompt.
- [ ] T023 [US2] Refine `src/document_generator/agent.py`'s prompt construction to leverage project context for generating accurate cross-references and explanations.

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Handle Large Files with Structured Output (Priority: P2)

**Goal**: Successfully document large files without crashing or truncating the output.

**Independent Test**: Provide a large source file (e.g., >500 lines). Run the engine. Assert that the output Markdown is complete (ends with the expected footer/sections) and is valid JSON/Markdown structure.

### Tests for User Story 3

- [ ] T024 [US3] Write RED unit tests in `tests/unit/document_generator/test_agent.py` to simulate Context Window Overflow and verify graceful handling (truncation, warning).
- [ ] T025 [US3] Write RED unit tests in `tests/unit/document_generator/test_agent.py` to simulate malformed JSON output from the LLM and verify retry/raw file saving.

### Implementation for User Story 3

- [ ] T026 [US3] Implement Context Window Overflow handling in `src/document_generator/agent.py` (first dropping project context, then truncating file content if necessary).
- [ ] T027 [US3] Implement retry mechanism for LLM calls in `src/document_generator/agent.py` (rate limits, transient errors).
- [ ] T028 [US3] Implement malformed JSON output handling in `src/document_generator/agent.py` (retry once, then save raw output to `.raw` file).

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Skip Trivial Files (Priority: P3)

**Goal**: Skip generating documentation for empty or trivial files.

**Independent Test**: Provide an empty file or a file with only imports. Run the engine. Assert that NO output file is created (or a log entry is made).

### Tests for User Story 4

- [ ] T029 [US4] Write RED unit tests in `tests/unit/document_generator/test_engine.py` for trivial file detection logic.

### Implementation for User Story 4

- [ ] T030 [US4] Implement trivial file detection logic in `src/document_generator/engine.py` (based on `elements` list from `FileAnalysis` and file size).
- [ ] T031 [US4] Modify `src/document_generator/engine.py` to skip processing and log when a trivial file is detected.

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T032 Refactor and clean up `src/document_generator/` modules for better readability and adherence to DRY principles.
- [ ] T033 Implement robust logging across all `src/document_generator/` modules.
- [ ] T034 Ensure all functions, classes, and methods in `src/document_generator/` have appropriate type hints and docstrings.
- [ ] T035 Update `pyproject.toml` with any new dependencies and ensure `uv` is configured correctly.
- [ ] T036 Review and update `quickstart.md` with final API usage and any necessary setup steps.
- [ ] T037 Run `ruff` and `black` to ensure code style compliance in `src/document_generator/`.
- [ ] T038 Review all generated documentation for consistency and quality (manual check).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 components (e.g. prompt construction) but should be independently testable for its core feature.
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Independent from other stories for its core feature (error handling, retries).
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Independent from other stories for its core feature (trivial file detection).

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T001-T007) can run in parallel.
- Foundational tasks T008-T012 can be implemented once models are defined.
- Once Foundational phase completes, User Stories 1, 2, 3, and 4 can technically start in parallel (if team capacity allows), though sequential by priority is recommended.
- Within User Story 1, tasks T013-T015 (tests) can be started in parallel, then T016-T020 (implementation) can be started in parallel or sequentially based on internal dependencies.
- Similarly for other user stories, test tasks can be parallel, then implementation tasks.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
