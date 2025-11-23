---
id: 0013
title: enable-documentation-file-saving-to-disk
stage: bugfix
date: 2025-11-24
surface: agent
model: gemini-2.5-flash
feature: 002-ai-processing-engine
branch: main
user: user
command: replace
labels: [bugfix, file-management, workflow]
links: null
files_yaml:
 - src/api/routes.py
tests_yaml: []
---

# User Prompt

<User reported that the workflow was not saving files, after previous issues were resolved.>

# Assistant Response

The user's crucial feedback indicated that despite all previous fixes to the Markdown content generation and formatting, the generated documentation files were not being saved to disk. This explained why the user was resorting to manual copy-pasting from console logs, which introduced formatting issues.

Upon investigation, it was discovered that the `DocumentGeneratorEngine.generate_documentation` method was being called with `write_to_disk=False` in `src/api/routes.py` within the `run_processing_in_background` function. This explicitly prevented the saving of files.

The following action was taken:
1.  **Modify `src/api/routes.py`:** The `write_to_disk` parameter in the call to `engine.generate_documentation` was changed from `False` to `True`.
2.  **Specify Output Directory:** The `output_dir` parameter was set to `Path("generated_docs")`. The `write_markdown_to_file` function in `src/document_generator/markdown.py` (which is part of the execution chain) will automatically create this directory and any necessary subdirectories if they do not exist. Generated files will now be saved in a `generated_docs` folder at the project root.

This change directly addresses the workflow issue, ensuring that the correctly formatted Markdown documentation is now persisted to disk.
