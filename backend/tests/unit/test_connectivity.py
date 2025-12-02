"""Unit tests for connectivity sanity-check utility.

TDD: Tests for T003a - Connectivity verification for OpenAI, Qdrant, Neon.
FR-ENV-002: System MUST provide connectivity sanity-check.
"""

import os
from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture
def mock_env():
    """Set up environment variables for tests."""
    env_vars = {
        "OPENAI_API_KEY": "sk-test-key",
        "QDRANT_URL": "https://test.qdrant.io",
        "QDRANT_API_KEY": "qdrant-key",
        "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        # Clear cached settings
        from core.config import get_settings
        get_settings.cache_clear()
        yield
        get_settings.cache_clear()


class TestConnectivityReport:
    """Tests for ConnectivityReport data structure."""

    def test_report_has_service_statuses(self) -> None:
        """ConnectivityReport should have status for each service."""
        from core.connectivity import ConnectivityReport, ServiceStatus

        report = ConnectivityReport(
            openai=ServiceStatus(healthy=True, message="Connected"),
            qdrant=ServiceStatus(healthy=True, message="Connected"),
            database=ServiceStatus(healthy=True, message="Connected"),
        )

        assert report.openai.healthy is True
        assert report.qdrant.healthy is True
        assert report.database.healthy is True

    def test_report_all_healthy_property(self) -> None:
        """ConnectivityReport.all_healthy should return True only if all services healthy."""
        from core.connectivity import ConnectivityReport, ServiceStatus

        # All healthy
        report = ConnectivityReport(
            openai=ServiceStatus(healthy=True, message="OK"),
            qdrant=ServiceStatus(healthy=True, message="OK"),
            database=ServiceStatus(healthy=True, message="OK"),
        )
        assert report.all_healthy is True

        # One unhealthy
        report_partial = ConnectivityReport(
            openai=ServiceStatus(healthy=True, message="OK"),
            qdrant=ServiceStatus(healthy=False, message="Connection refused"),
            database=ServiceStatus(healthy=True, message="OK"),
        )
        assert report_partial.all_healthy is False


class TestServiceStatus:
    """Tests for ServiceStatus data structure."""

    def test_service_status_fields(self) -> None:
        """ServiceStatus should have healthy flag and message."""
        from core.connectivity import ServiceStatus

        status = ServiceStatus(healthy=True, message="Connected successfully")
        assert status.healthy is True
        assert status.message == "Connected successfully"

    def test_service_status_with_latency(self) -> None:
        """ServiceStatus should optionally include latency_ms."""
        from core.connectivity import ServiceStatus

        status = ServiceStatus(healthy=True, message="OK", latency_ms=42.5)
        assert status.latency_ms == 42.5


class TestConnectivityChecker:
    """Tests for ConnectivityChecker service."""

    @pytest.mark.asyncio
    async def test_check_openai_success(self, mock_env) -> None:
        """check_openai should return healthy status when API responds."""
        from core.connectivity import ConnectivityChecker

        checker = ConnectivityChecker()

        with patch("core.connectivity.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_client.models.list.return_value = MagicMock(data=[{"id": "gpt-4"}])
            mock_openai.return_value = mock_client

            status = await checker.check_openai()

            assert status.healthy is True
            assert "connected" in status.message.lower()

    @pytest.mark.asyncio
    async def test_check_openai_failure(self, mock_env) -> None:
        """check_openai should return unhealthy status when API fails."""
        from core.connectivity import ConnectivityChecker

        checker = ConnectivityChecker()

        with patch("core.connectivity.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_client.models.list.side_effect = Exception("Invalid API key")
            mock_openai.return_value = mock_client

            status = await checker.check_openai()

            assert status.healthy is False
            assert "error" in status.message.lower() or "invalid" in status.message.lower()

    @pytest.mark.asyncio
    async def test_check_qdrant_success(self, mock_env) -> None:
        """check_qdrant should return healthy status when connection succeeds."""
        from core.connectivity import ConnectivityChecker

        checker = ConnectivityChecker()

        with patch("core.connectivity.QdrantClient") as mock_qdrant:
            mock_client = MagicMock()
            mock_client.get_collections.return_value = MagicMock(collections=[])
            mock_qdrant.return_value = mock_client

            status = await checker.check_qdrant()

            assert status.healthy is True
            assert "connected" in status.message.lower()

    @pytest.mark.asyncio
    async def test_check_qdrant_failure(self, mock_env) -> None:
        """check_qdrant should return unhealthy status when connection fails."""
        from core.connectivity import ConnectivityChecker

        checker = ConnectivityChecker()

        with patch("core.connectivity.QdrantClient") as mock_qdrant:
            mock_qdrant.side_effect = Exception("Connection refused")

            status = await checker.check_qdrant()

            assert status.healthy is False
            assert "error" in status.message.lower() or "refused" in status.message.lower()

    @pytest.mark.asyncio
    async def test_check_database_success(self, mock_env) -> None:
        """check_database should return healthy status when DB connects."""
        from core.connectivity import ConnectivityChecker

        checker = ConnectivityChecker()

        with patch("core.connectivity.create_async_engine") as mock_engine:
            # Create proper async context manager mock
            mock_conn = AsyncMock()
            mock_conn.execute = AsyncMock(return_value=MagicMock())

            # Mock the async context manager properly
            mock_engine_instance = MagicMock()
            mock_engine_instance.connect = MagicMock(return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_conn),
                __aexit__=AsyncMock(return_value=None),
            ))
            mock_engine_instance.dispose = AsyncMock()
            mock_engine.return_value = mock_engine_instance

            status = await checker.check_database()

            assert status.healthy is True
            assert "connected" in status.message.lower()

    @pytest.mark.asyncio
    async def test_check_database_failure(self, mock_env) -> None:
        """check_database should return unhealthy status when DB fails."""
        from core.connectivity import ConnectivityChecker

        checker = ConnectivityChecker()

        with patch("core.connectivity.create_async_engine") as mock_engine:
            mock_engine.side_effect = Exception("Connection timeout")

            status = await checker.check_database()

            assert status.healthy is False

    @pytest.mark.asyncio
    async def test_check_all_services(self, mock_env) -> None:
        """check_all should return ConnectivityReport with all service statuses."""
        from core.connectivity import ConnectivityChecker, ServiceStatus

        checker = ConnectivityChecker()

        with patch.object(
            checker, "check_openai", return_value=ServiceStatus(healthy=True, message="OK")
        ), patch.object(
            checker, "check_qdrant", return_value=ServiceStatus(healthy=True, message="OK")
        ), patch.object(
            checker, "check_database", return_value=ServiceStatus(healthy=True, message="OK")
        ):
            report = await checker.check_all()

            assert report.openai.healthy is True
            assert report.qdrant.healthy is True
            assert report.database.healthy is True
            assert report.all_healthy is True

    @pytest.mark.asyncio
    async def test_check_all_handles_partial_failure(self, mock_env) -> None:
        """check_all should complete even if some services fail."""
        from core.connectivity import ConnectivityChecker, ServiceStatus

        checker = ConnectivityChecker()

        with patch.object(
            checker, "check_openai", return_value=ServiceStatus(healthy=True, message="OK")
        ), patch.object(
            checker, "check_qdrant", return_value=ServiceStatus(healthy=False, message="Down")
        ), patch.object(
            checker, "check_database", return_value=ServiceStatus(healthy=True, message="OK")
        ):
            report = await checker.check_all()

            assert report.openai.healthy is True
            assert report.qdrant.healthy is False
            assert report.database.healthy is True
            assert report.all_healthy is False


class TestEnvValidation:
    """Tests for .env file validation."""

    def test_detect_placeholder_values(self) -> None:
        """Should detect placeholder values like 'your-api-key-here'."""
        from core.connectivity import is_placeholder_value

        assert is_placeholder_value("your-api-key-here") is True
        assert is_placeholder_value("YOUR_API_KEY") is True
        assert is_placeholder_value("xxx-placeholder-xxx") is True
        assert is_placeholder_value("") is True
        assert is_placeholder_value("sk-proj-abc123xyz") is False
        assert is_placeholder_value("https://xyz.qdrant.io") is False

    def test_validate_env_config(self) -> None:
        """Should validate that all required env vars have real values."""
        from core.connectivity import validate_env_config

        # Valid config
        valid_env = {
            "OPENAI_API_KEY": "sk-proj-abc123",
            "QDRANT_URL": "https://xyz.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key-123",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@host/db",
        }
        result = validate_env_config(valid_env)
        assert result.is_valid is True
        assert len(result.missing) == 0
        assert len(result.placeholders) == 0

        # Missing keys
        missing_env = {
            "OPENAI_API_KEY": "sk-proj-abc123",
        }
        result = validate_env_config(missing_env)
        assert result.is_valid is False
        assert "QDRANT_URL" in result.missing

        # Placeholder values
        placeholder_env = {
            "OPENAI_API_KEY": "your-api-key-here",
            "QDRANT_URL": "https://xyz.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key-123",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@host/db",
        }
        result = validate_env_config(placeholder_env)
        assert result.is_valid is False
        assert "OPENAI_API_KEY" in result.placeholders
