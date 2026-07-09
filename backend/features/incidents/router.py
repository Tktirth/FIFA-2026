from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .models import Incident, IncidentCreate, IncidentUpdate
from .service import IncidentService
from core.security import DemoUser, get_current_user

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.post("/", response_model=Incident, status_code=201)
async def create_incident(
    data: IncidentCreate,
    service: IncidentService = Depends(),
    user: DemoUser = Depends(get_current_user)
):
    """Report a new incident (Applies to all roles, but AI triages priority)."""
    # Override reporter with authenticated user
    data.reporter_id = user.id
    data.reporter_role = user.role.value
    return await service.create_incident(data)

@router.get("/", response_model=List[Incident])
async def list_active_incidents(
    service: IncidentService = Depends(),
    user: DemoUser = Depends(get_current_user)
):
    """Get active incidents (SECURITY, OPERATIONS, MEDICAL only)."""
    if user.role.value not in ["security", "operations", "medical"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return await service.list_active_incidents()

@router.get("/{incident_id}", response_model=Incident)
async def get_incident(
    incident_id: str,
    service: IncidentService = Depends(),
    user: DemoUser = Depends(get_current_user)
):
    return await service.get_incident(incident_id)

@router.patch("/{incident_id}", response_model=Incident)
async def update_incident(
    incident_id: str,
    data: IncidentUpdate,
    service: IncidentService = Depends(),
    user: DemoUser = Depends(get_current_user)
):
    return await service.update_incident(incident_id, data, actor_id=user.id)
