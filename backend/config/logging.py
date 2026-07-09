"""Logging configuration."""
import structlog
import logging
from .settings import settings

def configure_logging():
    logging.getLevelName(settings.BACKEND_LOG_LEVEL.upper())
    
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer() if settings.BACKEND_ENV == "production" else structlog.dev.ConsoleRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
