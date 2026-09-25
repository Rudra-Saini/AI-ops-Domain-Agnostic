import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps" / "ai-worker"))

from app.services.rag_engine import rag_engine

def test_rag_matches_zero_division():
    results = rag_engine.search_similar_patterns(
        error_type="ZeroDivisionError",
        error_message="division by zero in cart total",
        stack_trace="File 'cart.py', line 42, in calculate discount_per_item = total / count"
    )
    assert len(results) > 0
    top = results[0]
    assert top.pattern_id == "PAT-001"
    assert "ZeroDivisionError" in top.title
    assert top.similarity_score >= 0.5

def test_rag_matches_db_pool_exhaustion():
    results = rag_engine.search_similar_patterns(
        error_type="TooManyConnectionsError",
        error_message="remaining connection slots are reserved",
        stack_trace="asyncpg.exceptions.TooManyConnectionsError"
    )
    assert len(results) > 0
    top = results[0]
    assert top.pattern_id == "PAT-002"
    assert "Pool Exhaustion" in top.title
