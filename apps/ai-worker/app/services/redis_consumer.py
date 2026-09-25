import asyncio
import json
import logging
try:
    import redis.asyncio as aioredis
except ImportError:
    aioredis = None
from ..config import settings
from ..models.schemas import IncidentEvent
from .diagnosis_engine import diagnosis_engine
from .hotpatch_engine import hotpatch_engine

logger = logging.getLogger(__name__)

INCIDENT_CACHE = []

async def start_redis_listener():
    """Background loop listening to Redis pub/sub channel for incident alerts."""
    if aioredis is None:
        logger.warning("Redis library not installed on host. Redis subscriber disabled.")
        return
    logger.info(f"Connecting to Redis at {settings.REDIS_URL} for incident alerts...")
    while True:
        try:
            r = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
            pubsub = r.pubsub()
            await pubsub.subscribe(settings.REDIS_INCIDENT_CHANNEL)
            logger.info(f"[✓] Subscribed to Redis channel: '{settings.REDIS_INCIDENT_CHANNEL}'")

            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        incident = IncidentEvent(**data)
                        logger.info(f"[!] Processing received incident: {incident.incident_id} ({incident.error_type})")
                        
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
                    except Exception as parse_err:
                        logger.error(f"Error handling incident message: {parse_err}")

        except asyncio.CancelledError:
            logger.info("Redis subscriber task cancelled.")
            break
        except Exception as conn_err:
            logger.warning(f"Redis subscriber connection dropped ({conn_err}). Reconnecting in 5s...")
            await asyncio.sleep(5)
