"""Firestore Client Initialization."""
from google.cloud import firestore
from google.cloud.firestore_v1.async_client import AsyncClient
import structlog
from typing import Optional
from config.settings import settings

logger = structlog.get_logger()

_db: Optional[AsyncClient] = None

def get_firestore_client() -> AsyncClient:
    """Get or initialize the global Firestore AsyncClient."""
    global _db
    if _db is None:
        logger.info("firestore_init", project=settings.GCP_PROJECT_ID)
        _db = firestore.AsyncClient(
            project=settings.GCP_PROJECT_ID,
            database=settings.FIRESTORE_DATABASE
        )
    return _db
