"""
NEXOVA — Unit tests for core modules and features.
"""

from __future__ import annotations
from fastapi.testclient import TestClient

from core.types import UserRole, Severity, IncidentType
from core.security import DEMO_USERS, sanitize_input, generate_csrf_token

class TestUserRole:
    def test_all_roles_defined(self) -> None:
        assert len(UserRole) == 10

class TestSeverity:
    def test_severity_ordering(self) -> None:
        assert Severity.LOW.value == "low"

class TestIncidentType:
    def test_all_types(self) -> None:
        assert len(IncidentType) == 6

class TestDemoUsers:
    def test_all_roles_have_users(self) -> None:
        for role in UserRole:
            assert role in DEMO_USERS

class TestSanitizeInput:
    def test_strips_script_tags(self) -> None:
        result = sanitize_input("<script>alert('xss')</script>hello")
        assert "<script>" not in result
        assert "hello" in result

class TestCSRFToken:
    def test_generates_token(self) -> None:
        assert len(generate_csrf_token()) > 20

class TestHealthCheck:
    def test_health_returns_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

class TestAuthEndpoints:
    def test_get_personas(self, client: TestClient) -> None:
        response = client.get("/api/v1/auth/personas")
        assert response.status_code == 200

    def test_get_me(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/auth/me",
            headers={"X-User-Role": "security"},
        )
        assert response.status_code == 200
        assert response.json()["role"] == "security"

class TestCrowdEndpoints:
    def test_get_heatmap(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/crowd/heatmap",
            headers={"X-User-Role": "operations"},
        )
        assert response.status_code == 200

    def test_post_density(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/crowd/zones/north_gate/density",
            json={"occupancy": 500},
            headers={"X-User-Role": "operations"},
        )
        assert response.status_code == 200

class TestIncidentEndpoints:
    def test_create_incident(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/incidents/",
            json={
                "type": "security",
                "description": "Lost child near gate B",
                "zone_id": "gate-b",
                "reporter_id": "none",
                "reporter_role": "fan",
                "media_urls": []
            },
            headers={"X-User-Role": "security"},
        )
        assert response.status_code in (200, 201)

    def test_list_incidents(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/incidents/",
            headers={"X-User-Role": "security"},
        )
        assert response.status_code == 200

class TestNavigationEndpoints:
    def test_navigate(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/navigation/route",
            json={
                "from_zone": "gate-a",
                "to_zone": "section-120",
                "accessibility_required": False,
                "walking_speed": "AVERAGE"
            },
            headers={"X-User-Role": "fan"},
        )
        assert response.status_code == 200

class TestSecurityHeaders:
    def test_csp_header(self, client: TestClient) -> None:
        response = client.get("/health")
        assert "content-security-policy" in response.headers
