import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
try:
    import redis.asyncio as aioredis
except ImportError:
    aioredis = None

app = FastAPI(
    title="AIOps Core API Service",
    description="Backend service for E-Commerce orders, products, and chaos telemetry",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

@app.get("/health")
async def health_check():
    """Health check endpoint to prove service and dependencies are alive."""
    redis_status = "unknown"
    if aioredis is None:
        redis_status = "uninstalled_on_host"
    else:
        try:
            r = aioredis.from_url(REDIS_URL, decode_responses=True)
            pong = await r.ping()
            redis_status = "connected" if pong else "failed"
            await r.aclose()
        except Exception as e:
            redis_status = f"unreachable: {str(e)}"

    return {
        "status": "ok",
        "service": "api",
        "redis": redis_status,
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/")
async def root():
    return {
        "message": "AIOps E-Commerce Core API is operational",
        "health_url": "/health"
    }
