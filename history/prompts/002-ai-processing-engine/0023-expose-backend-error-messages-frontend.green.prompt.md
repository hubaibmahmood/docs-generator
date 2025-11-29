---
id: 0023
title: Expose Backend Error Messages to Frontend
stage: green
date: 2025-11-27
surface: agent
model: gemini-2.0-flash
feature: 002-ai-processing-engine
branch: main
user: user
command: replace
labels: ["frontend", "error-handling", "ux", "api"]
links:
  spec: specs/002-ai-processing-engine/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - docugen-ai/services/apiService.ts
  - docugen-ai/App.tsx
tests:
  - npm run build
---

## Prompt

I tested Command Injection & Shell Metacharacters and it just says Analysis Failed. On the console it does say "Repository error: Invalid repository URL. Contains illegal characters." Can we make errors show a bit more context so the user know we have security in place

## Response snapshot

Updated `apiService.ts` to include the `errors` field in the `getStatus` response type.
Modified `App.tsx` to extract the specific error message from the backend response when the status is `FAILED` and display it to the user instead of a generic "Analysis Failed".
Verified with a clean build.

## Outcome

- ✅ Impact: Users now see specific backend error messages (e.g., "Invalid repository URL..."), providing better context and confirming security validations are active.
- 🧪 Tests: Verified via code review and successful build.
- 📁 Files: Modified `apiService.ts` and `App.tsx`.
- 🔁 Next prompts: None immediate.
- 🧠 Reflection: Propagating specific error messages improves transparency and trust, especially when security validations reject an input.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
