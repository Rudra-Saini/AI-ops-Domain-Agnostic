# Project Rules & Technology Standard

This document is the **single source of truth** for repository conventions, tech stack selections, ownership boundaries, and AI agent permissions.

---

## 1. Finalized Technology Stack

| Application / Area | Language / Framework | Key Libraries | Owner |
| :--- | :--- | :--- | :--- |
| `apps/ai-worker` | Python 3.12 + FastAPI | LangChain, LangChain-Community, Google-GenerativeAI, Redis, Pydantic | **Rudra** |
| `apps/api` | Python 3.12 + FastAPI | Uvicorn, SQLAlchemy, AsyncPG, Pydantic, Redis | Taranay |
| `apps/worker` | Python 3.12 | RQ (Redis Queue), Redis, SQLAlchemy, AsyncPG | Taranay |
| `apps/web` | TypeScript + Next.js 14 | React, TailwindCSS, Lucide-React | Vivek |
| Database | PostgreSQL 16 | Relational persistence | Saurav / Taranay |
| Queue / Cache | Redis 7 Alpine | In-memory message broker & telemetry bus | Saurav |
| Containers | Docker & Compose | Multi-container composition | Saurav |

---

## 2. Directory Ownership Boundaries
1. **Rudra**: Exclusively owns `apps/ai-worker/`, AI evaluation tests under `tests/ai_worker/`, and AI prompt templates.
2. **Saurav**: Exclusively owns `infrastructure/`, `.github/`, root orchestration (`docker-compose.yml`), and environment setup.
3. **Taranay**: Exclusively owns `apps/api/`, `apps/worker/`, and `database/`.
4. **Vivek**: Exclusively owns `apps/web/`.

> **Cross-boundary rule**: No member (or AI assistant working on behalf of a member) may modify files outside their owned paths without proposing a contract update or creating a multi-author PR.

---

## 3. AI Safety & Agent Guardrails
* **No Unverified Execution**: Code hotpatches synthesized by an LLM must be parsed and verified using Python's `ast.parse()` to prevent syntactically malformed patches.
* **Human Approval**: The SRE Cockpit must provide an explicit "Apply Hotpatch" button with unified diff inspection before any production code modification takes effect.
* **No Secret Leakage**: AI prompts must sanitize credentials, passwords, and sensitive session tokens before invoking external LLMs.
