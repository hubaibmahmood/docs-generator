---
id: 0005
title: Update GitHub login to Coming Soon
stage: general
date: 2025-11-30
surface: agent
model: gemini-cli-agent
feature: none
branch: main
user: agent
command: "replace(file_path='docugen-ai/components/LoginScreen.tsx', instruction='Update the GitHub login button text to include \"(Coming Soon)\" since the feature is not yet implemented.', new_string='            <Github className=\"w-5 h-5\" />\n            GitHub (Coming Soon)\n          </button>', old_string='            <Github className=\"w-5 h-5\" />\n            GitHub\n          </button>')"
labels: ["UI", "Frontend", "Login", "Enhancement"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - docugen-ai/components/LoginScreen.tsx
tests:
---

## Prompt

Also, at the moment our login page we have github option under or continue with section. Lets make it coming soon as it's not implemented yet

## Response snapshot

````
I have read the `LoginScreen.tsx` file.

The GitHub login button is located here:

```typescript
          <button
            type="button"
            onClick={handleSocialLogin}
            disabled={isLoading}
            className="w-full bg-white text-slate-900 font-bold py-3 rounded-xl flex items-center justify-center gap-3 hover:bg-slate-50 transition-colors disabled:opacity-50"
          >
            <Github className="w-5 h-5" />
            GitHub
          </button>
```

To indicate "Coming Soon" for GitHub, I will modify the text inside the button. I want to replace "GitHub" with "GitHub (Coming Soon)". I will use the `replace` tool for this.
````
Successfully modified file: /Users/mac/Documents/PIAIC/speckit plus/document-generator/docugen-ai/components/LoginScreen.tsx (1 replacements).

## Outcome

- ✅ Impact: The GitHub login option on the login page now clearly indicates it is "Coming Soon" to users, setting correct expectations and avoiding confusion about unimplemented functionality.
- 🧪 Tests: N/A (Manual visual verification is sufficient for this UI text change).
- 📁 Files: One file modified: `docugen-ai/components/LoginScreen.tsx`.
- 🔁 Next prompts: The immediate task of updating the GitHub login option is complete.
- 🧠 Reflection: Successfully updated the UI to reflect the availability status of a feature. This process highlighted the importance of accurate communication regarding feature readiness.

## Evaluation notes (flywheel)

- Failure modes observed: Initially misused the PHR creation script by providing an incorrect feature argument for a 'general' stage prompt, leading to a script error. This was corrected by consulting the script's usage instructions and understanding the distinction between feature-specific and general prompts.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
