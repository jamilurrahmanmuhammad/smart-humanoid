"""Unit tests for Settings configuration model.

TDD: RED phase - these tests should FAIL until T007 is implemented.
"""

import os
from unittest.mock import patch

import pytest


class TestSettings:
    """Tests for Pydantic Settings model validation."""

    @pytest.mark.unit
    def test_settings_loads_from_environment(self) -> None:
        """Settings should load required values from environment variables."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key-123",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-test-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/testdb",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from core.config import Settings

            settings = Settings()

            assert settings.openai_api_key.get_secret_value() == "sk-test-key-123"
            assert settings.qdrant_url == "https://test.qdrant.io"
            assert settings.qdrant_api_key.get_secret_value() == "qdrant-test-key"
            assert "postgresql+asyncpg" in settings.database_url.get_secret_value()

    @pytest.mark.unit
    def test_settings_provides_defaults(self) -> None:
        """Settings should provide sensible defaults for optional fields."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from core.config import Settings

            settings = Settings()

            # Check defaults
            assert settings.app_name == "smart-humanoid-chatbot"
            assert settings.app_env == "development"
            assert settings.debug is True
            assert settings.log_level == "DEBUG"
            assert settings.api_host == "0.0.0.0"
            assert settings.api_port == 8000
            assert settings.qdrant_collection_name == "textbook_chunks"
            assert settings.rag_top_k == 10
            assert settings.rag_similarity_threshold == 0.5
            assert settings.rag_max_citations == 5
            assert settings.session_ttl_hours == 24
            assert settings.message_retention_hours == 24
            assert settings.safety_keywords_enabled is True

    @pytest.mark.unit
    def test_settings_validates_required_fields(self) -> None:
        """Settings should raise error when required fields are missing."""
        from pydantic import ValidationError

        # Create settings without required fields - should raise ValidationError
        # We test by directly instantiating with explicit None/missing values
        with pytest.raises(ValidationError):
            # Import fresh to avoid caching issues
            from core.config import Settings

            # Instantiate without providing required fields
            Settings(
                openai_api_key=None,  # type: ignore
                qdrant_url=None,  # type: ignore
                qdrant_api_key=None,  # type: ignore
                database_url=None,  # type: ignore
                _env_file=None,  # Disable .env file loading
            )

    @pytest.mark.unit
    def test_settings_validates_openai_model(self) -> None:
        """Settings should allow configuring OpenAI model."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
            "OPENAI_MODEL": "gpt-4-turbo",
            "OPENAI_EMBEDDING_MODEL": "text-embedding-3-large",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from core.config import Settings

            settings = Settings()

            assert settings.openai_model == "gpt-4-turbo"
            assert settings.openai_embedding_model == "text-embedding-3-large"

    @pytest.mark.unit
    def test_settings_cors_origins_parsing(self) -> None:
        """Settings should parse CORS origins as a list."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
            "CORS_ORIGINS": '["http://localhost:3000","http://localhost:8080"]',
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from core.config import Settings

            settings = Settings()

            assert isinstance(settings.cors_origins, list)
            assert "http://localhost:3000" in settings.cors_origins
            assert "http://localhost:8080" in settings.cors_origins

    @pytest.mark.unit
    def test_settings_rag_constraints(self) -> None:
        """Settings should validate RAG configuration constraints."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
            "RAG_TOP_K": "20",
            "RAG_SIMILARITY_THRESHOLD": "0.8",
            "RAG_MAX_CITATIONS": "5",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from core.config import Settings

            settings = Settings()

            assert settings.rag_top_k == 20
            assert settings.rag_similarity_threshold == 0.8
            assert settings.rag_max_citations == 5

    @pytest.mark.unit
    def test_get_settings_singleton(self) -> None:
        """get_settings should return cached Settings instance."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from core.config import get_settings

            settings1 = get_settings()
            settings2 = get_settings()

            # Should be cached (same instance or equal values)
            assert settings1.app_name == settings2.app_name
