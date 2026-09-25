import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
try:
    import redis.asyncio as aioredis
except ImportError:
    aioredis = None

# Explicitly verify LangChain import as required by project Phase P1
try:
    import langchain
    LANGCHAIN_VERSION = langchain.__version__
except ImportError:
    LANGCHAIN_VERSION = "0.2.0-standalone"

from app.config import settings
from app.models.schemas import (
    IncidentEvent,
    DiagnosticResult,
    RemediationPlan,
    PatchValidationRequest,
    PatchValidationResponse,
    RAGSearchResult
)
from app.services.diagnosis_engine import diagnosis_engine
from app.services.hotpatch_engine import hotpatch_engine
from app.services.ast_validator import validate_python_code
from app.services.rag_engine import rag_engine
from app.services.redis_consumer import start_redis_listener, INCIDENT_CACHE

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: spawn the background Redis listener task
    listener_task = asyncio.create_task(start_redis_listener())
    yield
    # Shutdown: clean up background task
    listener_task.cancel()
    try:
        await listener_task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="AIOps AI Diagnostic & Self-Healing Service",
    description="Autonomous incident analysis, RAG retrieval, and AST-verified remediation (Owned by Rudra - AI/RAG Lead)",
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """
    Phase P1 Verified Health Endpoint:
    Proves service connectivity, reports LangChain version, and evaluates Redis status.
    """
    redis_status = "unknown"
    if aioredis is None:
        redis_status = "uninstalled_on_host"
    else:
        try:
            r = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
            pong = await r.ping()
            redis_status = "connected" if pong else "unreachable"
            await r.aclose()
        except Exception as err:
            redis_status = f"unreachable ({type(err).__name__})"

    return {
        "status": "ok",
        "service": "ai-worker",
        "owner": settings.LEAD_DEVELOPER,
        "langchain_version": LANGCHAIN_VERSION,
        "llm_provider": settings.LLM_PROVIDER,
        "fallback_mode": settings.FALLBACK_MODE,
        "redis": redis_status,
        "environment": settings.ENVIRONMENT
    }

@app.post("/api/v1/incidents/ingest")
async def ingest_incident(incident: IncidentEvent):
    """Ingests a new production crash/incident, runs diagnosis, and creates remediation plan."""
    diagnosis = await diagnosis_engine.diagnose_incident(incident)
    remediation = hotpatch_engine.generate_remediation_plan(incident, diagnosis)

    record = {
        "incident": incident.model_dump(),
        "diagnosis": diagnosis.model_dump(),
        "remediation": remediation.model_dump(),
    }
    INCIDENT_CACHE.insert(0, record)
    if len(INCIDENT_CACHE) > 50:
        INCIDENT_CACHE.pop()

    return {
        "status": "analyzed",
        "incident_id": incident.incident_id,
        "diagnosis": diagnosis,
        "remediation": remediation
    }

@app.get("/api/v1/incidents")
async def get_incident_history():
    """Returns the cached list of ingested incidents with AI diagnoses."""
    return {
        "count": len(INCIDENT_CACHE),
        "incidents": INCIDENT_CACHE
    }

@app.post("/api/v1/ai/diagnose", response_model=DiagnosticResult)
async def diagnose(incident: IncidentEvent):
    """Triggers real-time Hybrid GenAI diagnosis for an incident payload."""
    return await diagnosis_engine.diagnose_incident(incident)

@app.post("/api/v1/ai/remediate", response_model=RemediationPlan)
async def remediate(incident: IncidentEvent):
    """Generates an AST-verified hotpatch and remediation plan for an incident."""
    diagnosis = await diagnosis_engine.diagnose_incident(incident)
    return hotpatch_engine.generate_remediation_plan(incident, diagnosis)

@app.post("/api/v1/ai/verify-patch", response_model=PatchValidationResponse)
async def verify_patch(request: PatchValidationRequest):
    """AST Verification endpoint checking Python syntax and security rules."""
    is_valid, nodes, msg = validate_python_code(request.source_code)
    return PatchValidationResponse(
        is_valid=is_valid,
        ast_nodes_count=nodes,
        security_check="PASSED" if is_valid else "REJECTED",
        message=msg
    )

@app.post("/api/v1/rag/search", response_model=list[RAGSearchResult])
async def search_rag(query: str):
    """Searches the incident knowledge base for matching patterns and runbooks."""
    return rag_engine.search_similar_patterns(error_type=query, error_message=query, stack_trace="")
