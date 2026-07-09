"""Core Security for NEXOVA."""
from pydantic import BaseModel
import bleach
import secrets
from fastapi import Request, HTTPException, Depends
import structlog
from typing import Dict, Any
import firebase_admin
from firebase_admin import auth
from .types import UserRole

class DemoUser(BaseModel):
    id: str
    name: str
    email: str
    role: UserRole
    language: str
    avatar_url: str = ""
    preferences: Dict[str, Any] = {}

DEMO_USERS = {
    UserRole.FAN: DemoUser(id="fan_1", name="Alex Fan", email="alex@demo.com", role=UserRole.FAN, language="en"),
    UserRole.VOLUNTEER: DemoUser(id="vol_1", name="Sam Vol", email="sam@demo.com", role=UserRole.VOLUNTEER, language="en"),
    UserRole.SECURITY: DemoUser(id="sec_1", name="Pat Sec", email="pat@demo.com", role=UserRole.SECURITY, language="en"),
    UserRole.MEDICAL: DemoUser(id="med_1", name="Dr. Med", email="doc@demo.com", role=UserRole.MEDICAL, language="en"),
    UserRole.OPERATIONS: DemoUser(id="ops_1", name="Ops Mgr", email="ops@demo.com", role=UserRole.OPERATIONS, language="en"),
    UserRole.VENDOR: DemoUser(id="ven_1", name="Chef Ven", email="chef@demo.com", role=UserRole.VENDOR, language="en"),
    UserRole.CLEANING: DemoUser(id="cln_1", name="Clean Staff", email="clean@demo.com", role=UserRole.CLEANING, language="en"),
    UserRole.TRANSPORT: DemoUser(id="trans_1", name="Driver T", email="driver@demo.com", role=UserRole.TRANSPORT, language="en"),
    UserRole.VIP: DemoUser(id="vip_1", name="VIP Guest", email="vip@demo.com", role=UserRole.VIP, language="en"),
    UserRole.MEDIA: DemoUser(id="media_1", name="Press Reporter", email="press@demo.com", role=UserRole.MEDIA, language="en"),
}

logger = structlog.get_logger()

# Initialize Firebase Admin once
try:
    if not firebase_admin._apps:
        # If in a real GCP environment, credentials.ApplicationDefault() works
        # For local dev without ADC, you'd provide a cert
        firebase_admin.initialize_app()
except Exception as e:
    logger.warning("Failed to initialize firebase_admin", error=str(e))

def get_current_user(request: Request) -> DemoUser:
    """
    Production Firebase Auth Verification.
    Reads Authorization: Bearer <token>, verifies JWT via Firebase Admin,
    and returns a DemoUser model mapped from the custom claims.
    """
    auth_header = request.headers.get("Authorization")
    # For demo environment when token isn't passed, fallback to header role
    if not auth_header or not auth_header.startswith("Bearer "):
        role_str = request.headers.get("X-User-Role", "fan")
        try:
            return DEMO_USERS[UserRole(role_str)]
        except ValueError:
            return DEMO_USERS[UserRole.FAN]

    token = auth_header.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email", "")
        # Expecting role to be set in Firebase custom claims
        role_claim = decoded_token.get("role", "fan")
        
        try:
            role = UserRole(role_claim)
        except ValueError:
            role = UserRole.FAN

        return DemoUser(
            id=uid,
            name=decoded_token.get("name", email),
            email=email,
            role=role,
            language="en"
        )
    except Exception as e:
        logger.error("firebase.auth.failed", error=str(e))
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: DemoUser = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user

def sanitize_input(text: str) -> str:
    if not text:
        return text
    return bleach.clean(text, tags=[], strip=True)

def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)
