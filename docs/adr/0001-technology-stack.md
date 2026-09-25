# ADR 0001: Technology Stack Standardization

## Status
Accepted

## Context
The project team comprises four engineering students with varying backgrounds. We need a performant, maintainable, and modern tech stack supporting microservices, asynchronous message passing, high-speed API endpoints, and a cutting-edge LLM/RAG pipeline.

## Decision
1. **Core Language for Backend and AI**: Standardized on **Python 3.12** across `apps/api`, `apps/worker`, and `apps/ai-worker`. Python provides first-class support for FastAPI, async database drivers, and the most mature ecosystem for LLM/RAG libraries (LangChain).
2. **Frontend Framework**: Standardized on **TypeScript with Next.js 14 (React)** for `apps/web`. Browsers natively execute JavaScript/TypeScript, and Next.js offers server-side rendering for optimal performance and dashboard reactivity.
3. **Storage & Messaging**: Standardized on **PostgreSQL 16** for relational persistence and **Redis 7** for telemetry caching and pub/sub message queuing.
4. **Containerization**: Standardized on **Docker Compose** to guarantee identical local environments across all team machines.

## Consequences
* Every developer can run the entire system locally via `docker compose up --build`.
* AI Lead (Rudra) can directly use LangChain without language cross-boundary overhead.
