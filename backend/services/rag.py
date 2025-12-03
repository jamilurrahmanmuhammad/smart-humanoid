"""RAG pipeline orchestration service.

Coordinates vector search, context building, and agent execution.
"""

import re
from dataclasses import dataclass, field
from typing import Any, Optional

from core.config import get_settings
from models.schemas import Citation
from services.citation import CitationExtractor, ConflictWarning
from services.embedding import EmbeddingService
from services.vector_store import ContentChunk, SearchFilters, VectorStoreClient


# Patterns that indicate vague contextual queries (FR-033)
# These queries need page content context to be answered
VAGUE_QUERY_PATTERNS = [
    r"\bexplain\s+this\b",
    r"\bwhat\s+is\s+this\b",
    r"\bwhat'?s\s+this\b",
    r"\bsummarize\s+this\b",
    r"\btell\s+me\s+about\s+this\b",
    r"\bwhat\s+does\s+this\s+(page\s+)?cover\b",
    r"\bhelp\s+me\s+understand\s+this\b",
    r"\bwhat\s+am\s+i\s+looking\s+at\b",
    r"\bdescribe\s+this\b",
    r"\bgive\s+me\s+an\s+overview\b",
    r"\boverview\s+of\s+this\b",
    r"\bwhat'?s\s+the\s+topic\s+here\b",
    r"\bwhat\s+topic\s+is\s+this\b",
    r"\bcan\s+you\s+explain\s+this\b",
    r"\bwhat\s+is\s+this\s+about\b",
    r"\bwhat'?s\s+this\s+about\b",
    r"\bbreak\s+this\s+down\b",
    r"\bwhat'?s\s+going\s+on\s+here\b",
]

# Technical terms that indicate a specific query (not vague)
SPECIFIC_QUERY_INDICATORS = [
    r"\bROS\b",
    r"\bURDF\b",
    r"\bnode[s]?\b",
    r"\btopic[s]?\b",
    r"\bservice[s]?\b",
    r"\bpublisher[s]?\b",
    r"\bsubscriber[s]?\b",
    r"\bdocker\b",
    r"\bcontainer[s]?\b",
    r"\bkinematic[s]?\b",
    r"\bMoveIt\b",
    r"\bgazebo\b",
    r"\bsimulat",  # simulation, simulator, etc.
    r"\bembodied\b",
    r"\bintelligence\b",
    r"\bframework\b",
    r"\bprogramming\b",
    r"\blanguage[s]?\b",
]


def is_vague_contextual_query(query: str) -> bool:
    """Detect if a query is vague and needs page content context.

    Vague contextual queries are requests like "explain this page" or
    "what is this about" that cannot be answered without knowing what
    page the user is currently viewing.

    Args:
        query: User query string.

    Returns:
        True if query is vague and contextual, False otherwise.

    FR Reference: FR-033
    """
    if not query or not query.strip():
        return False

    query_lower = query.lower().strip()

    # First check if query contains specific technical terms
    # If so, it's a specific query even if it has vague patterns
    for pattern in SPECIFIC_QUERY_INDICATORS:
        if re.search(pattern, query_lower, re.IGNORECASE):
            return False

    # Check for vague contextual patterns
    for pattern in VAGUE_QUERY_PATTERNS:
        if re.search(pattern, query_lower, re.IGNORECASE):
            return True

    return False


@dataclass
class RAGResult:
    """Result from RAG pipeline query.

    Contains retrieved context, extracted citations, and metadata.
    """

    context: str
    citations: list[Citation]
    is_out_of_scope: bool
    conflict_warnings: list[ConflictWarning] = field(default_factory=list)
    is_insufficient_selection: bool = False


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
        is_page_scoped: bool = False,
    ) -> RAGResult:
        """Execute RAG query pipeline.

        Args:
            message: User query message.
            filters: Optional search filters (chapter, module, persona).
            session_context: Optional conversation history.
            max_citations: Maximum number of citations to return.
            is_page_scoped: If True, skip out-of-scope detection (user wants page content).

        Returns:
            RAGResult containing context, citations, and metadata.

        FR References: FR-001, FR-003, FR-004
        """
        # Step 1: Embed the query
        query_vector = await self._embedding_service.embed(message)

        # Step 2: Search vector store
        # For page-scoped queries, use lower similarity threshold to get more results
        similarity_threshold = 0.3 if is_page_scoped else None
        chunks = await self._vector_store.search(
            query_vector=query_vector,
            filters=filters,
            limit=max_citations * 2,  # Get more for deduplication
            similarity_threshold=similarity_threshold,
        )

        # Step 3: Check for out-of-scope query
        # Skip out-of-scope detection for page-scoped queries with valid chapter
        is_out_of_scope = False
        if not is_page_scoped:
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

    # Minimum characters for a selection to be considered sufficient
    MIN_SELECTION_LENGTH = 20

    def check_selection_sufficiency(
        self,
        selected_text: str,
        query: str,
    ) -> bool:
        """Check if selected text has sufficient context to answer the query.

        Args:
            selected_text: User-selected text.
            query: User query about the selection.

        Returns:
            True if selection has adequate context, False otherwise.

        FR Reference: FR-020
        """
        # Check minimum length
        if len(selected_text.strip()) < self.MIN_SELECTION_LENGTH:
            return False

        # Check if selection has enough words (at least 3)
        word_count = len(selected_text.strip().split())
        if word_count < 3:
            return False

        return True

    async def query_selection(
        self,
        message: str,
        selected_text: str,
    ) -> RAGResult:
        """Execute selection-scoped query using only selected text as context.

        Does NOT perform vector search - uses selected text directly.

        Args:
            message: User query about the selection.
            selected_text: User-selected text to use as context.

        Returns:
            RAGResult with selection as context, no citations from search.

        FR References: FR-018 (selection-scoped), FR-019 (selection indicator),
                       FR-020 (insufficient selection)
        """
        # Check if selection is sufficient
        is_sufficient = self.check_selection_sufficiency(selected_text, message)

        if not is_sufficient:
            return RAGResult(
                context="",
                citations=[],
                is_out_of_scope=False,
                conflict_warnings=[],
                is_insufficient_selection=True,
            )

        # Build context from selection
        context = f"[User Selected Text]\n{selected_text}"

        return RAGResult(
            context=context,
            citations=[],  # No citations for selection-scoped queries
            is_out_of_scope=False,
            conflict_warnings=[],
            is_insufficient_selection=False,
        )
