# Product Requirements Document (PRD)

## 1. Executive Summary & Vision
The **AIOps Self-Healing E-Commerce Platform** is an autonomous Site Reliability Engineering (SRE) solution engineered for microservice-based e-commerce architectures. Modern online stores experience unexpected downtime and customer friction due to database pool exhaustion, sudden schema breaks, unhandled exceptions, and third-party rate limits.

This platform bridges the gap between chaos and recovery by pairing an Indian electronics storefront with an autonomous SRE Developer Cockpit:
1. **Live Customer Storefront**: Demonstrates realistic user transactions (product browsing, cart, checkout, payments).
2. **Autonomous AI Diagnostic Agent**: Ingests crashes in real time, diagnoses root causes using Hybrid GenAI (LangChain + Gemini with deterministic fallback), and generates AST-verified hotpatches.
3. **SRE Developer Cockpit**: Live telemetry topology, real-time WebSocket log stream, chaos injection control, and 1-click self-healing patch activation.

---

## 2. Target Personas
* **Site Reliability Engineer (SRE)**: Wants immediate root cause explanations, reduced Mean Time to Detect (MTTD), and reduced Mean Time to Recovery (MTTR) from hours to seconds.
* **Backend Engineer**: Wants precise stack trace analysis and safe, automated code diff suggestions.
* **Customer**: Experiences high availability and zero friction during checkout transactions.

---

## 3. Core Functional Requirements
* **FR-1 Microservice Foundation**: Independent API, background worker, AI diagnostic worker, and web frontend running in Docker.
* **FR-2 Chaos Engineering Suite**: Ability to inject controlled real-world failure scenarios (zero division in cart discount calculation, database connection pool exhaustion, missing environment secret, schema mismatch).
* **FR-3 Autonomous AI Ingestion & Analysis**: `apps/ai-worker` listens for error events, searches vector/knowledge base of past incidents, and calls an LLM to generate root-cause diagnosis.
* **FR-4 AST-Verified Hotpatch Generation**: Auto-generate Python unified diffs, run AST validation to ensure syntactic safety, and verify fix before remediation.
* **FR-5 Telemetry & Cockpit Dashboard**: Live streaming log viewer, node health indicators, and 1-click patch application.

---

## 4. Non-Functional Requirements
* **NFR-1 Recovery Speed**: Automated MTTR < 10 seconds for known and diagnosed failures.
* **NFR-2 Security**: Zero secrets in source repository; mandatory human approval gate for code modifications.
* **NFR-3 Modularity**: Clean boundary separation between team members using CODEOWNERS.
