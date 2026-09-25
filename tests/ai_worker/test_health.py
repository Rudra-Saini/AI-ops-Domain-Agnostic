import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps" / "ai-worker"))

from main import app

client = TestClient(app)

def test_ai_worker_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ai-worker"
    assert "Rudra" in data["owner"]
    assert "langchain_version" in data

def test_ai_worker_verify_patch_endpoint():
    payload = {
        "source_code": "def safe_sub(a, b):\n    return a - b\n"
    }
    response = client.post("/api/v1/ai/verify-patch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is True
    assert data["security_check"] == "PASSED"
