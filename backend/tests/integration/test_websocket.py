"""Integration tests for WebSocket chat endpoint.

TDD: Tests for T056-T059 - WebSocket connection lifecycle and error handling.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch
from dataclasses import dataclass

import pytest
from fastapi.testclient import TestClient


@dataclass
class MockRAGResult:
    """Mock RAG result for testing."""
    context: str
    citations: list
    is_out_of_scope: bool
    conflict_warnings: list


class TestWebSocketConnection:
    """Integration tests for WebSocket /ws/chat endpoint (T056-T057)."""

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
    def test_websocket_connect_and_welcome(self, mock_env) -> None:
        """WebSocket should accept connection and send welcome message."""
        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            client = TestClient(app)

            with client.websocket_connect("/chat/ws/test-session-123") as websocket:
                # Should receive welcome message
                data = websocket.receive_json()

                assert data["type"] == "welcome"
                assert data["session_id"] == "test-session-123"

    @pytest.mark.integration
    def test_websocket_send_message_receive_stream(self, mock_env) -> None:
        """WebSocket should process messages and stream responses."""
        from models.schemas import StreamChunk

        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            # Mock the RAGPipeline at the route level
            with patch("api.routes.chat.RAGPipeline") as mock_rag_class:
                mock_rag_result = MockRAGResult(
                    context="Test context",
                    citations=[],
                    is_out_of_scope=False,
                    conflict_warnings=[],
                )
                mock_rag_instance = MagicMock()
                mock_rag_instance.query = AsyncMock(return_value=mock_rag_result)
                mock_rag_class.return_value = mock_rag_instance

                with patch("api.routes.chat.AgentRunner") as mock_agent:
                    async def content_stream(*args, **kwargs):
                        yield StreamChunk(type="content", content="Hello ")
                        yield StreamChunk(type="content", content="World")
                        yield StreamChunk(type="done", content=None)

                    mock_agent.return_value.run_stream = content_stream

                    client = TestClient(app)

                    with client.websocket_connect("/chat/ws/test-session") as websocket:
                        # Receive welcome
                        welcome = websocket.receive_json()
                        assert welcome["type"] == "welcome"

                        # Send message
                        websocket.send_json({
                            "message": "What is ROS 2?",
                        })

                        # Receive message_start
                        msg_start = websocket.receive_json()
                        assert msg_start["type"] == "message_start"
                        assert "message_id" in msg_start

                        # Receive content chunks
                        content1 = websocket.receive_json()
                        assert content1["type"] == "content"
                        assert content1["content"] == "Hello "

                        content2 = websocket.receive_json()
                        assert content2["type"] == "content"
                        assert content2["content"] == "World"

                        # Receive done
                        done = websocket.receive_json()
                        assert done["type"] == "done"

    @pytest.mark.integration
    def test_websocket_with_citations(self, mock_env) -> None:
        """WebSocket should send citations before content."""
        from models.schemas import Citation, StreamChunk

        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            # Mock the RAGPipeline with citations
            with patch("api.routes.chat.RAGPipeline") as mock_rag_class:
                mock_citation = Citation(
                    chapter=2,
                    section="2.1",
                    heading="ROS 2 Overview",
                    quote="ROS 2 is a robotics middleware...",
                    link="/chapter-2#overview",
                    relevance_score=0.95,
                )
                mock_rag_result = MockRAGResult(
                    context="Test context",
                    citations=[mock_citation],
                    is_out_of_scope=False,
                    conflict_warnings=[],
                )
                mock_rag_instance = MagicMock()
                mock_rag_instance.query = AsyncMock(return_value=mock_rag_result)
                mock_rag_class.return_value = mock_rag_instance

                with patch("api.routes.chat.AgentRunner") as mock_agent:
                    async def content_stream(*args, **kwargs):
                        yield StreamChunk(type="content", content="Response")
                        yield StreamChunk(type="done", content=None)

                    mock_agent.return_value.run_stream = content_stream

                    client = TestClient(app)

                    with client.websocket_connect("/chat/ws/test-session") as websocket:
                        # Receive welcome
                        websocket.receive_json()

                        # Send message
                        websocket.send_json({"message": "What is ROS 2?"})

                        # Receive message_start
                        websocket.receive_json()

                        # Receive citation
                        citation_msg = websocket.receive_json()
                        assert citation_msg["type"] == "citation"
                        assert citation_msg["citation"]["chapter"] == 2
                        assert citation_msg["citation"]["heading"] == "ROS 2 Overview"

                        # Receive content
                        content = websocket.receive_json()
                        assert content["type"] == "content"

                        # Receive done
                        done = websocket.receive_json()
                        assert done["type"] == "done"

    @pytest.mark.integration
    def test_websocket_disconnect_graceful(self, mock_env) -> None:
        """WebSocket should handle client disconnect gracefully."""
        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            client = TestClient(app)

            # Connect and immediately close - should not raise
            with client.websocket_connect("/chat/ws/test-session") as websocket:
                websocket.receive_json()  # Get welcome
                # Connection closes at end of context - should be graceful


class TestWebSocketErrorHandling:
    """Integration tests for WebSocket error handling (T058-T059)."""

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
    def test_websocket_invalid_message_format(self, mock_env) -> None:
        """WebSocket should handle invalid message format gracefully."""
        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            client = TestClient(app)

            with client.websocket_connect("/chat/ws/test-session") as websocket:
                # Receive welcome
                websocket.receive_json()

                # Send invalid message (empty message should fail validation)
                websocket.send_json({
                    "message": "",  # Empty message violates min_length
                })

                # Should receive error response
                error = websocket.receive_json()
                assert error["type"] == "error"
                assert "Invalid request" in error["error"]

    @pytest.mark.integration
    def test_websocket_out_of_scope_query(self, mock_env) -> None:
        """WebSocket should handle out-of-scope queries gracefully."""
        from models.schemas import StreamChunk

        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            # Mock RAGPipeline to return out-of-scope
            with patch("api.routes.chat.RAGPipeline") as mock_rag_class:
                mock_rag_result = MockRAGResult(
                    context="",
                    citations=[],
                    is_out_of_scope=True,
                    conflict_warnings=[],
                )
                mock_rag_instance = MagicMock()
                mock_rag_instance.query = AsyncMock(return_value=mock_rag_result)
                mock_rag_class.return_value = mock_rag_instance

                client = TestClient(app)

                with client.websocket_connect("/chat/ws/test-session") as websocket:
                    # Receive welcome
                    websocket.receive_json()

                    # Send out-of-scope query
                    websocket.send_json({
                        "message": "What is the weather today?",
                    })

                    # Receive message_start
                    websocket.receive_json()

                    # Should receive out-of-scope content
                    content = websocket.receive_json()
                    assert content["type"] == "content"
                    assert "don't have information" in content["content"].lower()

                    # Receive done
                    done = websocket.receive_json()
                    assert done["type"] == "done"

    @pytest.mark.integration
    def test_websocket_multiple_messages(self, mock_env) -> None:
        """WebSocket should handle multiple messages in sequence."""
        from models.schemas import StreamChunk

        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            with patch("api.routes.chat.RAGPipeline") as mock_rag_class:
                mock_rag_result = MockRAGResult(
                    context="Test context",
                    citations=[],
                    is_out_of_scope=False,
                    conflict_warnings=[],
                )
                mock_rag_instance = MagicMock()
                mock_rag_instance.query = AsyncMock(return_value=mock_rag_result)
                mock_rag_class.return_value = mock_rag_instance

                with patch("api.routes.chat.AgentRunner") as mock_agent:
                    call_count = [0]

                    async def content_stream(*args, **kwargs):
                        call_count[0] += 1
                        yield StreamChunk(type="content", content=f"Response {call_count[0]}")
                        yield StreamChunk(type="done", content=None)

                    mock_agent.return_value.run_stream = content_stream

                    client = TestClient(app)

                    with client.websocket_connect("/chat/ws/test-session") as websocket:
                        # Receive welcome
                        websocket.receive_json()

                        # First message
                        websocket.send_json({"message": "First question"})
                        websocket.receive_json()  # message_start
                        content1 = websocket.receive_json()
                        websocket.receive_json()  # done

                        # Second message
                        websocket.send_json({"message": "Second question"})
                        websocket.receive_json()  # message_start
                        content2 = websocket.receive_json()
                        websocket.receive_json()  # done

                        # Verify both messages were processed
                        assert "Response" in content1.get("content", "")
                        assert "Response" in content2.get("content", "")

    @pytest.mark.integration
    def test_websocket_with_query_type(self, mock_env) -> None:
        """WebSocket should accept query_type parameter."""
        from models.schemas import StreamChunk

        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            with patch("api.routes.chat.RAGPipeline") as mock_rag_class:
                mock_rag_result = MockRAGResult(
                    context="Test context",
                    citations=[],
                    is_out_of_scope=False,
                    conflict_warnings=[],
                )
                mock_rag_instance = MagicMock()
                mock_rag_instance.query = AsyncMock(return_value=mock_rag_result)
                mock_rag_class.return_value = mock_rag_instance

                with patch("api.routes.chat.AgentRunner") as mock_agent:
                    async def content_stream(*args, **kwargs):
                        yield StreamChunk(type="content", content="Response")
                        yield StreamChunk(type="done", content=None)

                    mock_agent.return_value.run_stream = content_stream

                    client = TestClient(app)

                    with client.websocket_connect("/chat/ws/test-session") as websocket:
                        # Receive welcome
                        websocket.receive_json()

                        # Send message with query_type
                        websocket.send_json({
                            "message": "What is on this page?",
                            "query_type": "page",
                            "current_chapter": 3,
                        })

                        # Should process successfully
                        msg_start = websocket.receive_json()
                        assert msg_start["type"] == "message_start"

                        content = websocket.receive_json()
                        assert content["type"] == "content"

                        done = websocket.receive_json()
                        assert done["type"] == "done"

    @pytest.mark.integration
    def test_websocket_with_persona(self, mock_env) -> None:
        """WebSocket should accept persona parameter."""
        from models.schemas import StreamChunk

        with patch("services.rag.EmbeddingService"), \
             patch("services.rag.VectorStoreClient"), \
             patch("services.rag.CitationExtractor"), \
             patch("services.agent.OpenAI"):

            from main import app

            with patch("api.routes.chat.RAGPipeline") as mock_rag_class:
                mock_rag_result = MockRAGResult(
                    context="Test context",
                    citations=[],
                    is_out_of_scope=False,
                    conflict_warnings=[],
                )
                mock_rag_instance = MagicMock()
                mock_rag_instance.query = AsyncMock(return_value=mock_rag_result)
                mock_rag_class.return_value = mock_rag_instance

                with patch("api.routes.chat.AgentRunner") as mock_agent:
                    async def content_stream(*args, **kwargs):
                        yield StreamChunk(type="content", content="Response")
                        yield StreamChunk(type="done", content=None)

                    mock_agent.return_value.run_stream = content_stream

                    client = TestClient(app)

                    with client.websocket_connect("/chat/ws/test-session") as websocket:
                        # Receive welcome
                        websocket.receive_json()

                        # Send message with persona
                        websocket.send_json({
                            "message": "Explain torque",
                            "persona": "Explorer",
                        })

                        # Should process successfully
                        msg_start = websocket.receive_json()
                        assert msg_start["type"] == "message_start"

                        content = websocket.receive_json()
                        assert content["type"] == "content"

                        done = websocket.receive_json()
                        assert done["type"] == "done"
