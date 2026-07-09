import structlog
from datetime import datetime, timedelta, timezone
from typing import Dict
from fastapi import Depends
from .models import ZoneDensity, CrowdPrediction, CrowdPredictionResult, HeatMapData
from .repository import CrowdRepository
from intelligence.gemini_client import NexovaAI
from core.dependencies import get_gemini_client
from core.cache import async_cache

logger = structlog.get_logger()

# Mock capacities for demo purposes
ZONE_CAPACITIES = {
    "north_gate": 5000,
    "south_gate": 5000,
    "food_court_a": 2000,
    "merch_shop_1": 500,
    "vip_lounge": 300,
    "medical_tent": 50,
}

class CrowdService:
    def __init__(
        self,
        repo: CrowdRepository = Depends(),
        ai_client: NexovaAI = Depends(get_gemini_client)
    ):
        self.repo = repo
        self.ai_client = ai_client

    def _calculate_level(self, percentage: float) -> str:
        if percentage > 90:
            return "CRITICAL"
        if percentage > 75:
            return "HIGH"
        if percentage > 50:
            return "MODERATE"
        return "LOW"

    async def record_density(self, zone_id: str, occupancy: int) -> ZoneDensity:
        """Record the current density of a zone (usually called by IoT sensors)."""
        capacity = ZONE_CAPACITIES.get(zone_id, 1000)
        percentage = min(100.0, (occupancy / capacity) * 100)
        
        density = ZoneDensity(
            zone_id=zone_id,
            current_occupancy=occupancy,
            capacity=capacity,
            percentage=percentage,
            level=self._calculate_level(percentage)
        )
        await self.repo.create(density)
        return density

    @async_cache(ttl=5)
    async def get_current_heatmap(self) -> HeatMapData:
        """Get the latest density for all zones."""
        # In a real app we'd query the latest timestamp for each zone.
        # For this prototype, we'll fetch recent records.
        all_data = await self.repo.list_all(limit=100)
        
        # Deduplicate to get the latest per zone
        latest_zones: Dict[str, ZoneDensity] = {}
        for d in all_data:
            if d.zone_id not in latest_zones or d.timestamp > latest_zones[d.zone_id].timestamp:
                latest_zones[d.zone_id] = d
                
        return HeatMapData(
            timestamp=datetime.now(timezone.utc),
            zones=list(latest_zones.values())
        )

    @async_cache(ttl=60)
    async def predict_crowd(self, zone_id: str, minutes_ahead: int = 30) -> CrowdPrediction:
        """Use AI to predict crowd flow for a specific zone based on contextual data."""
        # Get historical context
        history = await self.repo.query({"zone_id": zone_id}, limit=10)
        history_summary = ", ".join([f"{h.current_occupancy} at {h.timestamp.strftime('%H:%M')}" for h in history])
        
        prompt = f"""
        Predict crowd density for zone: {zone_id} in {minutes_ahead} minutes.
        Current capacity: {ZONE_CAPACITIES.get(zone_id, 1000)}
        Recent history (occupancy): {history_summary}
        Context: Halftime is approaching in 15 minutes.
        
        Provide the predicted occupancy, trend, explanation, and mitigations.
        """
        
        result = await self.ai_client.generate_structured(
            prompt=prompt,
            response_schema=CrowdPredictionResult,
            system_instruction="You are a stadium crowd dynamics predictor.",
            complexity="high" # Pro model for reasoning
        )
        
        return CrowdPrediction(
            zone_id=zone_id,
            prediction_for_time=datetime.now(timezone.utc) + timedelta(minutes=minutes_ahead),
            result=result
        )
