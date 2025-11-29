---
id: 0034
title: fix-registration-flow-and-user-name-display
stage: bugfix
date: 2025-11-29
surface: agent
model: gemini-2.0-flash-thinking-exp-1219
feature: 002-ai-processing-engine
branch: main
user: user
command: sp.implement
labels: ["auth", "frontend", "backend", "ux", "bugfix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - src/models/auth.py
 - src/api/auth.py
 - docugen-ai/services/apiService.ts
 - docugen-ai/components/LoginScreen.tsx
tests:
 - npx tsc --noEmit (Passed)
---

## Prompt

Just noticed one bug, when I register an account, After Signed in as text it shows full name but when I log in it shows email after Signed in as text. Also, after registering, it should take to login page to log in instead of taking directly into dashboard

## Response snapshot

Fixed two bugs related to authentication flow and user name display:

1.  **Inconsistent User Name Display:**
    *   Modified `src/api/auth.py` to make `login_for_access_token` return a `user_name` field (representing the user's full name or username) alongside the token.
    *   Updated `src/models/auth.py` to define `TokenWithUser` model.
    *   Modified `docugen-ai/services/apiService.ts` to extract this `user_name` from the login response.
    *   Updated `docugen-ai/components/LoginScreen.tsx` to pass this `user_name` to `onLoginSuccess`. `App.tsx` now consistently displays the user's full name (or username).

2.  **Registration Flow:**
    *   Modified `docugen-ai/services/apiService.ts` to remove the implicit login after registration.
    *   Modified `docugen-ai/components/LoginScreen.tsx` to, after successful registration, clear the form, set `isRegistering` to `false` (to display the login form), and show a success message prompting the user to log in explicitly.

## Outcome

- ✅ Impact: Resolved inconsistencies in user name display and corrected the registration flow to improve user experience.
- 🧪 Tests: Frontend type checks (`tsc --noEmit`) passed successfully.
- 📁 Files: Modified `src/models/auth.py`, `src/api/auth.py`, `docugen-ai/services/apiService.ts`, and `docugen-ai/components/LoginScreen.tsx`.
- 🔁 Next prompts: Continue debugging the "Connection Lost" issue.
- 🧠 Reflection: Ensuring a clear and consistent authentication flow is critical for user experience. The changes now provide a more intuitive registration and login process.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
