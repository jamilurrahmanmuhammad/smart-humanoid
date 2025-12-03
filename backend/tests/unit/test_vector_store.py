"""Unit tests for Qdrant vector store client.

TDD: RED phase - these tests should FAIL until T033-T035 are implemented.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestVectorStoreClientInit:
    """Tests for VectorStoreClient initialization (T032-T033)."""

    @pytest.mark.unit
    def test_client_initialization(self) -> None:
        """VectorStoreClient should initialize with settings."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-test-key",
            "QDRANT_COLLECTION_NAME": "textbook_chunks",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.vector_store import VectorStoreClient

            client = VectorStoreClient()

            assert client is not None
            assert client.collection_name == "textbook_chunks"

    @pytest.mark.unit
    def test_client_custom_collection(self) -> None:
        """VectorStoreClient should accept custom collection name."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-test-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.vector_store import VectorStoreClient

            client = VectorStoreClient(collection_name="custom_collection")

            assert client.collection_name == "custom_collection"

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_health_check_healthy(self) -> None:
        """health_check should return True when Qdrant is available."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-test-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.vector_store import VectorStoreClient

            client = VectorStoreClient()

            # Mock the qdrant client
            client._client = MagicMock()
            client._client.get_collections = MagicMock(return_value=MagicMock())

            result = await client.health_check()

            assert result is True

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_health_check_unhealthy(self) -> None:
        """health_check should return False when Qdrant is unavailable."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-test-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.vector_store import VectorStoreClient

            client = VectorStoreClient()

            # Mock connection error
            client._client = MagicMock()
            client._client.get_collections = MagicMock(side_effect=Exception("Connection failed"))

            result = await client.health_check()

            assert result is False


class TestVectorStoreSearch:
    """Tests for vector search functionality (T034-T035)."""

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_search_returns_content_chunks(self) -> None:
        """search should return ContentChunk objects (FR-003)."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-test-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.vector_store import ContentChunk, VectorStoreClient

            client = VectorStoreClient()

            # Mock search response
            mock_point = MagicMock()
            mock_point.id = "chunk-1"
            mock_point.score = 0.95
            mock_point.payload = {
                "module_id": 1,
                "chapter_id": 2,
                "section_id": "2.3.1",
                "heading": "ROS 2 Nodes",
                "text": "A node is a process that performs computation...",
                "persona": "Default",
                "path": "/module-1/chapter-2#nodes",
                "chunk_index": 0,
            }

            # Mock query_points response (has .points attribute)
            mock_response = MagicMock()
            mock_response.points = [mock_point]

            client._client = MagicMock()
            client._client.query_points = MagicMock(return_value=mock_response)

            query_vector = [0.1] * 1536  # Mock embedding
            results = await client.search(query_vector)

            assert len(results) == 1
            assert isinstance(results[0], ContentChunk)
            assert results[0].chapter_id == 2
            assert results[0].heading == "ROS 2 Nodes"
            assert results[0].relevance_score == 0.95

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_search_respects_limit(self) -> None:
        """search should respect the limit parameter."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-test-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.vector_store import VectorStoreClient

            client = VectorStoreClient()

            # Mock multiple results (all above threshold)
            mock_points = []
            for i in range(5):
                point = MagicMock()
                point.id = f"chunk-{i}"
                point.score = 0.9 - (i * 0.05)  # All above 0.5 threshold
                point.payload = {
                    "module_id": 1,
                    "chapter_id": 1,
                    "section_id": "1.1",
                    "heading": f"Section {i}",
                    "text": f"Content {i}",
                    "persona": "Default",
                    "path": f"/test{i}",
                    "chunk_index": i,
                }
                mock_points.append(point)

            # Mock query_points response (has .points attribute)
            mock_response = MagicMock()
            mock_response.points = mock_points

            client._client = MagicMock()
            client._client.query_points = MagicMock(return_value=mock_response)

            query_vector = [0.1] * 1536
            results = await client.search(query_vector, limit=5)

            assert len(results) == 5

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_search_with_chapter_filter(self) -> None:
        """search should apply chapter filter for page-scoped queries."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-test-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.vector_store import SearchFilters, VectorStoreClient

            client = VectorStoreClient()

            mock_point = MagicMock()
            mock_point.id = "chunk-1"
            mock_point.score = 0.9
            mock_point.payload = {
                "module_id": 1,
                "chapter_id": 3,
                "section_id": "3.1",
                "heading": "Test",
                "text": "Content",
                "persona": "Default",
                "path": "/test",
                "chunk_index": 0,
            }

            # Mock query_points response (has .points attribute)
            mock_response = MagicMock()
            mock_response.points = [mock_point]

            client._client = MagicMock()
            client._client.query_points = MagicMock(return_value=mock_response)

            query_vector = [0.1] * 1536
            filters = SearchFilters(chapter_id=3)
            results = await client.search(query_vector, filters=filters)

            # Verify filter was passed to qdrant
            client._client.query_points.assert_called_once()
            call_kwargs = client._client.query_points.call_args[1]
            assert "query_filter" in call_kwargs

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_search_with_similarity_threshold(self) -> None:
        """search should filter results below similarity threshold."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-test-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.vector_store import VectorStoreClient

            client = VectorStoreClient()

            # Mock results with varying scores
            mock_points = []
            for score in [0.95, 0.85, 0.65, 0.55]:  # 2 above 0.7, 2 below
                point = MagicMock()
                point.id = f"chunk-{score}"
                point.score = score
                point.payload = {
                    "module_id": 1,
                    "chapter_id": 1,
                    "section_id": "1.1",
                    "heading": "Test",
                    "text": "Content",
                    "persona": "Default",
                    "path": "/test",
                    "chunk_index": 0,
                }
                mock_points.append(point)

            # Mock query_points response (has .points attribute)
            mock_response = MagicMock()
            mock_response.points = mock_points

            client._client = MagicMock()
            client._client.query_points = MagicMock(return_value=mock_response)

            query_vector = [0.1] * 1536
            results = await client.search(query_vector, similarity_threshold=0.7)

            # Should only return results with score >= 0.7
            assert len(results) == 2
            assert all(r.relevance_score >= 0.7 for r in results)

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_search_handles_empty_results(self) -> None:
        """search should handle empty results gracefully."""
        env_vars = {
            "OPENAI_API_KEY": "sk-test-key",
            "QDRANT_URL": "https://test.qdrant.io",
            "QDRANT_API_KEY": "qdrant-test-key",
            "DATABASE_URL": "postgresql+asyncpg://user:pass@localhost/db",
        }
        with patch.dict(os.environ, env_vars, clear=False):
            from services.vector_store import VectorStoreClient

            client = VectorStoreClient()

            client._client = MagicMock()
            client._client.search = MagicMock(return_value=[])

            query_vector = [0.1] * 1536
            results = await client.search(query_vector)

            assert results == []


class TestContentChunk:
    """Tests for ContentChunk dataclass."""

    @pytest.mark.unit
    def test_content_chunk_creation(self) -> None:
        """ContentChunk should be creatable with all required fields."""
        from services.vector_store import ContentChunk

        chunk = ContentChunk(
            id="chunk-123",
            module_id=1,
            chapter_id=2,
            section_id="2.3.1",
            heading="ROS 2 Nodes",
            text="A node is a process...",
            persona="Default",
            path="/module-1/chapter-2#nodes",
            chunk_index=0,
            relevance_score=0.95,
        )

        assert chunk.id == "chunk-123"
        assert chunk.chapter_id == 2
        assert chunk.relevance_score == 0.95

    @pytest.mark.unit
    def test_content_chunk_to_citation_link(self) -> None:
        """ContentChunk should generate citation link."""
        from services.vector_store import ContentChunk

        chunk = ContentChunk(
            id="chunk-123",
            module_id=1,
            chapter_id=2,
            section_id="2.3.1",
            heading="ROS 2 Nodes",
            text="A node is a process...",
            persona="Default",
            path="/module-1/chapter-2#nodes",
            chunk_index=0,
            relevance_score=0.95,
        )

        assert chunk.path == "/module-1/chapter-2#nodes"


class TestSearchFilters:
    """Tests for SearchFilters dataclass."""

    @pytest.mark.unit
    def test_search_filters_defaults(self) -> None:
        """SearchFilters should have sensible defaults."""
        from services.vector_store import SearchFilters

        filters = SearchFilters()

        assert filters.chapter_id is None
        assert filters.module_id is None
        assert filters.persona is None

    @pytest.mark.unit
    def test_search_filters_with_values(self) -> None:
        """SearchFilters should accept filter values."""
        from services.vector_store import SearchFilters

        filters = SearchFilters(
            chapter_id=3,
            module_id=1,
            persona="Explorer",
        )

        assert filters.chapter_id == 3
        assert filters.module_id == 1
        assert filters.persona == "Explorer"
