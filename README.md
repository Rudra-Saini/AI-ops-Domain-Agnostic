# ⚡ AIOps Self-Healing E-Commerce Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C.svg?style=flat)](https://langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

> **B.Tech Computer Science & Engineering — Minor Project**  
> An autonomous Site Reliability Engineering (SRE) and AIOps platform with a dual interface (Live Customer Store + SRE Developer Cockpit). It monitors production microservice crashes, isolates root causes with **Hybrid GenAI (LangChain + Gemini with deterministic fallback)**, visualizes live unified code diffs, and executes AST-verified self-healing hotpatches.

---

## 👥 Team & Code Ownership

Defined in `CODEOWNERS` and `docs/Rules.md`:

| Member | Role | Owned Directory | Primary Responsibilities |
| :--- | :--- | :--- | :--- |
| **Rudra** | **AI / RAG Lead** | `apps/ai-worker/` | Crash analysis, LangChain diagnostic pipeline, RAG incident memory, AST-verified hotpatch generation. |
| **Saurav** | **DevOps Lead** | `infrastructure/`, CI/CD | Docker, compose, CI pipelines, branch policies, deployment orchestration. |
| **Taranay** | **Backend Lead** | `apps/api/`, `apps/worker/` | E-commerce REST APIs, database schemas, async background job queues (RQ). |
| **Vivek** | **Frontend Lead** | `apps/web/` | SRE Developer Cockpit dashboard & customer storefront interfaces (Next.js/React). |

---

## 🏛️ Microservice Architecture & Port Allocations

| Service | Directory | Technology | Internal Port | Host Port | Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AI Worker** | `apps/ai-worker/` | Python 3.12, LangChain, FastAPI | 8001 | `http://localhost:8001` | **Rudra's Domain**: Incident diagnosis & self-healing |
| **API** | `apps/api/` | Python 3.12, FastAPI | 8000 | `http://localhost:8000` | Core E-Commerce backend API |
| **Worker** | `apps/worker/` | Python 3.12, RQ, Redis | N/A | N/A | Asynchronous task processing |
| **Web** | `apps/web/` | TypeScript, Next.js 14 | 3000 | `http://localhost:3000` | SRE Developer Cockpit & Customer Store |
| **PostgreSQL** | `database/` | PostgreSQL 16 | 5432 | `localhost:5432` | Primary relational database |
| **Redis** | Infrastructure | Redis 7 Alpine | 6379 | `localhost:6379` | Queue broker and telemetry cache |

---

## 🚀 Quickstart Guide

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (running)
* Python 3.12+ (for local development)
* Node.js 18+ (for frontend development)

### 1. Configure Environment
```bash
cp .env.example .env
```

### 2. Boot Full Stack with Docker Compose
```bash
docker compose up --build
```

### 3. Verify Health Endpoints
* **AI Worker (Rudra):** [http://localhost:8001/health](http://localhost:8001/health)
* **Backend API:** [http://localhost:8000/health](http://localhost:8000/health)
* **Developer Cockpit:** [http://localhost:3000](http://localhost:3000)

---

## 📚 Governance Documentation
All project rules and architecture blueprints are located in `docs/`:
* [PRD.md](docs/PRD.md) — Product Requirements Document.
* [Architecture.md](docs/Architecture.md) — System blueprint and service topology.
* [Rules.md](docs/Rules.md) — Coding conventions, tech stack, and boundary enforcement.
* [Phases.md](docs/Phases.md) — Sequential milestones (P0 through P12).
* [Design.md](docs/Design.md) — Frontend and cockpit design guidelines.
* [Memory.md](docs/Memory.md) — Chronological log of built features and roadmap state.
