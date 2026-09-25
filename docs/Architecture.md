# System Architecture & Technical Blueprint

```
                     +---------------------------------------+
                     |         Web Frontend (:3000)          |
                     |  - Customer Megastore                 |
                     |  - SRE Developer Cockpit (Next.js 14) |
                     +-------------------+-------------------+
                                         |
                       REST / WebSocket  |
                                         v
                     +---------------------------------------+
                     |            Core API (:8000)           |
                     |  - Fast API Backend Service           |
                     |  - Orders, Products, Cart             |
                     |  - Chaos Injection Endpoints          |
                     +---------+-------------------+---------+
                               |                   |
                     Telemetry |                   | Job Dispatch
                               v                   v
+---------------------------------------+   +---------------------------------------+
|          AI Worker (:8001)            |   |          Background Worker            |
|  - Owned by Rudra (AI/RAG Lead)       |   |  - RQ Redis Queue Worker              |
|  - Incident Ingestion & Webhooks      |   |  - Async event & notification worker  |
|  - Hybrid GenAI Diagnosis (LangChain) |   +-------------------+-------------------+
|  - RAG Incident Memory Engine         |                       |
|  - AST-Verified Hotpatch Generator    |                       |
+-------------------+-------------------+                       |
                    |                                           |
                    +--------------------+----------------------+
                                         |
                                         v
                         +-------------------------------+
                         |      Redis Broker (:6379)     |
                         |  - Pub/Sub Incident Channel   |
                         |  - RQ Task Queue              |
                         |  - Telemetry Frame Cache      |
                         +---------------+---------------+
                                         |
                                         v
                         +-------------------------------+
                         |      PostgreSQL (:5432)       |
                         |  - Catalog & Order Stores     |
                         |  - Incident Audit History     |
                         |  - SRE Metrics & MTTR Logs    |
                         +-------------------------------+
```

---

## Service Contracts & Responsibilities

### 1. `apps/ai-worker/` (Rudra — AI / RAG Lead)
* **Port**: 8001
* **Stack**: Python 3.12, FastAPI, LangChain, Google Gemini SDK, Redis, Pydantic, AST.
* **Responsibilities**:
  * Consumes crash reports and error logs via Redis pub/sub (`incidents:channel`) or REST (`POST /api/v1/incidents/ingest`).
  * Runs similarity search against past incident patterns and runbooks (RAG engine).
  * Executes Hybrid LLM root cause analysis using structured LangChain prompts and deterministic fallback.
  * Formulates unified code diffs and performs AST parsing validation.
  * Serves diagnosis and hotpatch recommendations to the Cockpit.

### 2. `apps/api/` (Taranay — Backend Lead)
* **Port**: 8000
* **Stack**: Python 3.12, FastAPI, SQLAlchemy, AsyncPG, Redis.
* **Responsibilities**: E-commerce business logic, inventory, cart calculation, checkout transactions, and error interceptor emitting crash telemetry.

### 3. `apps/worker/` (Taranay — Backend Lead)
* **Stack**: Python 3.12, RQ, Redis.
* **Responsibilities**: Handles asynchronous tasks without blocking client API requests. Configured with Docker self-healing restart policy.

### 4. `apps/web/` (Vivek — Frontend Lead)
* **Port**: 3000
* **Stack**: TypeScript, Next.js 14, React, TailwindCSS.
* **Responsibilities**: Unified dual-mode interface (Customer Storefront + SRE Developer Cockpit).

### 5. Infrastructure & DevOps (Saurav — DevOps Lead)
* **Stack**: Docker Compose, GitHub Actions, Linux containers.
* **Responsibilities**: Compose networking, Dockerfiles, continuous integration pipeline, environment security.
