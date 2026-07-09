"""Auth Router."""
from fastapi import APIRouter, Depends
from typing import List

from core.security import get_current_user, DemoUser
from .models import LoginRequest, LoginResponse, PersonaInfo
from .service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    return await auth_service.login(request.role)

@router.get("/personas", response_model=List[PersonaInfo])
async def get_personas():
    return await auth_service.get_personas()

@router.get("/me", response_model=DemoUser)
async def get_me(user: DemoUser = Depends(get_current_user)):
    return user
