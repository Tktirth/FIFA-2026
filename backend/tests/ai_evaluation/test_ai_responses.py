import pytest
from unittest.mock import AsyncMock, MagicMock
from features.incidents.service import IncidentService
from features.incidents.models import IncidentCreate, IncidentAnalysis
from core.types import IncidentType, UserRole, Severity

@pytest.mark.asyncio
async def test_ai_incident_priority_assignment():
    """Evaluate that the IncidentService correctly parses Vertex AI structured output."""
    mock_repo = AsyncMock()
    mock_repo.create.return_value = "test-incident-123"
    
    mock_ai = AsyncMock()
    
    # Simulate a deterministic Vertex AI response
    mock_ai.generate_structured.return_value = IncidentAnalysis(
        severity=Severity.HIGH,
        summary="Visitor collapsed with potential cardiac event.",
        recommended_actions=[
            "Dispatch medical team immediately",
            "Clear surrounding area",
            "Prepare AED"
        ]
    )
    
    service = IncidentService(repo=mock_repo, ai_client=mock_ai)
    
    req = IncidentCreate(
        type=IncidentType.MEDICAL,
        description="Visitor collapsed near concession stand 4. Unresponsive.",
        zone_id="ZONE-SOUTH-02",
        reporter_role=UserRole.MEDICAL,
        reporter_id="sim-user-med-01"
    )
    
    incident = await service.create_incident(req)
    
    # Verification
    mock_ai.generate_structured.assert_called_once()
    assert incident.severity == Severity.HIGH
    assert incident.ai_summary == "Visitor collapsed with potential cardiac event."
    assert len(incident.ai_recommended_actions) == 3
    
    # Assert timeline generation incorporates AI decision
    assert len(incident.timeline) == 2
    assert incident.timeline[1].actor == "NEXOVA_AI"
    assert "HIGH" in incident.timeline[1].action
