# Contributing to AIOps Self-Healing E-Commerce Platform

This repository follows strict team governance to prevent merge conflicts, security issues, and architectural drift. Every developer (and AI assistant) must adhere to the processes detailed below.

---

## 1. Task Declaration Template
Before creating a branch or writing code, declare your task as a GitHub Issue using this template:

```markdown
### TASK DECLARATION
- **OWNER**: [Rudra / Saurav / Taranay / Vivek]
- **TASK**: [Short description of feature, bug fix, or investigation]
- **ALLOWED PATHS**: [e.g. apps/ai-worker/**, tests/ai_worker/**]
- **FORBIDDEN PATHS**: [e.g. apps/api/**, apps/web/**, infrastructure/**]
- **ACCEPTANCE CRITERIA**:
  1. [Criteria 1]
  2. [Criteria 2]
```

---

## 2. Branching & PR Rules
* **No Direct Commits to `main`**: All work must be developed on a dedicated feature or fix branch.
* **Branch Naming**:
  * Feature: `feat/<phase>-<short-description>` (e.g., `feat/p2-ai-diagnosis`)
  * Bugfix: `fix/<short-description>`
  * Chore: `chore/<short-description>`
* **Pull Request Policy**:
  * Every PR must use the checklist provided in `.github/pull_request_template.md`.
  * The PR description must verify that no files outside your task's `ALLOWED PATHS` were modified.
  * All CI checks (linting, typing, unit tests) must pass before merging.
  * At least one teammate must review and approve before merging.

---

## 3. Cross-Team Contract Changes
If your feature requires modifying a shared API contract, schema, or event format (e.g. `apps/api` sending incident payloads to `apps/ai-worker`):
1. Propose the contract change in a dedicated issue or draft PR tagged with all affected owners.
2. Both owners must approve the schema before code changes begin.
3. Update shared schemas in `packages/` or API contracts before implementing consuming logic.
