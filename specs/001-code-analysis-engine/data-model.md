# Data Model: Code Analysis Engine

This document defines the data structures for the JSON output of the Code Analysis Engine. These structures will be implemented as Python dataclasses in `src/models/analysis.py`, ensuring type safety and consistency as per the project's constitution.

## Top-Level Object

### `CodeAnalysisResult`
The main object returned by the analysis service.

| Field           | Type                     | Description                                                              |
|-----------------|--------------------------|--------------------------------------------------------------------------|
| `file_tree`     | `dict[str, object]`      | A nested dictionary representing the file and directory structure.         |
| `file_analysis` | `dict[str, FileAnalysis]`| A dictionary mapping file paths to their detailed analysis.              |
| `errors`        | `list[AnalysisError]`    | A list of errors that occurred during the analysis of specific files.    |

---

## Core Entities

### `FileAnalysis`
Contains the detailed analysis for a single file.

| Field             | Type                    | Description                                                              |
|-------------------|-------------------------|--------------------------------------------------------------------------|
| `file_path`       | `str`                   | The full path to the file within the repository.                         |
| `file_type`       | `str`                   | The identified type of the file (e.g., "Python", "JavaScript", "Config"). |
| `language`        | `str`                   | The primary programming language of the file (e.g., "Python").           |
| `elements`        | `list[ExtractedElement]`| A list of code elements (classes, functions) extracted from the file.    |
| `dependencies`    | `list[Dependency]`      | A list of dependencies extracted from files like `requirements.txt`.     |
| `is_binary`       | `bool`                  | `True` if the file is detected as binary or has an unknown encoding.     |

### `AnalysisError`
Represents a failure to parse a specific file.

| Field       | Type    | Description                                             |
|-------------|---------|---------------------------------------------------------|
| `file_path` | `str`   | The path to the file that could not be parsed.          |
| `error`     | `str`   | A message describing the syntax error or other failure. |

---

## Extracted Elements

### `ExtractedElement` (Union Type)
A union of `FunctionElement`, `ClassElement`, and other future element types.

### `FunctionElement`
Represents a standalone function.

| Field         | Type          | Description                                    |
|---------------|---------------|------------------------------------------------|
| `name`        | `str`         | The name of the function.                      |
| `docstring`   | `str | None`  | The function's docstring, if present.          |
| `return_type` | `str | None`  | The return type annotation, if present.        |
| `methods`     | `list[MethodElement]` | List of methods within the function. |


### `ClassElement`
Represents a class.

| Field       | Type                  | Description                             |
|-------------|-----------------------|-----------------------------------------|
| `name`      | `str`                 | The name of the class.                  |
| `docstring` | `str | None`          | The class-level docstring, if present.  |
| `methods`   | `list[MethodElement]` | A list of methods defined in the class. |

### `MethodElement`
Represents a method within a class.

| Field         | Type         | Description                              |
|---------------|--------------|------------------------------------------|
| `name`        | `str`        | The name of the method.                  |
| `docstring`   | `str | None` | The method's docstring, if present.      |
| `return_type` | `str | None` | The return type annotation, if present.  |

### `Dependency`
Represents a single dependency from a manifest file.

| Field               | Type         | Description                                        |
|---------------------|--------------|----------------------------------------------------|
| `package_name`      | `str`        - The name of the package or library.                  |
| `version_specifier` | `str | None` | The version string (e.g., "==1.2.3", "^4.0").      |
| `source_file`       | `str`        | The manifest file where this dependency was found. |
