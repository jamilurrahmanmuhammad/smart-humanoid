"""Unit tests for RAG pipeline service.

TDD: RED phase - these tests should FAIL until T043-T045f are implemented.
"""

import os
from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestRAGPipelineQuery:
    """Tests for RAG pipeline query flow (T042-T043)."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_pipeline_query_returns_rag_result(self) -> None:
        """query should return RAGResult with response and citations (FR-001, FR-004)."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline, RAGResult

            # Create pipeline with mocked dependencies
            pipeline = RAGPipeline()

            # Mock embedding service
            mock_embedding = [0.1] * 1536
            pipeline._embedding_service = MagicMock()
            pipeline._embedding_service.embed = AsyncMock(return_value=mock_embedding)

            # Mock vector store search
            mock_chunk = MagicMock()
            mock_chunk.id = "chunk-1"
            mock_chunk.module_id = 1
            mock_chunk.chapter_id = 2
            mock_chunk.section_id = "2.3.1"
            mock_chunk.heading = "ROS 2 Nodes"
            mock_chunk.text = "A node is a process that performs computation..."
            mock_chunk.persona = "Default"
            mock_chunk.path = "/module-1/chapter-2#nodes"
            mock_chunk.chunk_index = 0
            mock_chunk.relevance_score = 0.95

            pipeline._vector_store = MagicMock()
            pipeline._vector_store.search = AsyncMock(return_value=[mock_chunk])

            result = await pipeline.query("What is a ROS 2 node?")

            assert isinstance(result, RAGResult)
            assert result.context is not None
            assert len(result.citations) > 0
            assert result.is_out_of_scope is False

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_pipeline_query_with_filters(self) -> None:
        """query should pass filters to vector store search."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline
            from services.vector_store import SearchFilters

            pipeline = RAGPipeline()

            # Mock embedding service
            pipeline._embedding_service = MagicMock()
            pipeline._embedding_service.embed = AsyncMock(return_value=[0.1] * 1536)

            # Mock vector store
            pipeline._vector_store = MagicMock()
            pipeline._vector_store.search = AsyncMock(return_value=[])

            filters = SearchFilters(chapter_id=3, persona="Explorer")
            await pipeline.query("What is URDF?", filters=filters)

            # Verify filters were passed
            pipeline._vector_store.search.assert_called_once()
            call_kwargs = pipeline._vector_store.search.call_args[1]
            assert call_kwargs.get("filters") == filters


class TestContextBuilder:
    """Tests for context window building (T044-T045)."""

    @pytest.mark.unit
    def test_build_context_from_chunks(self) -> None:
        """build_context should construct context from chunks within token limit."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline
            from services.vector_store import ContentChunk

            pipeline = RAGPipeline()

            chunks = [
                ContentChunk(
                    id="chunk-1",
                    module_id=1,
                    chapter_id=2,
                    section_id="2.1",
                    heading="Introduction",
                    text="This is the first chunk of content.",
                    persona="Default",
                    path="/test1",
                    chunk_index=0,
                    relevance_score=0.95,
                ),
                ContentChunk(
                    id="chunk-2",
                    module_id=1,
                    chapter_id=2,
                    section_id="2.2",
                    heading="Details",
                    text="This is the second chunk of content.",
                    persona="Default",
                    path="/test2",
                    chunk_index=0,
                    relevance_score=0.88,
                ),
            ]

            context = pipeline.build_context(chunks, max_tokens=1000)

            assert context is not None
            assert "first chunk" in context
            assert "second chunk" in context

    @pytest.mark.unit
    def test_build_context_respects_token_limit(self) -> None:
        """build_context should truncate when exceeding token limit."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline
            from services.vector_store import ContentChunk

            pipeline = RAGPipeline()

            # Create chunks that exceed token limit
            long_text = "This is a very long piece of text. " * 100
            chunks = [
                ContentChunk(
                    id=f"chunk-{i}",
                    module_id=1,
                    chapter_id=1,
                    section_id=f"1.{i}",
                    heading=f"Section {i}",
                    text=long_text,
                    persona="Default",
                    path=f"/test{i}",
                    chunk_index=0,
                    relevance_score=0.9 - (i * 0.1),
                )
                for i in range(10)
            ]

            context = pipeline.build_context(chunks, max_tokens=500)

            # Context should be limited
            # Rough estimate: 1 token ~= 4 chars
            assert len(context) < 500 * 4 * 2  # Allow some margin

    @pytest.mark.unit
    def test_build_context_empty_chunks(self) -> None:
        """build_context should handle empty chunks list."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline

            pipeline = RAGPipeline()

            context = pipeline.build_context([], max_tokens=1000)

            assert context == ""


