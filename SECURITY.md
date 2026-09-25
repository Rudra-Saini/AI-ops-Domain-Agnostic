# Security Policy & AI Safety Guidelines

The **AIOps Self-Healing E-Commerce Platform** operates autonomous agents that diagnose errors and propose code remedies. High security standards are enforced across human and automated contributors.

---

## 1. Secrets Management
* **Zero Secrets in Git**: Never hardcode or commit database credentials, Redis passwords, secret keys, or LLM API keys (e.g., `GEMINI_API_KEY`, `OPENAI_API_KEY`).
* Always read secrets from environment variables, defined locally in `.env` (which is `.gitignore`d).
* Maintain `.env.example` as a template with dummy/placeholder values.

---

## 2. AI Safety & Code Verification
* **Human in the Loop**: AI-suggested code fixes, hotpatches, and remediations must never be silently pushed to `main` without human confirmation.
* **AST Validation Gate**: Any patch synthesized by `apps/ai-worker` must undergo Abstract Syntax Tree (AST) validation before it is even presented to the developer. Invalid syntax, harmful system calls (`os.system`, `subprocess`, `shutil.rmtree`), or hallucinated modules must be rejected immediately.
* **Bounded Scope**: AI workers may only propose patches targeting the service encountering the incident.

---

## 3. Least Privilege & Webhook Integrity
* Containers run with non-root user permissions wherever possible.
* Webhook endpoints receiving telemetry or alerts must validate message signatures.
* Redis access is scoped to the shared internal docker network (`aiops-net`).
