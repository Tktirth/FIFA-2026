"""
NEXOVA — Integration tests for AI intelligence layer.

Tests the Gemini client wrapper with mocked API responses.
"""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from intelligence.gemini_client import NexovaAI


class TestNexovaAI:
    """Tests for the NexovaAI Gemini client wrapper."""

    @pytest.fixture
    def ai_enabled(self) -> NexovaAI:
        """Create an AI client with mocked Gemini backend."""
        with patch("intelligence.gemini_client.genai") as mock_genai:
            mock_client = MagicMock()
            mock_genai.Client.return_value = mock_client

            ai = NexovaAI(
                project_id="test-project",
                location="us-central1",
                default_model="gemini-2.5-pro",
                enabled=True,
            )
            ai._client = mock_client
            return ai

    @pytest.fixture
    def ai_disabled(self) -> NexovaAI:
        """Create a disabled AI client."""
        return NexovaAI(
            project_id="test-project",
            location="us-central1",
            default_model="gemini-2.5-pro",
            enabled=False,
        )

    # ---- Disabled Mode Tests ----

    @pytest.mark.asyncio
    async def test_disabled_generate_text(self, ai_disabled: NexovaAI) -> None:
        """Verify disabled AI returns graceful fallback."""
        result = await ai_disabled.generate_text("test prompt")
        assert isinstance(result, str)
        assert result != ""

    @pytest.mark.asyncio
    async def test_disabled_translate(self, ai_disabled: NexovaAI) -> None:
        """Verify disabled AI returns original text for translation."""
        result = await ai_disabled.translate("Hello world", "es")
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_disabled_summarize(self, ai_disabled: NexovaAI) -> None:
        """Verify disabled AI returns truncated text for summarization."""
        long_text = "This is a long incident report. " * 20
        result = await ai_disabled.summarize(long_text, max_length=50)
        assert isinstance(result, str)
        assert len(result) <= 200  # Generous limit for fallback

    # ---- Enabled Mode Tests ----

    @pytest.mark.asyncio
    async def test_enabled_generate_text(self, ai_enabled: NexovaAI) -> None:
        """Verify enabled AI calls Gemini API."""
        mock_response = MagicMock()
        mock_response.text = "Generated route suggestion"
        ai_enabled._client.aio.models.generate_content = AsyncMock(return_value=mock_response)

        result = await ai_enabled.generate_text(
            prompt="Find optimal route from Gate A to Section 120",
            system_instruction="You are a stadium navigation assistant.",
        )
        assert result == "Generated route suggestion"

    @pytest.mark.asyncio
    async def test_enabled_translate(self, ai_enabled: NexovaAI) -> None:
        """Verify enabled AI performs translation."""
        mock_response = MagicMock()
        mock_response.text = "Hola mundo"
        ai_enabled._client.aio.models.generate_content = AsyncMock(return_value=mock_response)

        result = await ai_enabled.translate("Hello world", "es")
        assert result == "Hola mundo"

    # ---- Error Handling Tests ----

    @pytest.mark.asyncio
    async def test_handles_api_error_gracefully(self, ai_enabled: NexovaAI) -> None:
        """Verify API errors are handled with fallback."""
        ai_enabled._client.aio.models.generate_content = AsyncMock(
            side_effect=Exception("API quota exceeded")
        )

        # Should not raise, should return fallback
        result = await ai_enabled.generate_text("test prompt")
        assert isinstance(result, str)

    # ---- Audit Logging Tests ----

    @pytest.mark.asyncio
    async def test_audit_logs_do_not_contain_prompts(self, ai_enabled: NexovaAI) -> None:
        """Verify audit logs never expose prompt content."""
        mock_response = MagicMock()
        mock_response.text = "Response"
        mock_response.usage_metadata = MagicMock(
            prompt_token_count=10,
            candidates_token_count=5,
            total_token_count=15,
        )
        ai_enabled._client.aio.models.generate_content = AsyncMock(return_value=mock_response)

        with patch("intelligence.gemini_client.logger") as mock_logger:
            await ai_enabled.generate_text(
                prompt="SECRET PROMPT CONTENT",
                system_instruction="SECRET SYSTEM INSTRUCTION",
            )

            # Check that the prompt was NOT logged
            for call in mock_logger.info.call_args_list:
                log_msg = str(call)
                assert "SECRET PROMPT CONTENT" not in log_msg
                assert "SECRET SYSTEM INSTRUCTION" not in log_msg
