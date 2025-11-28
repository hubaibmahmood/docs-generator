---
id: 0025
title: Implement SSRF Protection
stage: green
date: 2025-11-27
surface: agent
model: gemini-2.0-flash
feature: 002-ai-processing-engine
branch: main
user: user
command: replace
labels: ["security", "ssrf", "backend", "cleanup"]
links:
  spec: specs/002-ai-processing-engine/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/analysis/repository.py
  - src/api/routes.py
tests:
  - Manual verification
---

## Prompt

I gave it "http://169.254.169.254/latest/meta-data/" input and it started processing and even tried multiple times. This is the console log:
...
fatal: unable to access 'http://169.254.169.254/latest/meta-data/': Failed to connect to 169.254.169.254 port 80 after 75003 ms: Couldn't connect to server
...
FileNotFoundError: [Errno 2] No such file or directory: '/var/folders/kl/ztn29n8x4mb9txdt_q_7vvzr0000gn/T/tmp4p19s9u5'

## Response snapshot

Updated `src/analysis/repository.py` to implement robust SSRF (Server-Side Request Forgery) protection.
- Added logic to resolve the hostname from the repository URL to an IP address.
- Validates the resolved IP against a list of blocked private/reserved ranges (loopback, link-local, private networks).
- Raises a `RepositoryError` if a blocked IP is detected.

Updated `src/api/routes.py` to fix the `FileNotFoundError` during cleanup.
- Wrapped `shutil.rmtree` calls in `try...except` blocks to safely handle cases where the temporary directory might not exist (e.g., if `git clone` failed before creating it or cleaned it up itself).

## Outcome

- ✅ Impact: Prevented the application from accessing internal network resources (like AWS metadata service) via malicious URLs. enhanced stability by handling cleanup errors gracefully.
- 🧪 Tests: Manual verification logic implemented.
- 📁 Files: Modified `src/analysis/repository.py` and `src/api/routes.py`.
- 🔁 Next prompts: None immediate.
- 🧠 Reflection: SSRF is a critical vulnerability in any application that fetches resources from URLs provided by users. DNS resolution and IP checking are standard defenses.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
