"""Unit tests for message purge service.

TDD: RED phase - tests for T115-T116 message purge tasks.
"""

import os
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestMessagePurge:
    """Tests for expired message purge (T115-T116)."""

    @pytest.fixture
    def mock_env(self):
        """Set up environment variables for tests."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            yield

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_purge_deletes_expired_messages(self, mock_env) -> None:
        """purge_expired_messages should delete messages where expires_at < now (FR-027)."""
        from services.purge import PurgeService

        service = PurgeService()

        # Mock database session
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 5  # 5 messages deleted
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.commit = AsyncMock()

        deleted_count = await service.purge_expired_messages(mock_session)

        assert deleted_count == 5
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_purge_returns_zero_when_no_expired(self, mock_env) -> None:
        """purge_expired_messages should return 0 when no messages expired."""
        from services.purge import PurgeService

        service = PurgeService()

        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 0
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.commit = AsyncMock()

        deleted_count = await service.purge_expired_messages(mock_session)

        assert deleted_count == 0

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_purge_deletes_expired_analytics(self, mock_env) -> None:
        """purge_expired_analytics should delete analytics where expires_at < now (FR-027)."""
        from services.purge import PurgeService

        service = PurgeService()

        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 10
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.commit = AsyncMock()

        deleted_count = await service.purge_expired_analytics(mock_session)

        assert deleted_count == 10

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_run_all_purges(self, mock_env) -> None:
        """run_all should purge both messages and analytics."""
        from services.purge import PurgeService

        service = PurgeService()

        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 3
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.commit = AsyncMock()

        result = await service.run_all(mock_session)

        assert result["messages_deleted"] >= 0
        assert result["analytics_deleted"] >= 0

    @pytest.mark.unit
    def test_purge_service_has_ttl_constant(self, mock_env) -> None:
        """PurgeService should define TTL constant matching FR-027 (24 hours)."""
        from services.purge import PurgeService

        service = PurgeService()

        # TTL should be 24 hours
        assert hasattr(service, "MESSAGE_TTL_HOURS")
        assert service.MESSAGE_TTL_HOURS == 24
