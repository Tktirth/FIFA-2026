import structlog
from datetime import datetime, timezone
from typing import List
from fastapi import Depends
from .models import IncidentCreate, IncidentUpdate, Incident, IncidentStatus, TimelineEvent, IncidentAnalysis
from .repository import IncidentRepository
from intelligence.gemini_client import NexovaAI
from core.dependencies import get_gemini_client
from core.exceptions import NotFoundError

logger = structlog.get_logger()

class IncidentService:
    def __init__(
        self, 
        repo: IncidentRepository = Depends(),
        ai_client: NexovaAI = Depends(get_gemini_client)
    ):
        self.repo = repo
        self.ai_client = ai_client

    async def create_incident(self, data: IncidentCreate) -> Incident:
        """Create a new incident, leveraging AI for priority and summarization."""
        # AI Analysis (Pro model)
        prompt = f"""
        Analyze this stadium incident report:
        Type: {data.type.value}
        Zone: {data.zone_id}
        Description: {data.description}
        Reporter Role: {data.reporter_role}
        
        Determine the severity, write a concise summary, and list 3 recommended actions.
        """
        
        analysis = await self.ai_client.generate_structured(
            prompt=prompt,
            response_schema=IncidentAnalysis,
            system_instruction="You are an expert stadium operations AI. Provide structured JSON analysis of incidents.",
            complexity="high" # Routes to gemini-2.5-pro
        )

        timeline = [
            TimelineEvent(
                timestamp=datetime.now(timezone.utc),
                action="Incident reported",
                actor=data.reporter_id
            ),
            TimelineEvent(
                timestamp=datetime.now(timezone.utc),
                action=f"AI assigned severity: {analysis.severity.value}",
                actor="NEXOVA_AI"
            )
        ]

        incident = Incident(
            type=data.type,
            description=data.description,
            zone_id=data.zone_id,
            severity=analysis.severity,
            ai_summary=analysis.summary,
            ai_recommended_actions=analysis.recommended_actions,
            reporter_id=data.reporter_id,
            reporter_role=data.reporter_role,
            timeline=timeline
        )

        incident_id = await self.repo.create(incident)
        incident.id = incident_id
        
        logger.info("incident_created", incident_id=incident_id, severity=analysis.severity.value)
        return incident

    async def get_incident(self, incident_id: str) -> Incident:
        incident = await self.repo.get_by_id(incident_id)
        if not incident:
            raise NotFoundError(detail=f"Incident {incident_id} not found")
        return incident

    async def update_incident(self, incident_id: str, data: IncidentUpdate, actor_id: str) -> Incident:
        incident = await self.get_incident(incident_id)
        
        update_data = data.model_dump(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.now(timezone.utc)
            await self.repo.update(incident_id, update_data)
            
            # Update timeline in memory to return accurate model
            for k, v in update_data.items():
                if k != "updated_at":
                    incident.timeline.append(TimelineEvent(
                        timestamp=datetime.now(timezone.utc),
                        action=f"Updated {k} to {v}",
                        actor=actor_id
                    ))
            
            await self.repo.update(incident_id, {"timeline": [t.model_dump() for t in incident.timeline]})
            
        return await self.get_incident(incident_id)

    async def list_active_incidents(self) -> List[Incident]:
        """List all incidents not resolved or false alarm."""
        # Firestore query
        all_incidents = await self.repo.list_all(limit=500)
        return [i for i in all_incidents if i.status not in (IncidentStatus.RESOLVED, IncidentStatus.FALSE_ALARM)]
