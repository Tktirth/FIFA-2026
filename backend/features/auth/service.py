"""Auth Service."""
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException

from config.settings import settings
from core.types import UserRole
from core.security import DEMO_USERS
from core.cache import async_cache
from .models import LoginResponse, PersonaInfo

class AuthService:
    def __init__(self):
        pass

    async def login(self, role: UserRole) -> LoginResponse:
        if role not in DEMO_USERS:
            raise HTTPException(status_code=400, detail="Invalid role")
        
        user = DEMO_USERS[role]
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
        
        token = jwt.encode(
            {"sub": user.id, "role": role.value, "exp": expires_at},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        
        return LoginResponse(
            user=user,
            token=token,
            expires_at=expires_at
        )

    @async_cache(ttl=3600)
    async def get_personas(self) -> list[PersonaInfo]:
        return [
            PersonaInfo(role=UserRole.FAN, name="Fan", description="Match info, tickets, navigation.", icon="User", color="blue"),
            PersonaInfo(role=UserRole.VOLUNTEER, name="Volunteer", description="Shift tasks, alerts.", icon="HeartHandshake", color="green"),
            PersonaInfo(role=UserRole.SECURITY, name="Security", description="Crowd alerts, incidents.", icon="Shield", color="red"),
            PersonaInfo(role=UserRole.MEDICAL, name="Medical", description="Health incidents.", icon="Cross", color="red"),
            PersonaInfo(role=UserRole.OPERATIONS, name="Operations", description="Pulse, overall status.", icon="Activity", color="purple"),
            PersonaInfo(role=UserRole.VENDOR, name="Vendor", description="Queues, stock.", icon="Store", color="orange"),
            PersonaInfo(role=UserRole.CLEANING, name="Cleaning", description="Waste, maintenance.", icon="Trash", color="green"),
            PersonaInfo(role=UserRole.TRANSPORT, name="Transport", description="Parking, traffic.", icon="Bus", color="yellow"),
            PersonaInfo(role=UserRole.VIP, name="VIP", description="Concierge, special access.", icon="Star", color="gold"),
            PersonaInfo(role=UserRole.MEDIA, name="Media", description="Press info, stats.", icon="Camera", color="blue"),
        ]

auth_service = AuthService()
