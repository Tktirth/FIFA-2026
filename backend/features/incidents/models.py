from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from core.types import Severity, IncidentType, ZoneId

class IncidentStatus(str, Enum):
    REPORTED = "REPORTED"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    FALSE_ALARM = "FALSE_ALARM"

class IncidentCreate(BaseModel):
    type: IncidentType
    description: str
    zone_id: ZoneId
    reporter_id: str
    reporter_role: str
    media_urls: List[str] = Field(default_factory=list)

class IncidentUpdate(BaseModel):
    status: Optional[IncidentStatus] = None
    severity: Optional[Severity] = None
    assigned_to: Optional[str] = None
    resolution_notes: Optional[str] = None

class IncidentAnalysis(BaseModel):
    summary: str = Field(description="A brief, professional 1-2 sentence summary of the incident")
    severity: Severity = Field(description="The calculated severity based on the context and description")
    recommended_actions: List[str] = Field(description="List of immediate actions to take")
    is_emergency: bool = Field(description="True if this requires immediate stadium-wide escalation")

class TimelineEvent(BaseModel):
    timestamp: datetime
    action: str
    actor: str

class Incident(BaseModel):
    id: Optional[str] = None
    type: IncidentType
    description: str
    zone_id: ZoneId
    status: IncidentStatus = IncidentStatus.REPORTED
    severity: Severity = Severity.LOW
    
    # AI generated fields
    ai_summary: Optional[str] = None
    ai_recommended_actions: List[str] = Field(default_factory=list)
    
    # Tracking
    reporter_id: str
    reporter_role: str
    assigned_to: Optional[str] = None
    timeline: List[TimelineEvent] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class IncidentStats(BaseModel):
    total_active: int
    critical_count: int
    by_type: Dict[str, int]
    by_zone: Dict[str, int]
