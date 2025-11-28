---
id: 0028
title: Block Placeholder URLs
stage: green
date: 2025-11-27
surface: agent
model: gemini-2.0-flash
feature: 002-ai-processing-engine
branch: main
user: user
command: replace
labels: ["ux", "validation", "frontend"]
links:
  spec: specs/002-ai-processing-engine/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - docugen-ai/components/InputSection.tsx
tests:
  - Manual verification
---

## Prompt

But it shouldn't do any processing when user input urls like "https://github.com/user/repo" or should it?

## Response snapshot

The user pointed out that the system should not attempt to process obvious placeholder URLs (like `https://github.com/user/repo`).
Updated `docugen-ai/components/InputSection.tsx` to explicitly reject:
- `https://github.com/user/repo`
- `https://github.com/username/repository`
This prevents unnecessary backend calls for inputs that are clearly invalid/default examples.

## Outcome

- ✅ Impact: Improved UX by providing immediate feedback when users accidentally submit the placeholder text. Reduced backend noise.
- 🧪 Tests: Manual verification logic implemented.
- 📁 Files: Modified `docugen-ai/components/InputSection.tsx`.
- 🔁 Next prompts: None immediate.
- 🧠 Reflection: Catching "dumb" errors (like submitting the placeholder) is a key part of a polished user experience.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
