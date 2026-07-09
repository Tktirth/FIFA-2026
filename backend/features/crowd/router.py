from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from .models import HeatMapData, CrowdPrediction, ZoneDensity
from .service import CrowdService
from core.security import DemoUser, get_current_user

router = APIRouter(prefix="/crowd", tags=["Crowd"])

class DensityUpdate(BaseModel):
    occupancy: int

@router.get("/heatmap", response_model=HeatMapData)
async def get_heatmap(
    service: CrowdService = Depends(),
    user: DemoUser = Depends(get_current_user)
):
    """Get current stadium density heatmap."""
    return await service.get_current_heatmap()

@router.post("/zones/{zone_id}/density", response_model=ZoneDensity)
async def update_density(
    zone_id: str,
    data: DensityUpdate,
    service: CrowdService = Depends(),
    user: DemoUser = Depends(get_current_user)
):
    """Simulate IoT sensor density updates (Requires OPERATIONS role)."""
    if user.role.value != "operations":
        raise HTTPException(status_code=403, detail="IoT update restricted")
    return await service.record_density(zone_id, data.occupancy)

@router.get("/zones/{zone_id}/predict", response_model=CrowdPrediction)
async def predict_crowd(
    zone_id: str,
    minutes: int = 30,
    service: CrowdService = Depends(),
    user: DemoUser = Depends(get_current_user)
):
    """Get AI prediction for future crowd flow in a zone."""
    return await service.predict_crowd(zone_id, minutes_ahead=minutes)
