from pydantic import BaseModel, Field
from typing import List, Optional
from core.types import ZoneId

class RouteStep(BaseModel):
    instruction: str
    distance_m: int
    zone_id: Optional[ZoneId] = None

class Route(BaseModel):
    steps: List[RouteStep]
    total_distance_m: int
    estimated_minutes: int
    crowd_level: str = "LOW"
    accessibility_friendly: bool = True

class NavigationRequest(BaseModel):
    from_zone: ZoneId
    to_zone: ZoneId
    accessibility_required: bool = False
    walking_speed: str = "AVERAGE"

class NavigationResponse(BaseModel):
    primary_route: Route
    alternatives: List[Route] = Field(default_factory=list)
