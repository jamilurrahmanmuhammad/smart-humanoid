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
