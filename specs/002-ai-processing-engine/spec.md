# Feature Specification: AI Processing Engine

**Feature Branch**: `002-ai-processing-engine`
**Created**: 2025-11-23
**Status**: Draft
**Input**: User description: "Implement Step 2: AI Processing Engine to generate documentation from code using OpenAI Agents SDK and Gemini 2.5 Flash."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Documentation for Source File (Priority: P1)

As a developer, I want the system to automatically generate a comprehensive documentation file for a given source code file, so that I don't have to write boilerplate documentation manually.

**Why this priority**: This is the core functionality of the engine. Without this, no documentation is produced.

**Independent Test**: Can be tested by providing a single Python file (e.g., `src/main.py`) and asserting that a corresponding Markdown file (e.g., `docs/src/main.md`) is created with the correct content structure.

**Acceptance Scenarios**:

1.  **Given** a valid source code file path from the Step 1 analysis, **When** the engine processes it, **Then** it MUST read the raw content from disk.
2.  **Given** the raw content, **When** the Agent processes it, **Then** it MUST generate a single Markdown file containing an Overview, API Reference, and Usage Examples.
3.  **Given** the generated content, **When** saving, **Then** it MUST be written to a `docs/` directory structure that mirrors the source directory.

### User Story 2 - Context-Aware Generation (Priority: P2)

As a developer, I want the documentation to reflect the broader project context (e.g., knowing where a class is defined), so that the generated examples and explanations are accurate and linked correctly.

**Why this priority**: Increases the quality and accuracy of the documentation, preventing "hallucinations" about missing dependencies.

**Independent Test**: Create a file that imports a class from another module. Run the engine. Check if the output documentation correctly references the imported class's origin or context.

**Acceptance Scenarios**:

1.  **Given** a file that depends on other project modules, **When** the Agent analyzes it, **Then** it MUST have access to the Project Structure (from Step 1) in its system prompt.
2.  **Given** the context, **When** generating the Overview, **Then** the Agent MUST correctly identify relationships (e.g., "Inherits from BaseController defined in...").

### User Story 3 - Handle Large Files with Structured Output (Priority: P2)

As a developer, I want the system to successfully document large files without crashing or truncating the output, so that complex modules are fully documented.

**Why this priority**: Reliability. Real-world projects have large files that can break simple LLM calls.

**Independent Test**: Provide a large source file (e.g., >500 lines). Run the engine. Assert that the output Markdown is complete (ends with the expected footer/sections) and is valid JSON/Markdown structure.

**Acceptance Scenarios**:

1.  **Given** a large source file, **When** the Agent processes it, **Then** it MUST return the full documentation without truncation (potentially using a specific "Monolith" prompt strategy).
2.  **Given** the output, **When** validated, **Then** it MUST contain all required sections (Overview, API, Examples).

### User Story 4 - Skip Trivial Files (Priority: P3)

As a user, I want the system to skip generating documentation for empty or trivial files (like `__init__.py` with no logic), so that the documentation folder isn't cluttered with useless files.

**Why this priority**: Usability and cleanliness of the output.

**Independent Test**: Provide an empty file or a file with only imports. Run the engine. Assert that NO output file is created (or a log entry is made).

**Acceptance Scenarios**:

1.  **Given** a trivial file (e.g., empty `__init__.py`), **When** the Agent analyzes it, **Then** it MUST determine it is "skippable" and NOT produce a documentation file.

### Edge Cases

- What happens if the API key is invalid? The system should fail gracefully and report an auth error.
- What happens if the source file is deleted after Step 1 analysis but before Step 2 processing? The system should log a "File not found" error and continue to the next file.
- What happens if the LLM returns malformed Markdown? The system should attempt to save it as-is but log a warning, or retry the generation.
- What happens if the file contains non-text content (binary) that wasn't caught in Step 1? The system should catch the read error and skip the file.

## Requirements *(mandatory)*

#
## Clarifications

### Session 2025-11-23
- Q: How should files be processed regarding concurrency? → A: Sequential Async: Process files one by one using async IO.
- Q: What happens if a single file fails during batch processing? → A: Continue Processing: Log the error and continue with remaining files.
- Q: How strictly should we handle invalid JSON output from the Agent? → A: Retry then Raw: Retry once. If still invalid JSON, save the raw text output to a file (e.g., `.md.raw`) and log a warning.
- Q: What level of schema validation is required for `analysis.json`? → A: Full JSON Schema Validation: Validate the entire JSON structure, including nested fields and types, against a predefined schema.

### Functional Requirements

- **FR-001**: The system MUST utilize an AI Agent architecture to orchestrate the document generation process.
- **FR-002**: The system MUST connect to a high-capacity Large Language Model (LLM) capable of processing large code files (1M+ token context).
- **FR-003**: The system MUST accept the structural analysis data (from the previous step) and perform **Full JSON Schema Validation** against a predefined schema before processing.
- **FR-004**: For each target file, the system MUST read the **raw source code** directly from the file system.
- **FR-005**: The Agent MUST be prompted to generate a **Structured JSON** output containing fields for: 1) High-level Summary, 2) API Reference, and 3) Usage Examples. The system MUST then render this JSON into the final Markdown format.
- **FR-006**: The Agent MUST be provided with the Project Structure (from the analysis step) to ensure context-aware documentation.
- **FR-007**: The system MUST write the generated documentation to a documentation directory that mirrors the source file's directory structure.
- **FR-008**: The generated output MUST use standard formatting syntax (e.g., Markdown) and include syntax highlighting for all code snippets.
- **FR-009**: The system MUST implement logic to detect and skip "trivial" files (e.g., empty files or files with minimal logic) to prevent clutter.
- **FR-010**: The system MUST handle API availability issues (e.g., rate limits) with a retry mechanism.
- **FR-011**: The system MUST handle Context Window Overflow by first dropping project context, and then truncating the input file if necessary (logging a warning).
- **FR-012**: The system MUST handle Model Refusals (Safety/Policy) by generating a placeholder file indicating the blockage, rather than crashing.
- **FR-013**: The system MUST process files sequentially using asynchronous I/O, ensuring ordered processing.
- **FR-014**: The system MUST implement "continue-on-error" logic, ensuring that a failure in processing one file does NOT stop the processing of subsequent files; failures MUST be logged.
- **FR-015**: The system MUST handle invalid JSON output from the Agent by retrying once; if still invalid, the raw text output MUST be saved to a `.raw` file and a warning logged.

### Constraints

- **Tech Stack**: The implementation MUST use the `openai-agents-python` SDK.
- **Model Provider**: The implementation MUST use the `gemini-2.5-flash` model via the Google Generative Language API (compatible endpoint).
- **Output Format**: The output files MUST be in Markdown (`.md`) format.

### Key Entities

- **Document Job**: Represents the task of processing one file. Contains `file_path`, `context_data`.
- **Agent Context**: The prompt payload, including System Instructions, Project Context, and Raw Source Code.
- **Doc Artifact**: The resulting content and its destination path.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001 (Completeness)**: 100% of non-trivial source files identified in the analysis step have a corresponding documentation file in the output directory.
- **SC-002 (Structure Validity)**: 100% of generated documentation files contain the three required sections ("Overview", "API Reference", "Usage Examples").
- **SC-003 (Formatting Compliance)**: 100% of code snippets in the output are wrapped in correct syntax-highlighting blocks.
- **SC-004 (Internal Link Resolution)**: > 95% of internal file references (if any) in generated documentation resolve to valid paths within the documentation or source tree.
- **SC-005 (Performance)**: The system MUST process 95% of files (under 2000 lines) within 60 seconds per file.