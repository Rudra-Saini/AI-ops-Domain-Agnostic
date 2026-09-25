import os

class Settings:
    PROJECT_NAME: str = "AIOps AI Worker & Self-Healing Engine"
    VERSION: str = "0.1.0"
    LEAD_DEVELOPER: str = "Rudra (AI / RAG Lead)"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    REDIS_INCIDENT_CHANNEL: str = "aiops:incidents"
    REDIS_TELEMETRY_KEY: str = "aiops:telemetry:live"
    
    # LLM Settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    FALLBACK_MODE: str = os.getenv("FALLBACK_MODE", "deterministic")

settings = Settings()
