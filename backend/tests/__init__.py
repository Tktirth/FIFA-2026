"""
NEXOVA Backend Test Configuration.

Provides shared fixtures for unit, integration, and API tests.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from config.settings import Settings
from core.security import DemoUser, DEMO_USERS
from core.types import UserRole


# ---- Event Loop ----


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create a session-scoped event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ---- Settings ----


@pytest.fixture
def test_settings() -> Settings:
    """Create test settings with AI and simulation disabled."""
    return Settings(
        GCP_PROJECT_ID="nexova-test",
        GCP_REGION="us-central1",
        GEMINI_MODEL="gemini-2.5-pro",
        BACKEND_ENV="test",
        BACKEND_PORT=8080,
        BACKEND_CORS_ORIGINS="http://localhost:3000",
        BACKEND_RATE_LIMIT="1000/minute",
        SECRET_KEY="test-secret-key-do-not-use-in-production",
        ENABLE_SIMULATION=True,
        ENABLE_AI=False,
        BACKEND_LOG_LEVEL="DEBUG",
    )


# ---- Mock Firestore ----


@pytest.fixture
def mock_firestore() -> MagicMock:
    """Create a mock Firestore client."""
    client = MagicMock()
    collection = MagicMock()
    document = MagicMock()

    # Setup chain: client.collection().document()
    client.collection.return_value = collection
    collection.document.return_value = document

    # Setup async methods
    document.get = AsyncMock(return_value=MagicMock(exists=True, to_dict=lambda: {}))
    document.set = AsyncMock()
    document.update = AsyncMock()
    document.delete = AsyncMock()
    collection.add = AsyncMock(return_value=(None, document))
    collection.get = AsyncMock(return_value=[])
    collection.where = MagicMock(return_value=collection)
    collection.order_by = MagicMock(return_value=collection)
    collection.limit = MagicMock(return_value=collection)
    collection.offset = MagicMock(return_value=collection)
    collection.stream = AsyncMock(return_value=iter([]))

    return client


# ---- Mock Gemini ----


@pytest.fixture
def mock_gemini() -> MagicMock:
    """Create a mock NexovaAI client."""
    ai = MagicMock()
    ai.enabled = False
    ai.generate_text = AsyncMock(return_value="AI response placeholder")
    ai.generate_structured = AsyncMock(return_value={})
    ai.translate = AsyncMock(return_value="Translated text")
    ai.summarize = AsyncMock(return_value="Summary of the incident")
    ai.predict = AsyncMock(return_value={"prediction": "low_density"})
    return ai


# ---- Demo Users ----


@pytest.fixture
def fan_user() -> DemoUser:
    """Create a demo fan user."""
    return DEMO_USERS[UserRole.FAN]


@pytest.fixture
def security_user() -> DemoUser:
    """Create a demo security staff user."""
    return DEMO_USERS[UserRole.SECURITY]


@pytest.fixture
def operations_user() -> DemoUser:
    """Create a demo operations/event manager user."""
    return DEMO_USERS[UserRole.OPERATIONS]


@pytest.fixture
def volunteer_user() -> DemoUser:
    """Create a demo volunteer user."""
    return DEMO_USERS[UserRole.VOLUNTEER]


@pytest.fixture
def medical_user() -> DemoUser:
    """Create a demo medical staff user."""
    return DEMO_USERS[UserRole.MEDICAL]


# ---- FastAPI App ----


@pytest.fixture
def app(test_settings: Settings, mock_firestore: MagicMock, mock_gemini: MagicMock) -> FastAPI:
    """Create a FastAPI test app with mocked dependencies."""
    from main import create_app
    from core.dependencies import get_settings, get_firestore_client, get_gemini_client

    test_app = create_app()

    # Override dependencies
    test_app.dependency_overrides[get_settings] = lambda: test_settings
    test_app.dependency_overrides[get_firestore_client] = lambda: mock_firestore
    test_app.dependency_overrides[get_gemini_client] = lambda: mock_gemini

    return test_app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create a synchronous test client."""
    return TestClient(app)


@pytest.fixture
async def async_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ---- Helper Functions ----


def auth_headers(role: UserRole = UserRole.FAN) -> dict[str, str]:
    """Generate authentication headers for a given role."""
    return {
        "X-User-Role": role.value,
        "Content-Type": "application/json",
    }


# ---- Sample Data Factories ----


class SampleData:
    """Factory for generating sample test data."""

    @staticmethod
    def incident(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a sample incident."""
        data = {
            "type": "SECURITY",
            "description": "Unattended bag found near Gate B",
            "zone_id": "gate-b",
            "severity": "MEDIUM",
            "reporter_id": "security-001",
        }
        if overrides:
            data.update(overrides)
        return data

    @staticmethod
    def navigation_request(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a sample navigation request."""
        data = {
            "from_zone": "gate-a",
            "to_zone": "section-120",
            "accessibility": False,
            "walking_speed": "normal",
        }
        if overrides:
            data.update(overrides)
        return data

    @staticmethod
    def volunteer(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a sample volunteer."""
        data = {
            "id": "vol-001",
            "name": "Maria Garcia",
            "skills": ["first_aid", "crowd_management"],
            "languages": ["en", "es"],
            "zone": "gate-a",
            "available": True,
        }
        if overrides:
            data.update(overrides)
        return data

    @staticmethod
    def emergency(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a sample emergency."""
        data = {
            "type": "MEDICAL",
            "description": "Fan collapsed in Section 200",
            "zone_id": "section-200",
            "severity": "HIGH",
        }
        if overrides:
            data.update(overrides)
        return data

    @staticmethod
    def food_vendor(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
        """Create a sample food vendor."""
        data = {
            "id": "vendor-001",
            "name": "Stadium Burgers",
            "zone": "concourse-north",
            "type": "fast_food",
            "is_open": True,
            "current_queue_length": 12,
            "estimated_wait_minutes": 8,
        }
        if overrides:
            data.update(overrides)
        return data


@pytest.fixture
def sample_data() -> SampleData:
    """Provide access to sample data factories."""
    return SampleData()
