---
id: 0001
title: Update project constitution and dependent files
stage: constitution
date: 2025-11-20
surface: agent
model: gemini-pro
feature: none
branch: main
user: hubaib
command: /sp.constitution
labels: [constitution, refactor]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .gemini/commands/sp.tasks.toml
tests:
 - none
---

## Prompt

/sp.constitution 

Project principles and standards:
- Write tests first (TDD approach)
- Use Python 3.12+ with type hints everywhere
- Keep code clean and easy to read
- Document important decisions with ADRs
- Follow essential OOP principles: SOLID, DRY, KISS
- All functions must include type hints on parameters and return types
  - Example: `def add(a: float, b: float) -> float:`
- All functions must include docstrings explaining what they do
  - Example: `"""Add two numbers and return the sum."""`
- Follow PEP 8 naming conventions (lowercase_with_underscores for functions)
- Lines must be under 100 characters
- No magic numbers; use named constants
  - Bad: `if x > 10:`
  - Good: `if x > MAX_POWER_EXPONENT:`

Technical stack:
- Python 3.12+ with UV package manager

Quality requirements:
- All tests must pass
- At least 80% code coverage
- Use dataclasses for data structures

## Response snapshot

The project constitution was updated to reflect new principles and standards. Dependent files were also updated to ensure consistency.

## Outcome

- ✅ Impact: The project constitution was updated to reflect new principles and standards. Dependent files were also updated to ensure consistency.
- 🧪 Tests: none
- 📁 Files: 3 files modified.
- 🔁 Next prompts: none
- 🧠 Reflection: It's important to keep the constitution and dependent files in sync to avoid inconsistencies.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): none
