"""Auth Feature Models."""
from pydantic import BaseModel
from datetime import datetime

from core.types import UserRole
from core.security import DemoUser

class LoginRequest(BaseModel):
    role: UserRole

class LoginResponse(BaseModel):
    user: DemoUser
    token: str
    expires_at: datetime

class PersonaInfo(BaseModel):
    role: UserRole
    name: str
    description: str
    icon: str
    color: str
