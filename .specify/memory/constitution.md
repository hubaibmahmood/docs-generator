# Document Generator Constitution

<!-- 
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- List of modified principles: none
- Added sections
  - Principles
  - Technical Stack
  - Quality Requirements
  - Governance
- Removed sections: none
- Templates requiring updates: none
- Follow-up TODOs: none
-->

## Core Principles

### I. Test-Driven Development
Write tests first (TDD approach).

### II. Python 3.12+ with Type Hints
Use Python 3.12+ with type hints everywhere.

### III. Clean and Readable Code
Keep code clean and easy to read.

### IV. Document with ADRs
Document important decisions with ADRs.

### V. SOLID, DRY, KISS
Follow essential OOP principles: SOLID, DRY, KISS.

### VI. Function contracts
- All functions must include type hints on parameters and return types
  - Example: `def add(a: float, b: float) -> float:`
- All functions must include docstrings explaining what they do
  - Example: `"""Add two numbers and return the sum."""`

### VII. PEP 8 and Line Length
- Follow PEP 8 naming conventions (lowercase_with_underscores for functions)
- Lines must be under 100 characters

### VIII. No Magic Numbers
- No magic numbers; use named constants
  - Bad: `if x > 10:`
  - Good: `if x > MAX_POWER_EXPONENT:`

## Technical Stack
Python 3.12+ with UV package manager

## Quality Requirements
- All tests must pass
- At least 80% code coverage
- Use dataclasses for data structures

## Governance
This Constitution is the single source of truth for all software development practices within this project. It is a living document that can be amended through the process defined below. All team members are expected to adhere to these principles and standards.

### Amendment Process
1.  **Proposal:** Any team member can propose an amendment by creating an Architecture Decision Record (ADR) that details the change, its rationale, and its impact.
2.  **Review:** The proposed ADR will be reviewed by the project's technical leadership.
3.  **Approval:** If approved, the ADR is merged, and this Constitution is updated accordingly. The version number will be incremented based on the nature of the change (MAJOR for breaking changes, MINOR for new principles, PATCH for clarifications).
4.  **Communication:** All changes to the Constitution will be communicated to the entire team.

### Compliance
- Code reviews must verify compliance with this Constitution.
- Automated tooling (e.g., linters, static analyzers) will be used to enforce these standards wherever possible.
- Deviations from this Constitution require an approved ADR.

**Version**: 1.0.0 | **Ratified**: 2025-11-20 | **Last Amended**: 2025-11-20