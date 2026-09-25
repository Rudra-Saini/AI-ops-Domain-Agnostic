import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps" / "ai-worker"))

from app.models.schemas import IncidentEvent
from app.services.diagnosis_engine import diagnosis_engine
from app.services.hotpatch_engine import hotpatch_engine

@pytest.mark.asyncio
async def test_diagnosis_deterministic_fallback():
    incident = IncidentEvent(
        incident_id="test-inc-001",
        service_name="api",
        error_type="ZeroDivisionError",
        error_message="division by zero",
        stack_trace="ZeroDivisionError: division by zero in /routers/cart.py line 42",
        affected_file="apps/api/routers/cart.py"
    )

    diagnosis = await diagnosis_engine.diagnose_incident(incident)
    assert diagnosis.incident_id == "test-inc-001"
    assert diagnosis.confidence_score >= 0.8
    assert "ZeroDivisionError" in diagnosis.root_cause

    remediation = hotpatch_engine.generate_remediation_plan(incident, diagnosis)
    assert remediation.ast_validated is True
    assert remediation.safety_status == "PASSED"
    assert remediation.can_auto_apply is True
    assert "calculate_discount" in remediation.patch_diff or "apps/api" in remediation.patch_diff
