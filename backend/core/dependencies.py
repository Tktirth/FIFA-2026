"""Core Dependencies."""
from fastapi import Depends
from functools import lru_cache

from config.settings import Settings, settings
from intelligence.gemini_client import NexovaAI

@lru_cache()
def get_settings() -> Settings:
    return settings


def get_gemini_client(config: Settings = Depends(get_settings)) -> NexovaAI:
    return NexovaAI(
        project_id=config.GCP_PROJECT_ID,
        location=config.GCP_REGION,
        default_model=config.GEMINI_MODEL,
        enabled=config.ENABLE_AI
    )
