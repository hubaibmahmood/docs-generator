---
id: 0007
title: fix-await-runresultstreaming-error
stage: bugfix
date: 2025-11-24
surface: agent
model: gemini-2.0-flash-exp
feature: 002-ai-processing-engine
branch: 002-ai-processing-engine
user: user
command: fix the runtime error 'object RunResultStreaming can't be used in 'await' expression'
labels: [bugfix, async, agent, testing]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - src/document_generator/agent.py
 - tests/unit/document_generator/test_agent.py
tests:
 - tests/unit/document_generator/test_agent.py
---

## Prompt

2025-11-24 00:36:31,549 - src.document_generator.agent - ERROR - Error generating documentation for file_modification_checking.py: object RunResultStreaming can't be used in 'await' expression

## Response snapshot

I investigated the error and determined that `Runner.run_streamed` is a synchronous method that returns a `RunResultStreaming` object, which was incorrectly being awaited.

I fixed this by removing the `await` keyword from the `Runner.run_streamed` call in `src/document_generator/agent.py`.

I also updated the unit tests in `tests/unit/document_generator/test_agent.py` to use `MagicMock` instead of `AsyncMock` for `Runner.run_streamed`, reflecting its synchronous nature.

Verified the fix by running the updated unit tests and the full test suite, all of which passed.

## Outcome

- ✅ Impact: Fixed a runtime error preventing document generation.
- 🧪 Tests: 39 passed
- 📁 Files: Modified 2 files.
- 🔁 Next prompts: Continue with usage or further testing.
- 🧠 Reflection: When using third-party libraries, especially those with similar names to async patterns, it's crucial to verify if they are actually awaitable. The error message was clear, but the assumption that "client calls are async" led to the initial bug.

## Evaluation notes (flywheel)

- Failure modes observed: Incorrect use of `await` on synchronous method.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
