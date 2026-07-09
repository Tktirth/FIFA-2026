"""Sustainability Router."""
from fastapi import APIRouter, Depends
from core.security import get_current_user, DemoUser

router = APIRouter(prefix="/sustainability", tags=["Sustainability"])

@router.get("/dashboard")
async def get_dashboard(user: DemoUser = Depends(get_current_user)):
    return {"status": "ok", "metrics": {}}
