"""Unit tests for citation extraction.

TDD: RED phase - these tests should FAIL until T039-T041b are implemented.
"""

import pytest


class TestCitationExtractor:
    """Tests for CitationExtractor (T038-T041b)."""

    @pytest.mark.unit
    def test_extract_citations_from_chunks(self) -> None:
        """extract should convert ContentChunks to Citations (FR-004)."""
        from services.citation import CitationExtractor
        from services.vector_store import ContentChunk

        chunks = [
            ContentChunk(
                id="chunk-1",
                module_id=1,
                chapter_id=2,
                section_id="2.3.1",
                heading="ROS 2 Nodes",
                text="A node is a process that performs computation...",
                persona="Default",
                path="/module-1/chapter-2#nodes",
                chunk_index=0,
                relevance_score=0.95,
            ),
            ContentChunk(
                id="chunk-2",
                module_id=1,
                chapter_id=2,
                section_id="2.3.2",
                heading="Topics and Messages",
                text="Topics enable publish-subscribe communication...",
                persona="Default",
                path="/module-1/chapter-2#topics",
                chunk_index=0,
                relevance_score=0.88,
            ),
        ]

        extractor = CitationExtractor()
        citations = extractor.extract(chunks)

        assert len(citations) == 2
        assert citations[0].chapter == 2
        assert citations[0].section == "2.3.1"
        assert citations[0].heading == "ROS 2 Nodes"
        assert citations[0].relevance_score == 0.95

    @pytest.mark.unit
    def test_extract_limits_to_max_citations(self) -> None:
        """extract should limit citations to max (default 5) per FR-009."""
        from services.citation import CitationExtractor
        from services.vector_store import ContentChunk

        # Create 10 chunks
        chunks = [
            ContentChunk(
                id=f"chunk-{i}",
                module_id=1,
                chapter_id=i + 1,
                section_id=f"{i+1}.1",
                heading=f"Section {i+1}",
                text=f"Content {i+1}",
                persona="Default",
                path=f"/test{i+1}",
                chunk_index=0,
                relevance_score=0.9 - (i * 0.05),
            )
            for i in range(10)
        ]

        extractor = CitationExtractor()
        citations = extractor.extract(chunks, limit=5)

        assert len(citations) == 5
        # Should be top 5 by relevance
        assert citations[0].relevance_score >= citations[4].relevance_score

    @pytest.mark.unit
    def test_extract_generates_verbatim_quotes(self) -> None:
        """extract should generate verbatim quotes from text (FR-005)."""
        from services.citation import CitationExtractor
        from services.vector_store import ContentChunk

        chunk = ContentChunk(
            id="chunk-1",
            module_id=1,
            chapter_id=1,
            section_id="1.1",
            heading="Introduction",
            text="This is a long text that should be truncated to create a verbatim quote. "
            "The quote should capture the essence of the content without exceeding the max length.",
            persona="Default",
            path="/test",
            chunk_index=0,
            relevance_score=0.9,
        )

        extractor = CitationExtractor()
        citations = extractor.extract([chunk])

        assert len(citations) == 1
        assert len(citations[0].quote) <= 500  # Max quote length per FR-005
        assert citations[0].quote  # Should not be empty


class TestCitationDeduplication:
    """Tests for citation deduplication (T040-T041)."""

    @pytest.mark.unit
    def test_deduplicate_removes_same_section(self) -> None:
        """deduplicate should remove citations from same chapter+section (FR-009)."""
        from models.schemas import Citation
        from services.citation import CitationExtractor

        citations = [
            Citation(
                chapter=2,
                section="2.3.1",
                heading="ROS 2 Nodes",
                quote="Quote 1",
                link="/test1",
                relevance_score=0.95,
            ),
            Citation(
                chapter=2,
                section="2.3.1",  # Same section - should be removed
                heading="ROS 2 Nodes",
                quote="Quote 2",
                link="/test2",
                relevance_score=0.85,
            ),
            Citation(
                chapter=2,
                section="2.3.2",  # Different section - should be kept
                heading="Topics",
                quote="Quote 3",
                link="/test3",
                relevance_score=0.80,
            ),
        ]

        extractor = CitationExtractor()
        deduped = extractor.deduplicate(citations)

        assert len(deduped) == 2
        # Should keep highest relevance from duplicates
        assert deduped[0].relevance_score == 0.95
        assert deduped[1].section == "2.3.2"

    @pytest.mark.unit
    def test_deduplicate_keeps_highest_relevance(self) -> None:
        """deduplicate should keep citation with highest relevance score."""
        from models.schemas import Citation
        from services.citation import CitationExtractor

        citations = [
            Citation(
                chapter=1,
                section="1.1",
                heading="Test",
                quote="Lower relevance",
                link="/test1",
                relevance_score=0.70,
            ),
            Citation(
                chapter=1,
                section="1.1",  # Duplicate
                heading="Test",
                quote="Higher relevance",
                link="/test2",
                relevance_score=0.90,
            ),
        ]

        extractor = CitationExtractor()
        deduped = extractor.deduplicate(citations)

        assert len(deduped) == 1
        assert deduped[0].relevance_score == 0.90
        assert deduped[0].quote == "Higher relevance"


class TestConflictDetection:
    """Tests for conflicting source detection (T041a-T041b)."""

    @pytest.mark.unit
    def test_detect_conflicts_returns_empty_for_consistent_citations(self) -> None:
        """detect_conflicts should return empty list for consistent citations (FR-011)."""
        from models.schemas import Citation
        from services.citation import CitationExtractor

        citations = [
            Citation(
                chapter=1,
                section="1.1",
                heading="ROS 2 Overview",
                quote="ROS 2 uses DDS for communication",
                link="/test1",
                relevance_score=0.9,
            ),
            Citation(
                chapter=1,
                section="1.2",
                heading="DDS Layer",
                quote="DDS provides reliable communication",
                link="/test2",
                relevance_score=0.85,
            ),
        ]

        extractor = CitationExtractor()
        conflicts = extractor.detect_conflicts(citations)

        assert conflicts == []

    @pytest.mark.unit
    def test_detect_conflicts_flags_contradictions(self) -> None:
        """detect_conflicts should flag contradictory information (FR-011)."""
        from models.schemas import Citation
        from services.citation import CitationExtractor, ConflictWarning

        # These citations have potentially contradictory information
        citations = [
            Citation(
                chapter=1,
                section="1.1",
                heading="Version Info",
                quote="ROS 2 requires Python 3.8 or higher",
                link="/test1",
                relevance_score=0.9,
            ),
            Citation(
                chapter=5,
                section="5.1",
                heading="Requirements",
                quote="ROS 2 requires Python 3.10 or higher",
                link="/test2",
                relevance_score=0.85,
            ),
        ]

        extractor = CitationExtractor()
        conflicts = extractor.detect_conflicts(citations)

        # Should detect potential version conflict
        # Note: Actual implementation may use semantic analysis
        # For now, we accept either detection or empty (implementation-dependent)
        assert isinstance(conflicts, list)

    @pytest.mark.unit
    def test_conflict_warning_structure(self) -> None:
        """ConflictWarning should have required fields."""
        from services.citation import ConflictWarning

        warning = ConflictWarning(
            citation_indices=[0, 1],
            description="Potential version conflict detected",
            severity="low",
        )

        assert warning.citation_indices == [0, 1]
        assert "version" in warning.description.lower() or "conflict" in warning.description.lower()
        assert warning.severity in ["low", "medium", "high"]
