"""Integration tests for error handling and graceful degradation.

TDD: RED phase - tests for T117-T118b error handling tasks.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


class TestGracefulDegradation:
    """Tests for graceful degradation when services are unavailable (T117-T118)."""

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

    @pytest.mark.integration
    def test_returns_503_when_qdrant_unavailable(self, mock_env) -> None:
        """Chat should return 503 INDEX_UNAVAILABLE when Qdrant is down (FR-028)."""
        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            # Mock VectorStoreClient to raise connection error
            with patch("services.rag.VectorStoreClient") as mock_vector:
                mock_instance = MagicMock()
                mock_instance.search = AsyncMock(
                    side_effect=Exception("Connection refused")
                )
                mock_vector.return_value = mock_instance

                with patch("api.routes.chat.RAGPipeline") as mock_rag:
                    mock_rag_instance = MagicMock()
                    mock_rag_instance.query = AsyncMock(
                        side_effect=Exception("Vector store unavailable")
                    )
                    mock_rag.return_value = mock_rag_instance

                    client = TestClient(app, raise_server_exceptions=False)

                    response = client.post(
                        "/chat",
                        json={"message": "What is ROS 2?"}
                    )

                    assert response.status_code == 503
                    data = response.json()
                    assert data["error"] == "INDEX_UNAVAILABLE"

    @pytest.mark.integration
    def test_returns_503_when_openai_unavailable(self, mock_env) -> None:
        """Chat should return 503 when OpenAI is unavailable."""
        with patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"):

            from main import app

            with patch("services.rag.EmbeddingService") as mock_embed:
                mock_instance = MagicMock()
                mock_instance.embed = AsyncMock(
                    side_effect=Exception("OpenAI API error")
                )
                mock_embed.return_value = mock_instance

                with patch("api.routes.chat.RAGPipeline") as mock_rag:
                    mock_rag_instance = MagicMock()
                    mock_rag_instance.query = AsyncMock(
                        side_effect=Exception("Embedding service unavailable")
                    )
                    mock_rag.return_value = mock_rag_instance

                    client = TestClient(app, raise_server_exceptions=False)

                    response = client.post(
                        "/chat",
                        json={"message": "What is ROS 2?"}
                    )

                    assert response.status_code == 503


class TestErrorSanitization:
    """Tests for error response sanitization (T118a-T118b)."""

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

    @pytest.mark.integration
    def test_error_does_not_expose_internal_paths(self, mock_env) -> None:
        """Error responses should not expose internal file paths (FR-029)."""
        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            with patch("api.routes.chat.RAGPipeline") as mock_rag:
                # Simulate error with internal path in message
                mock_rag_instance = MagicMock()
                mock_rag_instance.query = AsyncMock(
                    side_effect=Exception(
                        "Error at /home/user/app/services/rag.py line 42"
                    )
                )
                mock_rag.return_value = mock_rag_instance

                client = TestClient(app, raise_server_exceptions=False)

                response = client.post(
                    "/chat",
                    json={"message": "What is ROS 2?"}
                )

                # Error response should not contain internal paths
                response_text = response.text.lower()
                assert "/home/" not in response_text
                assert "/app/" not in response_text
                assert ".py" not in response_text or "error" in response_text

    @pytest.mark.integration
    def test_error_does_not_expose_credentials(self, mock_env) -> None:
        """Error responses should not expose API keys or credentials (FR-029)."""
        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            with patch("api.routes.chat.RAGPipeline") as mock_rag:
                # Simulate error that might contain credentials
                mock_rag_instance = MagicMock()
                mock_rag_instance.query = AsyncMock(
                    side_effect=Exception(
                        "Authentication failed for api_key=sk-secret123"
                    )
                )
                mock_rag.return_value = mock_rag_instance

                client = TestClient(app, raise_server_exceptions=False)

                response = client.post(
                    "/chat",
                    json={"message": "What is ROS 2?"}
                )

                # Error response should not contain credentials
                response_text = response.text.lower()
                assert "sk-" not in response_text
                assert "api_key" not in response_text
                assert "secret" not in response_text

    @pytest.mark.integration
    def test_error_does_not_expose_stack_trace(self, mock_env) -> None:
        """Error responses should not expose full stack traces (FR-029)."""
        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            with patch("api.routes.chat.RAGPipeline") as mock_rag:
                mock_rag_instance = MagicMock()
                mock_rag_instance.query = AsyncMock(
                    side_effect=ValueError("Invalid configuration")
                )
                mock_rag.return_value = mock_rag_instance

                client = TestClient(app, raise_server_exceptions=False)

                response = client.post(
                    "/chat",
                    json={"message": "What is ROS 2?"}
                )

                # Error response should not contain stack trace indicators
                response_text = response.text.lower()
                assert "traceback" not in response_text
                assert "file \"" not in response_text
