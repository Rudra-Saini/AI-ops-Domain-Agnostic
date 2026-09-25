from typing import List, Optional
from ..models.schemas import RAGPattern, RAGSearchResult

KNOWLEDGE_BASE: List[RAGPattern] = [
    RAGPattern(
        pattern_id="PAT-001",
        title="ZeroDivisionError in Cart Discount Calculation",
        error_signature="ZeroDivisionError: division by zero",
        keywords=["zerodivisionerror", "division by zero", "discount", "coupon", "cart", "total"],
        root_cause_explanation="Discount or item pricing logic divides by cart item quantity or subtotal without checking if value is 0 (e.g. empty cart or 100% coupon FLASH50).",
        standard_fix_diff="""--- a/apps/api/routers/cart.py
+++ b/apps/api/routers/cart.py
@@ -42,7 +42,7 @@
-    discount_per_item = total_discount / item_count
+    discount_per_item = (total_discount / item_count) if item_count > 0 else 0.0
""",
        reference_runbook="RB-001: Ensure all numerical denominators have guard clauses (if denom > 0) before division."
    ),
    RAGPattern(
        pattern_id="PAT-002",
        title="PostgreSQL Connection Pool Exhaustion",
        error_signature="asyncpg.exceptions.TooManyConnectionsError: remaining connection slots are reserved",
        keywords=["connection", "pool", "exhausted", "asyncpg", "toomanyconnectionserror", "slots", "timeout"],
        root_cause_explanation="Database connection leak or high burst traffic exceeding connection pool size (max_overflow=0 or lack of connection release in finally block).",
        standard_fix_diff="""--- a/apps/api/database.py
+++ b/apps/api/database.py
@@ -18,4 +18,6 @@
-    pool_size=5, max_overflow=0
+    pool_size=20, max_overflow=10, pool_recycle=1800, pool_pre_ping=True
""",
        reference_runbook="RB-002: Increase max_overflow and ensure async sessions are closed via 'async with get_db()'."
    ),
    RAGPattern(
        pattern_id="PAT-003",
        title="Missing Environment Secret / KeyError in JWT Authentication",
        error_signature="KeyError: 'JWT_SECRET'",
        keywords=["keyerror", "jwt_secret", "secret", "environ", "getenv", "missing env"],
        root_cause_explanation="Microservice attempted to read mandatory configuration directly using os.environ['JWT_SECRET'] without default or fallback value.",
        standard_fix_diff="""--- a/apps/api/auth.py
+++ b/apps/api/auth.py
@@ -10,3 +10,3 @@
-SECRET_KEY = os.environ['JWT_SECRET']
+SECRET_KEY = os.getenv('JWT_SECRET', 'fallback_development_secret_do_not_use_in_prod')
""",
        reference_runbook="RB-003: Always use os.getenv() with safe fallback defaults for non-production environments."
    ),
    RAGPattern(
        pattern_id="PAT-004",
        title="Database Schema Drift / Missing Column in Orders Table",
        error_signature="asyncpg.exceptions.UndefinedColumnError: column 'tax_rate' does not exist",
        keywords=["undefinedcolumnerror", "column", "does not exist", "schema", "migration", "tax_rate"],
        root_cause_explanation="Application queries a database column introduced in an unapplied Alembic migration or missing in test database schema.",
        standard_fix_diff="""--- a/database/migrations/versions/002_add_tax_rate.py
+++ b/database/migrations/versions/002_add_tax_rate.py
@@ -15,1 +15,2 @@
+    op.add_column('orders', sa.Column('tax_rate', sa.Float(), server_default='0.18'))
""",
        reference_runbook="RB-004: Execute 'alembic upgrade head' or dynamically fallback to default tax rate."
    ),
    RAGPattern(
        pattern_id="PAT-005",
        title="Payment Gateway API Rate Limit Spike (HTTP 429)",
        error_signature="HTTPStatusError: 429 Too Many Requests from Payment Gateway",
        keywords=["429", "too many requests", "rate limit", "payment", "razorpay", "upi", "gateway"],
        root_cause_explanation="Surge in payment status polling requests triggered gateway throttle.",
        standard_fix_diff="""--- a/apps/api/payment.py
+++ b/apps/api/payment.py
@@ -28,3 +28,4 @@
-    response = httpx.post(GATEWAY_URL, json=payload)
+    # Implement exponential backoff jitter
     response = await retry_with_backoff(lambda: client.post(GATEWAY_URL, json=payload))
""",
        reference_runbook="RB-005: Introduce exponential backoff with jitter and client-side rate limit token bucket."
    )
]

class RAGEngine:
    def __init__(self):
        self.patterns = KNOWLEDGE_BASE

    def search_similar_patterns(self, error_type: str, error_message: str, stack_trace: str) -> List[RAGSearchResult]:
        query_text = f"{error_type} {error_message} {stack_trace}".lower()
        results: List[RAGSearchResult] = []

        for pattern in self.patterns:
            matched_kw = [kw for kw in pattern.keywords if kw in query_text]
            if matched_kw:
                score = len(matched_kw) / max(len(pattern.keywords), 1)
                score = min(round(score, 2), 1.0)
                results.append(
                    RAGSearchResult(
                        pattern_id=pattern.pattern_id,
                        title=pattern.title,
                        similarity_score=score,
                        matched_keywords=matched_kw,
                        root_cause_explanation=pattern.root_cause_explanation,
                        suggested_runbook=pattern.reference_runbook
                    )
                )

        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results

    def get_pattern_by_id(self, pattern_id: str) -> Optional[RAGPattern]:
        for pattern in self.patterns:
            if pattern.pattern_id == pattern_id:
                return pattern
        return None

rag_engine = RAGEngine()
