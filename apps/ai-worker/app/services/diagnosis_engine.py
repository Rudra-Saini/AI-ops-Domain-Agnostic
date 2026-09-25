import logging
from typing import Optional
from ..models.schemas import IncidentEvent, DiagnosticResult
from ..config import settings
from .rag_engine import rag_engine

logger = logging.getLogger(__name__)

class DiagnosisEngine:
    """
    Hybrid GenAI Diagnostic Engine:
    Combines LangChain / Gemini LLM reasoning with deterministic pattern-matching fallback.
    """

    async def diagnose_incident(self, incident: IncidentEvent) -> DiagnosticResult:
        rag_matches = rag_engine.search_similar_patterns(
            error_type=incident.error_type,
            error_message=incident.error_message,
            stack_trace=incident.stack_trace
        )

        top_pattern = rag_matches[0] if rag_matches else None

        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
            try:
                llm_result = await self._diagnose_with_gemini(incident, top_pattern)
                if llm_result:
                    return llm_result
            except Exception as e:
                logger.warning(f"LLM diagnosis failed ({e}). Reverting to deterministic fallback.")

        return self._diagnose_with_fallback(incident, top_pattern)

    async def _diagnose_with_gemini(self, incident: IncidentEvent, top_pattern) -> Optional[DiagnosticResult]:
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(settings.GEMINI_MODEL)

            rag_context = ""
            if top_pattern:
                rag_context = f"\nRelevant Historical Runbook: {top_pattern.title}\n{top_pattern.root_cause_explanation}"

            prompt = f"""
You are an expert SRE and AIOps Autonomous Incident Diagnostician.
Analyze the following microservice incident and provide:
1. Root cause explanation
2. Confidence score (between 0.0 and 1.0)
3. Specific suggested fix summary

Incident Details:
Service: {incident.service_name}
Error Type: {incident.error_type}
Message: {incident.error_message}
Stack Trace:
{incident.stack_trace}
Affected File: {incident.affected_file or 'N/A'}
{rag_context}

Return your response strictly in concise technical language.
"""
            response = await model.generate_content_async(prompt)
            explanation = response.text.strip() if response.text else "LLM Analysis completed."

            return DiagnosticResult(
                incident_id=incident.incident_id,
                root_cause=explanation,
                confidence_score=0.95,
                diagnostic_source="gemini_llm",
                suggested_fix_summary="Generated from Gemini reasoning using stack trace and RAG context.",
                target_file=incident.affected_file
            )
        except Exception as err:
            logger.error(f"Gemini LLM call failed: {err}")
            return None

    def _diagnose_with_fallback(self, incident: IncidentEvent, top_pattern) -> DiagnosticResult:
        if top_pattern:
            confidence = max(0.85, top_pattern.similarity_score)
            return DiagnosticResult(
                incident_id=incident.incident_id,
                root_cause=f"[RAG Matched: {top_pattern.title}] {top_pattern.root_cause_explanation}",
                confidence_score=confidence,
                diagnostic_source="deterministic_fallback",
                suggested_fix_summary=top_pattern.suggested_runbook,
                target_file=incident.affected_file
            )

        return DiagnosticResult(
            incident_id=incident.incident_id,
            root_cause=f"Unhandled exception '{incident.error_type}' in {incident.service_name}: {incident.error_message}",
            confidence_score=0.70,
            diagnostic_source="deterministic_fallback",
            suggested_fix_summary="Inspect stack trace and add defensive error handling around crashing instruction.",
            target_file=incident.affected_file
        )

diagnosis_engine = DiagnosisEngine()
