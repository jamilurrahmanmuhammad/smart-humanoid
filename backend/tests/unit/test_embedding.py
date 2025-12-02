"""Unit tests for embedding service.

TDD: RED phase - these tests should FAIL until T037 is implemented.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestEmbeddingService:
    """Tests for EmbeddingService (T036-T037)."""

    @pytest.mark.unit
    def test_embedding_service_initialization(self) -> None:
        """EmbeddingService should initialize with settings."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
            "OPENAI_EMBEDDING_MODEL": "text-embedding-3-small",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.embedding import EmbeddingService

            service = EmbeddingService()

            assert service is not None
            assert service.model == "text-embedding-3-small"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_embed_returns_vector(self) -> None:
        """embed should return 1536-dimensional vector."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.embedding import EmbeddingService

            service = EmbeddingService()

            # Mock OpenAI response
            mock_embedding = [0.1] * 1536
            mock_response = MagicMock()
            mock_response.data = [MagicMock(embedding=mock_embedding)]

            with patch.object(
                service._client.embeddings, "create", return_value=mock_response
            ):
                result = await service.embed("What is ROS 2?")

            assert len(result) == 1536
            assert isinstance(result, list)
            assert all(isinstance(x, float) for x in result)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_embed_handles_empty_input(self) -> None:
        """embed should handle empty input gracefully."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.embedding import EmbeddingService

            service = EmbeddingService()

            # Empty input should raise or return zeros
            with pytest.raises(ValueError):
                await service.embed("")

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_embed_uses_correct_model(self) -> None:
        """embed should use configured embedding model."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.embedding import EmbeddingService

            service = EmbeddingService()

            mock_embedding = [0.1] * 1536
            mock_response = MagicMock()
            mock_response.data = [MagicMock(embedding=mock_embedding)]

            with patch.object(
                service._client.embeddings, "create", return_value=mock_response
            ) as mock_create:
                await service.embed("Test text")

                # Verify model parameter was passed (default is text-embedding-3-small)
                mock_create.assert_called_once()
                call_kwargs = mock_create.call_args[1]
                assert "model" in call_kwargs
                assert call_kwargs["model"] == service.model

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_embed_batch(self) -> None:
        """embed_batch should handle multiple texts."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.embedding import EmbeddingService

            service = EmbeddingService()

            # Mock batch response
            mock_embeddings = [[0.1] * 1536 for _ in range(3)]
            mock_response = MagicMock()
            mock_response.data = [
                MagicMock(embedding=emb) for emb in mock_embeddings
            ]

            with patch.object(
                service._client.embeddings, "create", return_value=mock_response
            ):
                texts = ["Text 1", "Text 2", "Text 3"]
                results = await service.embed_batch(texts)

            assert len(results) == 3
            assert all(len(emb) == 1536 for emb in results)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_embed_handles_api_error(self) -> None:
        """embed should handle OpenAI API errors gracefully."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.embedding import EmbeddingService, EmbeddingError

            service = EmbeddingService()

            with patch.object(
                service._client.embeddings,
                "create",
                side_effect=Exception("API Error"),
            ):
                with pytest.raises(EmbeddingError):
                    await service.embed("Test text")
