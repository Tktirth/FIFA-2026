import structlog
from fastapi import Depends
from .models import NavigationRequest, NavigationResponse
from intelligence.gemini_client import NexovaAI
from core.dependencies import get_gemini_client

logger = structlog.get_logger()

class NavigationService:
    def __init__(
        self,
        ai_client: NexovaAI = Depends(get_gemini_client)
    ):
        self.ai_client = ai_client

    async def calculate_route(self, req: NavigationRequest) -> NavigationResponse:
        """Calculate optimal stadium routes, using AI to parse dynamic conditions."""
        # In a real app we'd query graph data and crowd data here.
        # We pass it to the AI to construct the route steps dynamically.
        
        prompt = f"""
        Generate navigation instructions for a stadium.
        From: {req.from_zone}
        To: {req.to_zone}
        Needs Accessibility: {req.accessibility_required}
        Walking Speed: {req.walking_speed}
        
        Provide the primary route steps and one alternative. Ensure distance matches estimated time.
        """
        
        # We use Flash for simple path generation (speed is critical here)
        return await self.ai_client.generate_structured(
            prompt=prompt,
            response_schema=NavigationResponse,
            system_instruction="You are a real-time stadium navigation engine.",
            complexity="low"
        )
