"""Main FastAPI Application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from config.settings import settings
from config.logging import configure_logging
from core.middleware import RequestIDMiddleware, SecurityHeadersMiddleware, TimingMiddleware, AuditLogMiddleware
from core.exceptions import register_exception_handlers
from features.auth.router import router as auth_router
from features.navigation.router import router as nav_router
from features.crowd.router import router as crowd_router
from features.incidents.router import router as incidents_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title="NEXOVA API",
        version="1.0.0",
        lifespan=lifespan
    )

    limiter = Limiter(key_func=get_remote_address, default_limits=[settings.BACKEND_RATE_LIMIT])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.add_middleware(AuditLogMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestIDMiddleware)

    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(nav_router, prefix="/api/v1")
    app.include_router(crowd_router, prefix="/api/v1")
    app.include_router(incidents_router, prefix="/api/v1")

    register_exception_handlers(app)

    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "version": app.version,
            "environment": settings.BACKEND_ENV,
            "timestamp": "now"
        }

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.BACKEND_PORT, reload=True)  # nosec B104
