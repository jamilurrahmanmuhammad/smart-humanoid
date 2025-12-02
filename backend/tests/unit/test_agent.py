"""Unit tests for OpenAI Agent integration.

TDD: RED phase - these tests should FAIL until T047-T049 are implemented.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestAgentToolDefinition:
    """Tests for Agent tool definition (T046-T047)."""

    @pytest.mark.unit
    def test_search_book_content_tool_defined(self) -> None:
        """search_book_content tool should be defined with correct schema."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.agent import get_agent_tools

            tools = get_agent_tools()

            # Should have search_book_content tool
            tool_names = [t.name for t in tools]
            assert "search_book_content" in tool_names

    @pytest.mark.unit
    def test_search_book_content_tool_schema(self) -> None:
        """search_book_content tool should have correct parameter schema."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.agent import get_agent_tools

            tools = get_agent_tools()
            search_tool = next(t for t in tools if t.name == "search_book_content")

            # Should have query parameter at minimum
            assert search_tool.parameters is not None
            assert "query" in search_tool.parameters.get("properties", {})

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_search_book_content_executes_rag(self) -> None:
        """search_book_content should use RAGPipeline for search."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.agent import search_book_content

            # Mock RAGPipeline
            with patch("services.agent.RAGPipeline") as mock_pipeline_class:
                mock_pipeline = MagicMock()
                mock_result = MagicMock()
                mock_result.context = "Retrieved context about nodes"
                mock_result.citations = []
                mock_result.is_out_of_scope = False
                mock_pipeline.query = AsyncMock(return_value=mock_result)
                mock_pipeline_class.return_value = mock_pipeline

                result = await search_book_content("What is a ROS 2 node?")

                assert "Retrieved context" in result or "nodes" in result


class TestAgentRunner:
    """Tests for AgentRunner with streaming (T048-T049)."""

    @pytest.mark.unit
    def test_agent_runner_initialization(self) -> None:
        """AgentRunner should initialize with settings."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.agent import AgentRunner

            runner = AgentRunner()

            assert runner is not None
            assert runner.model is not None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_run_stream_yields_chunks(self) -> None:
        """run_stream should yield StreamChunk objects (NFR-001)."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from models.schemas import StreamChunk
            from services.agent import AgentRunner

            runner = AgentRunner()

            # Mock OpenAI streaming response
            mock_chunk = MagicMock()
            mock_chunk.choices = [MagicMock()]
            mock_chunk.choices[0].delta = MagicMock()
            mock_chunk.choices[0].delta.content = "Test response"
            mock_chunk.choices[0].finish_reason = None

            mock_done_chunk = MagicMock()
            mock_done_chunk.choices = [MagicMock()]
            mock_done_chunk.choices[0].delta = MagicMock()
            mock_done_chunk.choices[0].delta.content = None
            mock_done_chunk.choices[0].finish_reason = "stop"

            async def mock_stream():
                yield mock_chunk
                yield mock_done_chunk

            with patch.object(
                runner, "_create_stream", return_value=mock_stream()
            ):
                chunks = []
                async for chunk in runner.run_stream("What is ROS 2?"):
                    chunks.append(chunk)

                assert len(chunks) >= 1
                assert all(isinstance(c, StreamChunk) for c in chunks)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_run_stream_includes_done_chunk(self) -> None:
        """run_stream should yield done chunk at end."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.agent import AgentRunner

            runner = AgentRunner()

            mock_done_chunk = MagicMock()
            mock_done_chunk.choices = [MagicMock()]
            mock_done_chunk.choices[0].delta = MagicMock()
            mock_done_chunk.choices[0].delta.content = None
            mock_done_chunk.choices[0].finish_reason = "stop"

            async def mock_stream():
                yield mock_done_chunk

            with patch.object(
                runner, "_create_stream", return_value=mock_stream()
            ):
                chunks = []
                async for chunk in runner.run_stream("Test"):
                    chunks.append(chunk)

                # Last chunk should be done type
                assert chunks[-1].type == "done"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_run_stream_with_context(self) -> None:
        """run_stream should accept context for conversation history."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.agent import AgentRunner

            runner = AgentRunner()

            context = [
                {"role": "user", "content": "Previous question"},
                {"role": "assistant", "content": "Previous answer"},
            ]

            mock_done_chunk = MagicMock()
            mock_done_chunk.choices = [MagicMock()]
            mock_done_chunk.choices[0].delta = MagicMock()
            mock_done_chunk.choices[0].delta.content = None
            mock_done_chunk.choices[0].finish_reason = "stop"

            async def mock_stream():
                yield mock_done_chunk

            with patch.object(
                runner, "_create_stream", return_value=mock_stream()
            ):
                chunks = []
                async for chunk in runner.run_stream("Follow-up", context=context):
                    chunks.append(chunk)

                # Should complete without error
                assert len(chunks) >= 1


class TestAgentError:
    """Tests for agent error handling."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_run_stream_handles_api_error(self) -> None:
        """run_stream should handle OpenAI API errors gracefully."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.agent import AgentError, AgentRunner

            runner = AgentRunner()

            async def mock_error_stream():
                raise Exception("API Error")
                yield  # Make it a generator

            with patch.object(
                runner, "_create_stream", return_value=mock_error_stream()
            ):
                with pytest.raises(AgentError):
                    async for _ in runner.run_stream("Test"):
                        pass
