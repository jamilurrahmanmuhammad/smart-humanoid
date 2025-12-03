"""Integration tests for chat API endpoints.

TDD: Tests for T052-T055 - Chat and streaming endpoints.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


class TestChatEndpoint:
    """Integration tests for POST /chat endpoint (T052-T053)."""

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
    def test_chat_returns_200(self, mock_env) -> None:
        """POST /chat should return 200 status."""
        from models.schemas import StreamChunk
        from services.rag import RAGResult

        # Create mock RAG result
        mock_rag_result = RAGResult(
            context="Mocked context",
            citations=[],
            is_out_of_scope=False,
            conflict_warnings=[],
        )

        # Patch at the services.rag module level to affect local imports
        with patch("services.rag.EmbeddingService") as mock_embed, \
             patch("services.rag.VectorStoreClient") as mock_vector, \
             patch("services.rag.CitationExtractor") as mock_cite, \
             patch("services.agent.OpenAI"):

            # Configure embedding service mock
            mock_embed.return_value.embed = AsyncMock(return_value=[0.1] * 1536)

            # Configure vector store mock
            mock_vector.return_value.search = AsyncMock(return_value=[])

            # Configure citation extractor mock
            mock_cite.return_value.extract.return_value = []
            mock_cite.return_value.deduplicate.return_value = []
            mock_cite.return_value.detect_conflicts.return_value = []

            from main import app

            # Patch AgentRunner.run_stream to return empty stream
            with patch("api.routes.chat.AgentRunner") as mock_agent:
                async def empty_stream(*args, **kwargs):
                    yield StreamChunk(type="done", content=None)

                mock_agent.return_value.run_stream = empty_stream

                client = TestClient(app)
                response = client.post(
                    "/chat",
                    json={"message": "What is a ROS 2 node?"},
                )

                assert response.status_code == 200

    @pytest.mark.integration
    def test_chat_returns_chat_response(self, mock_env) -> None:
        """POST /chat should return ChatResponse schema."""
        from models.schemas import StreamChunk
        from services.rag import RAGResult

        # Patch at the services.rag module level to affect local imports
        with patch("services.rag.EmbeddingService") as mock_embed, \
             patch("services.rag.VectorStoreClient") as mock_vector, \
             patch("services.rag.CitationExtractor") as mock_cite, \
             patch("services.agent.OpenAI"):

            # Configure embedding service mock
            mock_embed.return_value.embed = AsyncMock(return_value=[0.1] * 1536)

            # Configure vector store mock
            mock_vector.return_value.search = AsyncMock(return_value=[])

            # Configure citation extractor mock
            mock_cite.return_value.extract.return_value = []
            mock_cite.return_value.deduplicate.return_value = []
            mock_cite.return_value.detect_conflicts.return_value = []

            from main import app

            with patch("api.routes.chat.AgentRunner") as mock_agent:
                async def content_stream(*args, **kwargs):
                    yield StreamChunk(type="content", content="Test response")
                    yield StreamChunk(type="done", content=None)

                mock_agent.return_value.run_stream = content_stream

                client = TestClient(app)
                response = client.post(
                    "/chat",
                    json={"message": "What is a ROS 2 node?"},
                )
                data = response.json()

                # ChatResponse required fields
                assert "session_id" in data
                assert "message_id" in data
                assert "content" in data
                assert "citations" in data
                assert "query_type" in data

    @pytest.mark.integration
    def test_chat_creates_session_if_missing(self, mock_env) -> None:
        """POST /chat should create session if not provided (FR-012)."""
        from models.schemas import StreamChunk
        from services.rag import RAGResult

        # Patch at the services.rag module level to affect local imports
        with patch("services.rag.EmbeddingService") as mock_embed, \
             patch("services.rag.VectorStoreClient") as mock_vector, \
             patch("services.rag.CitationExtractor") as mock_cite, \
             patch("services.agent.OpenAI"):

            # Configure embedding service mock
            mock_embed.return_value.embed = AsyncMock(return_value=[0.1] * 1536)

            # Configure vector store mock
            mock_vector.return_value.search = AsyncMock(return_value=[])

            # Configure citation extractor mock
            mock_cite.return_value.extract.return_value = []
            mock_cite.return_value.deduplicate.return_value = []
            mock_cite.return_value.detect_conflicts.return_value = []

            from main import app

            with patch("api.routes.chat.AgentRunner") as mock_agent:
                async def empty_stream(*args, **kwargs):
                    yield StreamChunk(type="done", content=None)

                mock_agent.return_value.run_stream = empty_stream

                client = TestClient(app)
                response = client.post(
                    "/chat",
                    json={"message": "What is a ROS 2 node?"},
                )
                data = response.json()

                assert data["session_id"] is not None
                assert len(data["session_id"]) > 0

    @pytest.mark.integration
    def test_chat_validates_message_length(self, mock_env) -> None:
        """POST /chat should validate message length."""
        from main import app

        client = TestClient(app)

        # Empty message should fail
        response = client.post(
            "/chat",
            json={"message": ""},
        )

        assert response.status_code == 422  # Validation error


class TestStreamEndpoint:
    """Integration tests for POST /chat/stream endpoint (T054-T055)."""

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
    def test_stream_returns_sse(self, mock_env) -> None:
        """POST /chat/stream should return SSE response (NFR-001)."""
        from models.schemas import StreamChunk
        from services.rag import RAGResult

        # Patch at the services.rag module level to affect local imports
        with patch("services.rag.EmbeddingService") as mock_embed, \
             patch("services.rag.VectorStoreClient") as mock_vector, \
             patch("services.rag.CitationExtractor") as mock_cite, \
             patch("services.agent.OpenAI"):

            # Configure embedding service mock
            mock_embed.return_value.embed = AsyncMock(return_value=[0.1] * 1536)

            # Configure vector store mock
            mock_vector.return_value.search = AsyncMock(return_value=[])

            # Configure citation extractor mock
            mock_cite.return_value.extract.return_value = []
            mock_cite.return_value.deduplicate.return_value = []
            mock_cite.return_value.detect_conflicts.return_value = []

            from main import app

            with patch("api.routes.chat.AgentRunner") as mock_agent:
                async def stream_response(*args, **kwargs):
                    yield StreamChunk(type="content", content="Hello")
                    yield StreamChunk(type="done", content=None)

                mock_agent.return_value.run_stream = stream_response

                client = TestClient(app)
                response = client.post(
                    "/chat/stream",
                    json={"message": "What is a ROS 2 node?"},
                )

                assert response.status_code == 200
                assert "text/event-stream" in response.headers.get("content-type", "")

    @pytest.mark.integration
    def test_stream_accepts_chat_request(self, mock_env) -> None:
        """POST /chat/stream should accept ChatRequest schema."""
        from models.schemas import StreamChunk
        from services.rag import RAGResult

        # Patch at the services.rag module level to affect local imports
        with patch("services.rag.EmbeddingService") as mock_embed, \
             patch("services.rag.VectorStoreClient") as mock_vector, \
             patch("services.rag.CitationExtractor") as mock_cite, \
             patch("services.agent.OpenAI"):

            # Configure embedding service mock
            mock_embed.return_value.embed = AsyncMock(return_value=[0.1] * 1536)

            # Configure vector store mock
            mock_vector.return_value.search = AsyncMock(return_value=[])

            # Configure citation extractor mock
            mock_cite.return_value.extract.return_value = []
            mock_cite.return_value.deduplicate.return_value = []
            mock_cite.return_value.detect_conflicts.return_value = []

            from main import app

            with patch("api.routes.chat.AgentRunner") as mock_agent:
                async def empty_stream(*args, **kwargs):
                    yield StreamChunk(type="done", content=None)

                mock_agent.return_value.run_stream = empty_stream

                client = TestClient(app)
                response = client.post(
                    "/chat/stream",
                    json={
                        "message": "What is a ROS 2 node?",
                        "persona": "Explorer",
                        "query_type": "page",
                        "current_chapter": 2,
                    },
                )

                assert response.status_code == 200