class TestOutOfScopeDetection:
    """Tests for out-of-scope query detection (T045a-T045b)."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_detect_out_of_scope_with_no_results(self) -> None:
        """detect_out_of_scope should return True when no relevant results (FR-006, FR-007)."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline

            pipeline = RAGPipeline()

            # Query with no search results
            is_out_of_scope = pipeline.detect_out_of_scope(
                query="What is the capital of France?",
                search_results=[],
            )

            assert is_out_of_scope is True

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_detect_out_of_scope_with_low_relevance(self) -> None:
        """detect_out_of_scope should return True when results have low relevance."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline
            from services.vector_store import ContentChunk

            pipeline = RAGPipeline()

            # Results with very low relevance scores
            low_relevance_chunks = [
                ContentChunk(
                    id="chunk-1",
                    module_id=1,
                    chapter_id=1,
                    section_id="1.1",
                    heading="Test",
                    text="Some unrelated content",
                    persona="Default",
                    path="/test",
                    chunk_index=0,
                    relevance_score=0.3,  # Below threshold
                ),
            ]

            is_out_of_scope = pipeline.detect_out_of_scope(
                query="What is quantum physics?",
                search_results=low_relevance_chunks,
            )

            assert is_out_of_scope is True

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_detect_out_of_scope_with_relevant_results(self) -> None:
        """detect_out_of_scope should return False when results are relevant."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline
            from services.vector_store import ContentChunk

            pipeline = RAGPipeline()

            relevant_chunks = [
                ContentChunk(
                    id="chunk-1",
                    module_id=1,
                    chapter_id=2,
                    section_id="2.1",
                    heading="ROS 2 Nodes",
                    text="A node is a process that performs computation",
                    persona="Default",
                    path="/test",
                    chunk_index=0,
                    relevance_score=0.92,  # Above threshold
                ),
            ]

            is_out_of_scope = pipeline.detect_out_of_scope(
                query="What is a ROS 2 node?",
                search_results=relevant_chunks,
            )

            assert is_out_of_scope is False


class TestContextSummarization:
    """Tests for context window summarization (T045c-T045d)."""

    @pytest.mark.unit
    def test_summarize_context_preserves_recent(self) -> None:
        """summarize_context should preserve recent messages (FR-013)."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline

            pipeline = RAGPipeline()

            history = [
                {"role": "user", "content": "Old question 1"},
                {"role": "assistant", "content": "Old answer 1"},
                {"role": "user", "content": "Old question 2"},
                {"role": "assistant", "content": "Old answer 2"},
                {"role": "user", "content": "Recent question"},
                {"role": "assistant", "content": "Recent answer"},
            ]

            # Small token limit to force summarization
            result = pipeline.summarize_context(history, max_tokens=100)

            # Recent messages should be preserved
            assert "Recent question" in result or "Recent answer" in result

    @pytest.mark.unit
    def test_summarize_context_empty_history(self) -> None:
        """summarize_context should handle empty history."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline

            pipeline = RAGPipeline()

            result = pipeline.summarize_context([], max_tokens=1000)

            assert result == ""


class TestCrossChapterStitching:
    """Tests for cross-chapter context stitching (T045e-T045f)."""

    @pytest.mark.unit
    def test_stitch_cross_chapter_context(self) -> None:
        """stitch_cross_chapter_context should combine chunks with transitions (FR-014)."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline
            from services.vector_store import ContentChunk

            pipeline = RAGPipeline()

            chunks = [
                ContentChunk(
                    id="chunk-1",
                    module_id=1,
                    chapter_id=2,
                    section_id="2.1",
                    heading="Chapter 2 Content",
                    text="Content from chapter 2 about nodes.",
                    persona="Default",
                    path="/chapter-2",
                    chunk_index=0,
                    relevance_score=0.95,
                ),
                ContentChunk(
                    id="chunk-2",
                    module_id=1,
                    chapter_id=3,
                    section_id="3.1",
                    heading="Chapter 3 Content",
                    text="Content from chapter 3 about topics.",
                    persona="Default",
                    path="/chapter-3",
                    chunk_index=0,
                    relevance_score=0.90,
                ),
            ]

            result = pipeline.stitch_cross_chapter_context(chunks)

            # Should contain content from both chapters
            assert "chapter 2" in result.lower() or "nodes" in result.lower()
            assert "chapter 3" in result.lower() or "topics" in result.lower()

    @pytest.mark.unit
    def test_stitch_same_chapter_no_transition(self) -> None:
        """stitch_cross_chapter_context should not add transition for same chapter."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline
            from services.vector_store import ContentChunk

            pipeline = RAGPipeline()

            # Both chunks from same chapter
            chunks = [
                ContentChunk(
                    id="chunk-1",
                    module_id=1,
                    chapter_id=2,
                    section_id="2.1",
                    heading="First Section",
                    text="Content from first section.",
                    persona="Default",
                    path="/chapter-2#section1",
                    chunk_index=0,
                    relevance_score=0.95,
                ),
                ContentChunk(
                    id="chunk-2",
                    module_id=1,
                    chapter_id=2,
                    section_id="2.2",
                    heading="Second Section",
                    text="Content from second section.",
                    persona="Default",
                    path="/chapter-2#section2",
                    chunk_index=0,
                    relevance_score=0.90,
                ),
            ]

            result = pipeline.stitch_cross_chapter_context(chunks)

            # Both contents should be present
            assert "first section" in result.lower()
            assert "second section" in result.lower()


