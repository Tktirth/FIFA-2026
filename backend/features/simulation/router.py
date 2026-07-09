from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from features.incidents.service import IncidentService
from features.incidents.models import IncidentCreate
from core.types import IncidentType, UserRole, Severity

router = APIRouter(prefix="/simulation", tags=["Simulation"])

class ScenarioRequest(BaseModel):
    scenario_name: str

SCENARIOS = {
    "medical_emergency": {
        "type": IncidentType.MEDICAL,
        "zone_id": "ZONE-SOUTH-02",
        "description": "Visitor collapsed near concession stand 4. Unresponsive, possible cardiac event. Crowd gathering.",
        "reporter_role": UserRole.MEDICAL,
        "reporter_id": "sim-user-med-01"
    },
    "fire_food_court": {
        "type": IncidentType.FIRE,
        "zone_id": "ZONE-EAST-01",
        "description": "Small grease fire reported in kitchen of Burger Stall 2. Thick smoke filling the concourse.",
        "reporter_role": UserRole.VENDOR,
        "reporter_id": "sim-user-vendor-02"
    },
    "security_threat": {
        "type": IncidentType.SECURITY,
        "zone_id": "ZONE-VIP-01",
        "description": "Unattended suspicious package located near the VIP entrance scanner. No owner identified.",
        "reporter_role": UserRole.SECURITY,
        "reporter_id": "sim-user-sec-01"
    },
    "crowd_crush": {
        "type": IncidentType.CROWD,
        "zone_id": "ZONE-NORTH-04",
        "description": "Severe bottleneck at North Exit 4. Escalators stopped working, people are pushing, risk of crushing.",
        "reporter_role": UserRole.OPERATIONS,
        "reporter_id": "sim-user-ops-01"
    }
}

@router.post("/scenario", status_code=status.HTTP_201_CREATED)
async def trigger_scenario(
    req: ScenarioRequest,
    incident_service: IncidentService = Depends()
):
    """Trigger a deterministic demonstration scenario."""
    if req.scenario_name not in SCENARIOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown scenario. Available: {list(SCENARIOS.keys())}"
        )

    scenario_data = SCENARIOS[req.scenario_name]
    
    # We create the incident exactly as if a user submitted it via the app.
    # The IncidentService will trigger Vertex AI to generate the summary, severity, and timeline.
    create_req = IncidentCreate(
        type=scenario_data["type"],
        description=scenario_data["description"],
        zone_id=scenario_data["zone_id"],
        reporter_role=scenario_data["reporter_role"],
        reporter_id=scenario_data["reporter_id"]
    )
    
    incident = await incident_service.create_incident(create_req)
    
    return {
        "status": "success",
        "scenario_triggered": req.scenario_name,
        "incident_id": incident.id,
        "ai_severity_assigned": incident.severity.value,
        "ai_summary": incident.ai_summary
    }
