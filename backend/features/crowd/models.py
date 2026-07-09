from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from core.types import ZoneId

class ZoneDensity(BaseModel):
    zone_id: ZoneId
    current_occupancy: int
    capacity: int
    percentage: float
    level: str = Field(description="LOW, MODERATE, HIGH, CRITICAL")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CrowdPredictionResult(BaseModel):
    predicted_occupancy: int
    trend: str = Field(description="INCREASING, DECREASING, STABLE")
    explanation: str = Field(description="AI explanation for the predicted trend based on match context")
    suggested_mitigations: List[str]

class CrowdPrediction(BaseModel):
    zone_id: ZoneId
    prediction_for_time: datetime
    result: CrowdPredictionResult

class HeatMapData(BaseModel):
    timestamp: datetime
    zones: List[ZoneDensity]
