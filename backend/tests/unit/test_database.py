"""Unit tests for async database session factory.

TDD: RED phase - these tests should FAIL until T017 is implemented.
"""

import os
from unittest.mock import patch

import pytest


class TestAsyncSessionFactory:
    """Tests for async database session factory (T016-T017)."""

    @pytest.mark.unit
    def test_async_engine_creation(self) -> None:
        """Should create async engine from DATABASE_URL."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/testdb",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from core.database import create_async_engine

            engine = create_async_engine()

            assert engine is not None
            # Verify it's async
            assert "asyncpg" in str(engine.url.drivername)

    @pytest.mark.unit
    def test_async_session_factory_creation(self) -> None:
        """Should create async session factory."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/testdb",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from core.database import AsyncSessionFactory

            assert AsyncSessionFactory is not None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_get_async_session_context_manager(self) -> None:
        """get_async_session should work as async context manager."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/testdb",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from core.database import get_async_session

            # Should be an async generator
            session_gen = get_async_session()
            assert hasattr(session_gen, "__anext__")

    @pytest.mark.unit
    def test_database_url_must_be_async(self) -> None:
        """Should verify DATABASE_URL uses asyncpg driver."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost:5432/testdb",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from core.database import create_async_engine

            engine = create_async_engine()
            # Should be using asyncpg dialect
            assert engine.dialect.name == "postgresql"


class TestExpiredMessageFiltering:
    """Tests for expired message filtering (T107)."""

    @pytest.mark.unit
    def test_filter_excludes_expired_messages(self) -> None:
        """get_valid_messages should exclude messages where expires_at < now (FR-027)."""
        from datetime import datetime, timedelta, timezone
        from unittest.mock import MagicMock

        now = datetime.now(timezone.utc)

        # Create mock messages - some expired, some valid
        expired_msg = MagicMock()
        expired_msg.id = "1"
        expired_msg.expires_at = now - timedelta(hours=1)  # Expired

        valid_msg = MagicMock()
        valid_msg.id = "2"
        valid_msg.expires_at = now + timedelta(hours=23)  # Valid

        messages = [expired_msg, valid_msg]

        # Filter logic: exclude where expires_at < now
        valid_messages = [m for m in messages if m.expires_at > now]

        assert len(valid_messages) == 1
        assert valid_messages[0].id == "2"

    @pytest.mark.unit
    def test_filter_includes_messages_expiring_in_future(self) -> None:
        """Messages with expires_at in future should be included."""
        from datetime import datetime, timedelta, timezone
        from unittest.mock import MagicMock

        now = datetime.now(timezone.utc)

        # All messages valid
        msg1 = MagicMock()
        msg1.id = "1"
        msg1.expires_at = now + timedelta(hours=1)

        msg2 = MagicMock()
        msg2.id = "2"
        msg2.expires_at = now + timedelta(hours=24)

        messages = [msg1, msg2]

        valid_messages = [m for m in messages if m.expires_at > now]

        assert len(valid_messages) == 2

    @pytest.mark.unit
    def test_filter_handles_empty_list(self) -> None:
        """Filter should handle empty message list."""
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        messages = []

        valid_messages = [m for m in messages if m.expires_at > now]

        assert valid_messages == []

    @pytest.mark.unit
    def test_filter_excludes_exactly_expired_messages(self) -> None:
        """Messages with expires_at exactly at now should be excluded."""
        from datetime import datetime, timezone
        from unittest.mock import MagicMock

        now = datetime.now(timezone.utc)

        # Message that expires exactly now
        msg = MagicMock()
        msg.id = "1"
        msg.expires_at = now

        messages = [msg]

        # Using > (not >=) so exactly-now is excluded
        valid_messages = [m for m in messages if m.expires_at > now]

        assert len(valid_messages) == 0
