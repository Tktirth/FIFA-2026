"""Pulse Router."""
from fastapi import APIRouter, Depends
from core.security import get_current_user, DemoUser

router = APIRouter(prefix="/pulse", tags=["Pulse"])

@router.get("/")
async def get_pulse(user: DemoUser = Depends(get_current_user)):
    return {"status": "ok", "score": 98}
