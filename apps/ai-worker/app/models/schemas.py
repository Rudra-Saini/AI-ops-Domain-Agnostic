from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

class IncidentEvent(BaseModel):
    incident_id: str = Field(..., description="Unique UUID or identifier for the incident")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    service_name: str = Field(..., description="Affected microservice (e.g. api, worker, web)")
    error_type: str = Field(..., description="Python exception or HTTP status name")
    error_message: str = Field(..., description="Detailed error message")
    stack_trace: str = Field(..., description="Full captured traceback")
    affected_file: Optional[str] = Field(None, description="Path to the file where crash originated")
    code_snippet: Optional[str] = Field(None, description="Source code excerpt around crash point")
    context_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Request parameters or state")

class DiagnosticResult(BaseModel):
    incident_id: str
    root_cause: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    diagnostic_source: str = Field(..., description="'gemini_llm' or 'deterministic_fallback'")
    suggested_fix_summary: str
    target_file: Optional[str] = None
    affected_line: Optional[int] = None
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class RemediationPlan(BaseModel):
    incident_id: str
    target_file: str
    patch_diff: str = Field(..., description="Unified diff syntax containing the fix")
    ast_validated: bool
    ast_validation_message: str
    safety_status: str = Field(..., description="'PASSED' or 'REJECTED'")
    can_auto_apply: bool = False
    estimated_mttr_seconds: float = Field(default=2.5)

class PatchValidationRequest(BaseModel):
    source_code: str
    target_file_name: Optional[str] = "patch.py"

class PatchValidationResponse(BaseModel):
    is_valid: bool
    ast_nodes_count: int
    security_check: str
    message: str

class RAGPattern(BaseModel):
    pattern_id: str
    title: str
    error_signature: str
    keywords: List[str]
    root_cause_explanation: str
    standard_fix_diff: str
    reference_runbook: str

class RAGSearchResult(BaseModel):
    pattern_id: str
    title: str
    similarity_score: float
    matched_keywords: List[str]
    root_cause_explanation: str
    suggested_runbook: str
