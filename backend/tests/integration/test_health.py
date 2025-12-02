"""Integration tests for health check endpoints.

TDD: RED phase - these tests should FAIL until T051 is implemented.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Integration tests for GET /health endpoint (T050-T051)."""

    @pytest.mark.integration
    def test_health_returns_200(self) -> None:
        """GET /health should return 200 status."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from main import app

            client = TestClient(app)
            response = client.get("/health")

            assert response.status_code == 200

    @pytest.mark.integration
    def test_health_returns_status(self) -> None:
        """GET /health should return status field."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from main import app

            client = TestClient(app)
            response = client.get("/health")
            data = response.json()

            assert "status" in data
            assert data["status"] in ["healthy", "degraded", "unhealthy"]

    @pytest.mark.integration
    def test_health_returns_version(self) -> None:
        """GET /health should return version field."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from main import app

            client = TestClient(app)
            response = client.get("/health")
            data = response.json()

            assert "version" in data


class TestReadyEndpoint:
    """Integration tests for GET /ready endpoint."""

    @pytest.mark.integration
    def test_ready_returns_200_when_healthy(self) -> None:
        """GET /ready should return 200 when all dependencies are healthy."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from main import app

            client = TestClient(app)
            response = client.get("/ready")

            assert response.status_code == 200

    @pytest.mark.integration
    def test_ready_checks_dependencies(self) -> None:
        """GET /ready should check all dependencies."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from main import app

            client = TestClient(app)
            response = client.get("/ready")
            data = response.json()

            # Should return status
            assert "status" in data
