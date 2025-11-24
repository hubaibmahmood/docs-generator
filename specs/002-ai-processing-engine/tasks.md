# Implementation Tasks: Cohesive Documentation Generation

**Feature**: `002-ai-processing-engine`
**Based on Plan**: `specs/002-ai-processing-engine/plan.md`

## Task List

- [ ] **Task 1: Update Data Models** <!-- id: 0 -->
    - Modify `src/models/doc_gen.py`.
    - Deprecate or Remove `GeneratedDocumentation` (the strict 3-field JSON).
    - Create `DocumentationSection` (enum or class) for the types (README, API, etc.).
    - Create `SectionJob` model.

- [ ] **Task 2: Implement Context Strategies** <!-- id: 1 -->
    - Create `src/document_generator/strategies.py`.
    - Implement `BaseStrategy` with `gather_context(analysis)` and `prompt_template`.
    - Implement concrete strategies:
        - `ReadmeStrategy`
        - `ArchitectureStrategy`
        - `ApiStrategy` (filter for routes)
        - `ModelsStrategy` (filter for classes)
        - `ServicesStrategy`
        - `GettingStartedStrategy`

- [ ] **Task 3: Update AI Agent** <!-- id: 2 -->
    - Modify `src/document_generator/agent.py`.
    - Change `doc_gen_agent` instructions to be generic "Technical Writer".
    - Remove the strict `output_type=GeneratedDocumentation` constraint (switch to `str` or a simple `MarkdownOutput`).
    - Update `generate_documentation_from_job` to handle `SectionJob`.

- [ ] **Task 4: Refactor Engine** <!-- id: 3 -->
    - Modify `src/document_generator/engine.py`.
    - Replace file-iteration loop with `Strategy` iteration loop.
    - `generate_documentation` should yield a result for each Strategy.

- [ ] **Task 5: Verify & Clean Up** <!-- id: 4 -->
    - Update `src/api/routes.py` (or wherever the engine is called) if the signature changed.
    - Run manual test on the repo itself.