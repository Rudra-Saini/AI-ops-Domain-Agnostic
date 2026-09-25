# Project Phases & Sequential Roadmap

> **Note on Terminology**: `P0`, `P1`, `P2` ... `P12` represent sequential milestones in this project's roadmap, NOT priority levels. Each phase has explicit goals and exit criteria.

---

### Phase P0: Governance & Repository Bootstrap
* **Goal**: Establish repository rules, ownership, branching standards, and skeleton directories.
* **Exit Criteria**: All planning documents (`PRD.md`, `Architecture.md`, `Rules.md`, `Phases.md`, `Design.md`, `Memory.md`), `README.md`, `CODEOWNERS`, and GitHub templates committed and approved.
* **Status**: **COMPLETE**

### Phase P1: Technical Foundation
* **Goal**: Build minimal application skeletons booting successfully, connected to PostgreSQL and Redis, containerized, with automated CI. Zero business logic.
* **Exit Criteria**: All 4 apps boot and respond to `/health`, Docker Compose orchestrates the full stack with restart policies, and CI pipeline passes.
* **Status**: **COMPLETE**

### Phase P2: AI Diagnostic Engine & Incident Ingestion (Rudra's Focus)
* **Goal**: Build out `apps/ai-worker` with real incident ingestion, LangChain/Gemini root-cause diagnosis, RAG incident retrieval, and AST hotpatch validation.
* **Exit Criteria**: `/api/v1/incidents/ingest`, `/api/v1/ai/diagnose`, `/api/v1/ai/remediate` operational and passing automated test suites.
* **Status**: **IN PROGRESS**

### Phase P3: Core E-Commerce API & Database Schemas
* **Goal**: Implement products, cart, and orders tables with PostgreSQL migrations in `apps/api`.
* **Status**: UPCOMING

### Phase P4: Chaos Engineering Suite
* **Goal**: Implement controlled failure injectors (zero-division in checkout, database pool exhaustion, missing secret).
* **Status**: UPCOMING

### Phase P5: SRE Developer Cockpit Frontend
* **Goal**: Real-time microservice topology, streaming WebSocket logs, incident inspection, and 1-click AST hotpatching UI.
* **Status**: UPCOMING

### Phase P6: End-to-End Self-Healing Integration
* **Goal**: Connect full loop: Chaos Injection $\rightarrow$ Crash Ingestion $\rightarrow$ AI Diagnosis $\rightarrow$ AST-Verified Patch $\rightarrow$ 1-Click Cockpit Remediation $\rightarrow$ Auto-Recovery.
* **Status**: UPCOMING
