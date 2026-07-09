"""Gemini API Client Wrapper with Model Routing."""
from google import genai
from google.genai.types import GenerateContentConfig
from typing import Type, TypeVar, Optional
from pydantic import BaseModel
import structlog
import time

logger = structlog.get_logger()
T = TypeVar("T", bound=BaseModel)

class NexovaAI:
    def __init__(self, project_id: str, location: str, default_model: str, enabled: bool = True):
        self.enabled = enabled
        self.default_model = default_model
        
        # In a real app we'd load specific versions. For hackathon, we assume these are valid names.
        self.MODEL_PRO = "gemini-2.5-pro"
        self.MODEL_FLASH = "gemini-2.5-flash"
        
        if enabled:
            # Note: For strict google-genai we pass vertexai=True. 
            self._client = genai.Client(vertexai=True, project=project_id, location=location)

    def _select_model(self, model_override: Optional[str], complexity: str = "low") -> str:
        """Route to appropriate model based on complexity if not explicitly overridden."""
        if model_override:
            return model_override
        if complexity == "high":
            return self.MODEL_PRO
        return self.MODEL_FLASH

    async def generate_text(self, prompt: str, system_instruction: Optional[str] = None, model: Optional[str] = None, complexity: str = "low") -> str:
        if not self.enabled:
            return "AI response placeholder (Simulation Mode)"
            
        target_model = self._select_model(model, complexity)
        start = time.time()
        
        config = GenerateContentConfig(system_instruction=system_instruction) if system_instruction else None
        
        try:
            response = await self._client.aio.models.generate_content(
                model=target_model,
                contents=prompt,
                config=config
            )
            duration = time.time() - start
            logger.info("ai_call", model=target_model, duration=duration, type="text")
            return response.text or ""
        except Exception as e:
            logger.error("ai_error", error=str(e), model=target_model)
            return "AI fallback response due to error."

    async def generate_structured(self, prompt: str, response_schema: Type[T], system_instruction: Optional[str] = None, model: Optional[str] = None, complexity: str = "high") -> T:
        """Generate strictly typed JSON matching the provided Pydantic model."""
        if not self.enabled:
            # Attempt to instantiate with empty/default fields for fallback
            return response_schema.model_construct()
            
        target_model = self._select_model(model, complexity)
        start = time.time()
        
        # The new SDK supports response_schema directly
        config = GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=response_schema
        )
        
        try:
            response = await self._client.aio.models.generate_content(
                model=target_model,
                contents=prompt,
                config=config
            )
            duration = time.time() - start
            logger.info("ai_call", model=target_model, duration=duration, type="structured")
            
            # response.parsed contains the Pydantic model if the SDK parsed it, 
            # otherwise we parse response.text manually.
            if hasattr(response, 'parsed') and response.parsed is not None:
                if isinstance(response.parsed, response_schema):
                    return response.parsed
                # Sometimes it returns a dict depending on SDK version
                if isinstance(response.parsed, dict):
                    return response_schema.model_validate(response.parsed)
            
            # Fallback to parsing text manually
            raw_text = response.text or "{}"
            # Strip markdown JSON blocks if present
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:-3].strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:-3].strip()
                
            return response_schema.model_validate_json(raw_text)
            
        except Exception as e:
            logger.error("ai_error", error=str(e), model=target_model, context="generate_structured")
            return response_schema.model_construct()

    async def translate(self, text: str, target_language: str, context: str = "FIFA World Cup") -> str:
        if not self.enabled:
            return text
            
        prompt = f"Translate the following text to {target_language}. Context: {context}\n\nText: {text}"
        # Flash is more than sufficient for translation
        return await self.generate_text(
            prompt=prompt, 
            system_instruction="You are a professional translator for a global sporting event. Return ONLY the translated text.",
            complexity="low"
        )

    async def summarize(self, text: str, max_length: int = 200, complexity: str = "low") -> str:
        if not self.enabled:
            return text[:max_length] + "..." if len(text) > max_length else text
            
        prompt = f"Summarize this in under {max_length} characters:\n\n{text}"
        return await self.generate_text(
            prompt=prompt,
            system_instruction="You are a precise summarization engine. Return ONLY the summary, adhering to the character limit.",
            complexity=complexity
        )
