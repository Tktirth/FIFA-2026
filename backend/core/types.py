"""Core Types for NEXOVA."""
from enum import Enum
from typing import TypeVar, Generic, Optional, List
from pydantic import BaseModel

T = TypeVar("T")

class UserRole(str, Enum):
    FAN = "fan"
    VOLUNTEER = "volunteer"
    SECURITY = "security"
    MEDICAL = "medical"
    OPERATIONS = "operations"
    VENDOR = "vendor"
    CLEANING = "cleaning"
    TRANSPORT = "transport"
    VIP = "vip"
    MEDIA = "media"

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentType(str, Enum):
    MEDICAL = "medical"
    SECURITY = "security"
    FIRE = "fire"
    STRUCTURAL = "structural"
    CROWD = "crowd"
    OTHER = "other"

ZoneId = str

class ApiResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    message: Optional[str] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int

class ErrorResponse(BaseModel):
    error: dict
