"""RAG pipeline orchestration service.

Coordinates vector search, context building, and agent execution.
"""

from dataclasses import dataclass, field
from typing import Any, Optional

from core.config import get_settings
from models.schemas import Citation
from services.citation import CitationExtractor, ConflictWarning
from services.embedding import EmbeddingService
from services.vector_store import ContentChunk, SearchFilters, VectorStoreClient


@dataclass
class RAGResult:
    """Result from RAG pipeline query.

    Contains retrieved context, extracted citations, and metadata.
    """

    context: str
    citations: list[Citation]
    is_out_of_scope: bool
    conflict_warnings: list[ConflictWarning] = field(default_factory=list)


class RAGPipeline:
    """Orchestrates RAG query flow.

    Coordinates:
    1. Query embedding generation
    2. Vector store search with filtering
    3. Context building from retrieved chunks
    4. Citation extraction and deduplication
    5. Out-of-scope query detection

    FR References:
    - FR-001: RAG-based Q&A
    - FR-003: Query types (global, page, selection)
    - FR-004: Inline citations
    - FR-006, FR-007: Out-of-scope handling
    - FR-013: Context summarization
    - FR-014: Cross-chapter stitching
    """

    # Relevance threshold for out-of-scope detection
    RELEVANCE_THRESHOLD = 0.5

    # Approximate characters per token (for rough estimation)
    CHARS_PER_TOKEN = 4

    def __init__(self) -> None:
        """Initialize RAG pipeline with dependencies."""
        settings = get_settings()

        self._embedding_service = EmbeddingService()
        self._vector_store = VectorStoreClient()
        self._citation_extractor = CitationExtractor()
        self._max_context_tokens = settings.rag_max_context_tokens

    async def query(
        self,
        message: str,
        filters: Optional[SearchFilters] = None,
        session_context: Optional[list[dict[str, Any]]] = None,
        max_citations: int = 5,
    ) -> RAGResult:
        """Execute RAG query pipeline.

        Args:
            message: User query message.
            filters: Optional search filters (chapter, module, persona).
            session_context: Optional conversation history.
            max_citations: Maximum number of citations to return.

        Returns:
            RAGResult containing context, citations, and metadata.

        FR References: FR-001, FR-003, FR-004
        """
        # Step 1: Embed the query
        query_vector = await self._embedding_service.embed(message)

        # Step 2: Search vector store
        chunks = await self._vector_store.search(
            query_vector=query_vector,
            filters=filters,
            limit=max_citations * 2,  # Get more for deduplication
        )

        # Step 3: Check for out-of-scope query
        is_out_of_scope = self.detect_out_of_scope(message, chunks)

        if is_out_of_scope:
            return RAGResult(
                context="",
                citations=[],
                is_out_of_scope=True,
                conflict_warnings=[],
            )

        # Step 4: Build context from chunks
        context = self.stitch_cross_chapter_context(chunks)

        # Step 5: Extract and deduplicate citations
        citations = self._citation_extractor.extract(chunks, limit=max_citations)
        citations = self._citation_extractor.deduplicate(citations)

        # Step 6: Detect conflicts
        conflict_warnings = self._citation_extractor.detect_conflicts(citations)

        return RAGResult(
            context=context,
            citations=citations,
            is_out_of_scope=False,
            conflict_warnings=conflict_warnings,
        )

    def build_context(
        self,
        chunks: list[ContentChunk],
        max_tokens: int = 2000,
    ) -> str:
        """Build context string from content chunks.

        Args:
            chunks: Retrieved content chunks.
            max_tokens: Maximum tokens for context.

        Returns:
            Formatted context string within token limit.
        """
        if not chunks:
            return ""

        # Estimate max characters from tokens
        max_chars = max_tokens * self.CHARS_PER_TOKEN

        context_parts = []
        current_length = 0

        for chunk in chunks:
            # Format chunk with heading
            chunk_text = f"[{chunk.heading}]\n{chunk.text}\n"
            chunk_length = len(chunk_text)

            # Check if adding this chunk exceeds limit
            if current_length + chunk_length > max_chars:
                # Add truncated version if there's room
                remaining = max_chars - current_length
                if remaining > 50:  # Only add if meaningful space left
                    truncated = chunk_text[:remaining - 3] + "..."
                    context_parts.append(truncated)
                break

            context_parts.append(chunk_text)
            current_length += chunk_length

        return "\n".join(context_parts)

    def detect_out_of_scope(
        self,
        query: str,
        search_results: list[ContentChunk],
    ) -> bool:
        """Detect if query is out of scope based on search results.

        Args:
            query: User query string.
            search_results: Vector search results.

        Returns:
            True if query appears to be out of scope.

        FR Reference: FR-006, FR-007
        """
        if not search_results:
            return True

        # Check if best result is above relevance threshold
        max_relevance = max(chunk.relevance_score for chunk in search_results)
        return max_relevance < self.RELEVANCE_THRESHOLD

    def summarize_context(
        self,
        history: list[dict[str, str]],
        max_tokens: int = 500,
    ) -> str:
        """Summarize conversation history for context window management.

        Preserves recent messages while summarizing older ones.

        Args:
            history: Conversation history (list of role/content dicts).
            max_tokens: Maximum tokens for summarized context.

        Returns:
            Summarized context string.

        FR Reference: FR-013
        """
        if not history:
            return ""

        max_chars = max_tokens * self.CHARS_PER_TOKEN

        # Always preserve the most recent exchange
        recent_count = min(2, len(history))
        recent = history[-recent_count:]
        older = history[:-recent_count] if len(history) > recent_count else []

        # Format recent messages
        recent_text = ""
        for msg in recent:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            recent_text += f"{role.capitalize()}: {content}\n"

        # If recent fits in budget, try to include summary of older
        if len(recent_text) < max_chars and older:
            # Simple summarization: count exchanges
            summary = f"[Previous {len(older)} messages summarized]\n"
            if len(summary) + len(recent_text) < max_chars:
                return summary + recent_text

        # Truncate recent if still too long
        if len(recent_text) > max_chars:
            recent_text = recent_text[:max_chars - 3] + "..."

        return recent_text

    def stitch_cross_chapter_context(
        self,
        chunks: list[ContentChunk],
    ) -> str:
        """Combine chunks from different chapters with transition markers.

        Args:
            chunks: Content chunks potentially from multiple chapters.

        Returns:
            Stitched context with chapter transitions.

        FR Reference: FR-014
        """
        if not chunks:
            return ""

        context_parts = []
        current_chapter: Optional[int] = None

        for chunk in chunks:
            # Add chapter transition marker if chapter changes
            if current_chapter is not None and chunk.chapter_id != current_chapter:
                context_parts.append(
                    f"\n--- From Chapter {chunk.chapter_id} ---\n"
                )
            elif current_chapter is None:
                # First chunk - add chapter marker
                context_parts.append(f"--- From Chapter {chunk.chapter_id} ---\n")

            current_chapter = chunk.chapter_id

            # Add chunk content with heading
            context_parts.append(f"[{chunk.heading}]\n{chunk.text}\n")

        return "\n".join(context_parts)
