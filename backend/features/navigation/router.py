from fastapi import APIRouter, Depends
from .models import NavigationRequest, NavigationResponse
from .service import NavigationService
from core.security import DemoUser, get_current_user

router = APIRouter(prefix="/navigation", tags=["Navigation"])

@router.post("/route", response_model=NavigationResponse)
async def calculate_route(
    req: NavigationRequest,
    service: NavigationService = Depends(),
    user: DemoUser = Depends(get_current_user)
):
    """Calculate a route between two zones. (Accessible by all roles)"""
    return await service.calculate_route(req)
