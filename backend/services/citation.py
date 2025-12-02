"""Citation extraction and processing service.

Converts vector search results to citations with deduplication and conflict detection.
"""

from dataclasses import dataclass
from typing import Literal

from models.schemas import Citation
from services.vector_store import ContentChunk


@dataclass
class ConflictWarning:
    """Warning about potentially conflicting information in citations.

    FR Reference: FR-011 (flag conflicting sources)
    """

    citation_indices: list[int]
    description: str
    severity: Literal["low", "medium", "high"]


class CitationExtractor:
    """Extracts and processes citations from content chunks.

    Converts ContentChunks to Citations, handles deduplication,
    and detects potentially conflicting information.

    FR References:
    - FR-004: Inline citations
    - FR-005: Verbatim quotes
    - FR-009: Max 5 citations
    - FR-011: Flag conflicting sources
    """

    MAX_QUOTE_LENGTH = 500

    def extract(
        self,
        chunks: list[ContentChunk],
        limit: int = 5,
    ) -> list[Citation]:
        """Extract citations from content chunks.

        Args:
            chunks: List of ContentChunks from vector search.
            limit: Maximum number of citations to return (default 5 per FR-009).

        Returns:
            List of Citation objects sorted by relevance score.
        """
        if not chunks:
            return []

        # Sort by relevance score (descending)
        sorted_chunks = sorted(chunks, key=lambda c: c.relevance_score, reverse=True)

        # Convert to citations
        citations = []
        for chunk in sorted_chunks[:limit]:
            quote = self._generate_quote(chunk.text)
            citation = Citation(
                chapter=chunk.chapter_id,
                section=chunk.section_id,
                heading=chunk.heading,
                quote=quote,
                link=chunk.path,
                relevance_score=chunk.relevance_score,
            )
            citations.append(citation)

        return citations

    def deduplicate(self, citations: list[Citation]) -> list[Citation]:
        """Remove duplicate citations from the same chapter+section.

        Keeps the citation with the highest relevance score for each
        unique (chapter, section) combination.

        Args:
            citations: List of citations to deduplicate.

        Returns:
            Deduplicated list of citations.

        FR Reference: FR-009 (unique citations)
        """
        if not citations:
            return []

        # Group by (chapter, section) and keep highest relevance
        seen: dict[tuple[int, str], Citation] = {}

        for citation in citations:
            key = (citation.chapter, citation.section)
            if key not in seen or citation.relevance_score > seen[key].relevance_score:
                seen[key] = citation

        # Return sorted by relevance score
        return sorted(seen.values(), key=lambda c: c.relevance_score, reverse=True)

    def detect_conflicts(self, citations: list[Citation]) -> list[ConflictWarning]:
        """Detect potentially conflicting information across citations.

        Uses simple heuristics to identify citations that may contain
        contradictory information (e.g., different version numbers,
        conflicting requirements).

        Args:
            citations: List of citations to analyze.

        Returns:
            List of ConflictWarning objects for detected conflicts.

        FR Reference: FR-011 (flag conflicting sources)
        """
        if len(citations) < 2:
            return []

        conflicts: list[ConflictWarning] = []

        # Simple heuristic: look for version number conflicts
        # This is a basic implementation - could be enhanced with NLP
        for i, cite_a in enumerate(citations):
            for j, cite_b in enumerate(citations[i + 1 :], start=i + 1):
                conflict = self._check_version_conflict(cite_a, cite_b, i, j)
                if conflict:
                    conflicts.append(conflict)

        return conflicts

    def _generate_quote(self, text: str) -> str:
        """Generate a verbatim quote from text, truncating if needed.

        Args:
            text: Source text to create quote from.

        Returns:
            Quote string, truncated to MAX_QUOTE_LENGTH if necessary.

        FR Reference: FR-005 (verbatim quotes)
        """
        if not text:
            return ""

        if len(text) <= self.MAX_QUOTE_LENGTH:
            return text

        # Truncate at word boundary and add ellipsis
        truncated = text[: self.MAX_QUOTE_LENGTH - 3]
        last_space = truncated.rfind(" ")
        if last_space > 0:
            truncated = truncated[:last_space]

        return truncated + "..."

    def _check_version_conflict(
        self,
        cite_a: Citation,
        cite_b: Citation,
        idx_a: int,
        idx_b: int,
    ) -> ConflictWarning | None:
        """Check if two citations have conflicting version information.

        Args:
            cite_a: First citation.
            cite_b: Second citation.
            idx_a: Index of first citation.
            idx_b: Index of second citation.

        Returns:
            ConflictWarning if conflict detected, None otherwise.
        """
        import re

        # Extract version patterns (e.g., "3.8", "3.10", "2.0")
        version_pattern = r"\d+\.\d+"

        versions_a = set(re.findall(version_pattern, cite_a.quote))
        versions_b = set(re.findall(version_pattern, cite_b.quote))

        # Check for conflicting versions in similar contexts
        # This is a simplified heuristic
        if versions_a and versions_b:
            # Look for Python version conflicts
            python_pattern = r"Python\s+(\d+\.\d+)"
            py_versions_a = set(re.findall(python_pattern, cite_a.quote, re.IGNORECASE))
            py_versions_b = set(re.findall(python_pattern, cite_b.quote, re.IGNORECASE))

            if py_versions_a and py_versions_b and py_versions_a != py_versions_b:
                return ConflictWarning(
                    citation_indices=[idx_a, idx_b],
                    description=f"Potential Python version conflict: {py_versions_a} vs {py_versions_b}",
                    severity="medium",
                )

        return None
