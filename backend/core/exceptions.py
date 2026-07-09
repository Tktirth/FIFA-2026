"""Core Exceptions for NEXOVA."""
from fastapi import Request
from fastapi.responses import JSONResponse

class NexovaException(Exception):
    def __init__(self, status_code: int, detail: str, error_code: str):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code

class NotFoundError(NexovaException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(404, detail, "NOT_FOUND")

class ForbiddenError(NexovaException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(403, detail, "FORBIDDEN")

class ValidationError(NexovaException):
    def __init__(self, detail: str = "Validation Error"):
        super().__init__(422, detail, "VALIDATION_ERROR")

class AIServiceError(NexovaException):
    def __init__(self, detail: str = "AI Service Error"):
        super().__init__(503, detail, "AI_SERVICE_ERROR")

def register_exception_handlers(app):
    @app.exception_handler(NexovaException)
    async def nexova_exception_handler(request: Request, exc: NexovaException):
        req_id = request.state.request_id if hasattr(request.state, "request_id") else "unknown"
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.error_code, "message": exc.detail, "request_id": req_id}}
        )