class TestRAGResult:
    """Tests for RAGResult dataclass."""

    @pytest.mark.unit
    def test_rag_result_creation(self) -> None:
        """RAGResult should be creatable with all required fields."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from models.schemas import Citation
            from services.rag import RAGResult

            citations = [
                Citation(
                    chapter=2,
                    section="2.1",
                    heading="Test",
                    quote="Test quote",
                    link="/test",
                    relevance_score=0.9,
                )
            ]

            result = RAGResult(
                context="Retrieved context",
                citations=citations,
                is_out_of_scope=False,
                conflict_warnings=[],
            )

            assert result.context == "Retrieved context"
            assert len(result.citations) == 1
            assert result.is_out_of_scope is False


class TestSelectionQuery:
    """Tests for selection-scoped query handling (T087-T088b)."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_selection_query_uses_selected_text_as_context(self) -> None:
        """selection query should use only selected_text as context (FR-018, FR-019)."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline

            pipeline = RAGPipeline()

            # Mock embedding service - should NOT be called for selection queries
            pipeline._embedding_service = MagicMock()
            pipeline._embedding_service.embed = AsyncMock(return_value=[0.1] * 1536)

            # Mock vector store - should NOT be called for selection queries
            pipeline._vector_store = MagicMock()
            pipeline._vector_store.search = AsyncMock(return_value=[])

            selected_text = "ROS 2 uses a publish-subscribe pattern for communication."
            result = await pipeline.query_selection(
                message="What pattern does ROS 2 use?",
                selected_text=selected_text,
            )

            # Vector store search should NOT be called
            pipeline._vector_store.search.assert_not_called()

            # Context should be the selected text
            assert selected_text in result.context

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_selection_query_skips_vector_search(self) -> None:
        """selection query should skip vector search entirely (FR-018)."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline

            pipeline = RAGPipeline()

            # Mock vector store
            pipeline._vector_store = MagicMock()
            pipeline._vector_store.search = AsyncMock(return_value=[])

            await pipeline.query_selection(
                message="Explain this",
                selected_text="A node is a process that performs computation.",
            )

            # Verify vector store search was NOT called
            pipeline._vector_store.search.assert_not_called()

    @pytest.mark.unit
    def test_check_selection_sufficiency_short_text(self) -> None:
        """check_selection_sufficiency should return False for very short selections (FR-020)."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline

            pipeline = RAGPipeline()

            # Very short selection
            is_sufficient = pipeline.check_selection_sufficiency(
                selected_text="ROS",
                query="What is this?",
            )

            assert is_sufficient is False

    @pytest.mark.unit
    def test_check_selection_sufficiency_adequate_text(self) -> None:
        """check_selection_sufficiency should return True for adequate selections."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline

            pipeline = RAGPipeline()

            # Adequate selection
            is_sufficient = pipeline.check_selection_sufficiency(
                selected_text="ROS 2 is a set of software libraries and tools for building robot applications. It is designed to be modular and flexible.",
                query="What is ROS 2?",
            )

            assert is_sufficient is True

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_selection_query_insufficient_context_message(self) -> None:
        """selection query with insufficient context should return explicit message (FR-020)."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.rag import RAGPipeline

            pipeline = RAGPipeline()

            # Very short selection - should be insufficient
            result = await pipeline.query_selection(
                message="Explain in detail what this means",
                selected_text="Hi",  # Too short
            )

            # Should indicate insufficient context
            assert result.is_insufficient_selection is True
