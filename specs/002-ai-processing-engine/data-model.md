# Data Model: AI Processing Engine

This document defines the data structures for the AI Processing Engine.

## Core Entities

### `DocumentJob`
Represents a single file processing task.

| Field          | Type                  | Description                                        |
|----------------|-----------------------|----------------------------------------------------|
| `file_path`    | `str`                 | Relative path to the source file.                  |
| `content`      | `str`                 | Raw content of the file.                           |
| `context`      | `dict`                | Project context (file tree, related modules).      |
| `analysis`     | `FileAnalysis`        | The static analysis data for this file (from Step 1). |

### `GeneratedDocumentation`
The structured output from the AI Agent (before saving).

| Field          | Type                  | Description                                        |
|----------------|-----------------------|----------------------------------------------------|
| `summary`      | `str`                 | High-level overview of the file.                   |
| `api_reference`| `str`                 | Detailed API documentation (classes, functions).   |
| `examples`     | `str`                 | Usage examples.                                    |

### `ProcessingResult`
The result of processing a single file.

| Field          | Type                  | Description                                        |
|----------------|-----------------------|----------------------------------------------------|
| `file_path`    | `str`                 | The source file path.                              |
| `doc_path`     | `str`                 | The path where documentation was saved.            |
| `status`       | `str`                 | "success", "skipped", "failed".                    |
| `error`        | `str | None`          | Error message if failed.                           |

### `BatchGenerationResult`
The aggregate result of the entire generation process.

| Field          | Type                  | Description                                        |
|----------------|-----------------------|----------------------------------------------------|
| `total_files`  | `int`                 | Total files considered.                            |
| `processed`    | `int`                 | Number of files successfully processed.            |
| `skipped`      | `int`                 | Number of files skipped.                           |
| `failed`       | `int`                 | Number of files failed.                            |
| `results`      | `list[ProcessingResult]` | Detailed results for each file.                 |
