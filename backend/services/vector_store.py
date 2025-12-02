"""Qdrant vector store client wrapper.

Handles vector search with filtering for RAG retrieval.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from core.config import get_settings

# Thread pool for running sync Qdrant calls
_executor = ThreadPoolExecutor(max_workers=4)


@dataclass
class ContentChunk:
    """Content chunk retrieved from vector store.

    Represents indexed textbook content with metadata.
    """

    id: str
    module_id: int
    chapter_id: int
    section_id: str
    heading: str
    text: str
    persona: str
    path: str
    chunk_index: int
    relevance_score: float


@dataclass
class SearchFilters:
    """Filters for vector search.

    Used to scope searches to specific chapters, modules, or personas.
    """

    chapter_id: Optional[int] = None
    module_id: Optional[int] = None
    persona: Optional[str] = None


class VectorStoreClient:
    """Client for Qdrant vector store operations.

    Provides search functionality with filtering for RAG retrieval.
    Uses sync client with thread pool for reliable async compatibility.
    FR Reference: FR-003 (query types with filters)
    """

    def __init__(self, collection_name: Optional[str] = None) -> None:
        """Initialize vector store client.

        Args:
            collection_name: Qdrant collection name. Defaults to settings value.
        """
        settings = get_settings()

        self.collection_name = collection_name or settings.qdrant_collection_name
        self._similarity_threshold = settings.rag_similarity_threshold

        # Initialize sync Qdrant client (will run in thread pool)
        self._client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key.get_secret_value(),
            timeout=30,
        )

    async def health_check(self) -> bool:
        """Check if vector store is healthy.

        Returns:
            True if Qdrant is accessible, False otherwise.
        """
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(_executor, self._client.get_collections)
            return True
        except Exception:
            return False

    async def search(
        self,
        query_vector: list[float],
        filters: Optional[SearchFilters] = None,
        limit: int = 10,
        similarity_threshold: Optional[float] = None,
    ) -> list[ContentChunk]:
        """Search for similar content chunks.

        Args:
            query_vector: Query embedding vector (1536 dimensions).
            filters: Optional filters for chapter, module, or persona.
            limit: Maximum number of results to return.
            similarity_threshold: Minimum similarity score (0-1).

        Returns:
            List of ContentChunk objects sorted by relevance.

        FR Reference: FR-003 (global, page-scoped, selection-scoped queries)
        """
        import logging
        logger = logging.getLogger(__name__)

        threshold = similarity_threshold or self._similarity_threshold

        # Build Qdrant filter
        query_filter = self._build_filter(filters) if filters else None

        logger.info(f"Searching collection={self.collection_name}")
        logger.info(f"Query vector length: {len(query_vector)}, limit={limit}")

        # Run sync query in thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            _executor,
            lambda: self._client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                query_filter=query_filter,
                with_payload=True,
            )
        )
        results = response.points
        logger.info(f"Query returned {len(results)} points")

        # Convert to ContentChunk objects and filter by threshold
        chunks = []
        for point in results:
            if point.score >= threshold:
                chunk = ContentChunk(
                    id=str(point.id),
                    module_id=point.payload.get("module_id", 0),
                    chapter_id=point.payload.get("chapter_id", 0),
                    section_id=point.payload.get("section_id", ""),
                    heading=point.payload.get("heading", ""),
                    text=point.payload.get("text", ""),
                    persona=point.payload.get("persona", "Default"),
                    path=point.payload.get("path", ""),
                    chunk_index=point.payload.get("chunk_index", 0),
                    relevance_score=point.score,
                )
                chunks.append(chunk)

        logger.info(f"Returning {len(chunks)} chunks (threshold={threshold})")
        return chunks

    def _build_filter(self, filters: SearchFilters) -> Optional[Filter]:
        """Build Qdrant filter from SearchFilters.

        Args:
            filters: Search filters to apply.

        Returns:
            Qdrant Filter object or None if no filters.
        """
        conditions = []

        if filters.chapter_id is not None:
            conditions.append(
                FieldCondition(
                    key="chapter_id",
                    match=MatchValue(value=filters.chapter_id),
                )
            )

        if filters.module_id is not None:
            conditions.append(
                FieldCondition(
                    key="module_id",
                    match=MatchValue(value=filters.module_id),
                )
            )

        if filters.persona is not None:
            conditions.append(
                FieldCondition(
                    key="persona",
                    match=MatchValue(value=filters.persona),
                )
            )

        if not conditions:
            return None

        return Filter(must=conditions)
