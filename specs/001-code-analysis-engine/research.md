# Research for Code Analysis Engine

This document records the key technical decisions made during the planning phase for the Code Analysis Engine, based on the requirements in `spec.md` and the principles in `constitution.md`.

## 1. Code Parsing Strategy

### NEEDS CLARIFICATION
The specification requires parsing multiple languages (Python, Java, JavaScript, C) to extract code elements. The built-in Python `ast` module only supports Python. A more robust, multi-language solution is needed.

### Decision
We will use the **`tree-sitter`** parsing framework.

### Rationale
- **Multi-Language Support**: `tree-sitter` has a wide range of high-quality grammars for many languages, including all those required by the specification.
- **Resilience**: It is designed to build a concrete syntax tree even if the source code contains syntax errors, which directly supports functional requirement **FR-010**.
- **Performance**: `tree-sitter` is known for its high performance, which will be beneficial for analyzing large repositories.
- **Ecosystem**: It has Python bindings (`tree-sitter-python`) that allow easy integration into our Python-based application.

### Alternatives Considered
- **Multiple `ast` Libraries**: Using a separate AST library for each language (e.g., `ast` for Python, `esprima` for JavaScript, etc.). This was rejected due to the complexity of managing multiple dependencies and learning different APIs for each, which would violate the "KISS" principle.
- **Regular Expressions**: Using regex to find functions and classes. This is notoriously brittle, unreliable, and cannot handle complex syntax or errors gracefully. It would fail to meet the accuracy requirements (**SC-005**).

## 2. Git Repository Cloning

### NEEDS CLARIFICATION
The system must clone a remote GitHub repository into a temporary directory for analysis (**FR-002**). A reliable method for handling this within a Python application is required.

### Decision
We will use the **`GitPython`** library.

### Rationale
- **Full Git Functionality**: `GitPython` provides a comprehensive, object-oriented interface to a local git repository. It can be used to clone remote repositories, check out branches, and manage the repository lifecycle.
- **Maturity and Stability**: It is a widely-used and well-maintained library for git operations in Python.
- **Error Handling**: It provides clear exceptions for common git failures (e.g., `GitCommandError`), which will help in implementing the retry logic and specific error reporting required by the edge case analysis.

### Alternatives Considered
- **`subprocess` with `git` CLI**: Directly calling the `git` command-line tool using Python's `subprocess` module. While feasible, this approach is more complex to manage, requires manual parsing of `stdout`/`stderr`, and is less platform-independent than using a dedicated library like `GitPython`.
