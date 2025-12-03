"""Tests for vague contextual query detection.

T121: Test vague query detection patterns.
FR Reference: FR-033 - System MUST use page content for vague contextual queries.
"""

import pytest

from services.rag import is_vague_contextual_query


class TestVagueQueryDetection:
    """Test cases for is_vague_contextual_query function."""

    # Vague contextual queries that SHOULD return True
    @pytest.mark.parametrize(
        "query",
        [
            "explain this page",
            "Explain this page",
            "EXPLAIN THIS PAGE",
            "what is this about",
            "What is this about?",
            "what's this about",
            "summarize this",
            "summarize this page",
            "Summarize this for me",
            "tell me about this page",
            "Tell me about this",
            "what does this page cover",
            "what does this cover",
            "can you explain this",
            "help me understand this page",
            "what am I looking at",
            "what is this",
            "what's this",
            "describe this page",
            "give me an overview",
            "overview of this page",
            "break this down for me",
            "what's going on here",
        ],
    )
    def test_vague_queries_return_true(self, query: str) -> None:
        """Vague contextual queries should return True."""
        assert is_vague_contextual_query(query) is True

    # Specific queries that SHOULD return False
    @pytest.mark.parametrize(
        "query",
        [
            "what is ROS 2?",
            "What is ROS 2?",
            "how do nodes work?",
            "explain ROS 2 nodes",
            "what is a topic in ROS?",
            "how does message passing work",
            "what is URDF",
            "explain the difference between topics and services",
            "how do I create a publisher",
            "what are the benefits of ROS 2 over ROS 1",
            "can you explain docker containers",
            "what is embodied intelligence",
            "how does inverse kinematics work",
            "explain the MoveIt framework",
            "what programming languages does ROS support",
        ],
    )
    def test_specific_queries_return_false(self, query: str) -> None:
        """Specific technical queries should return False."""
        assert is_vague_contextual_query(query) is False

    # Edge cases
    def test_empty_query_returns_false(self) -> None:
        """Empty query should return False."""
        assert is_vague_contextual_query("") is False

    def test_whitespace_query_returns_false(self) -> None:
        """Whitespace-only query should return False."""
        assert is_vague_contextual_query("   ") is False

    def test_mixed_vague_and_specific_returns_false(self) -> None:
        """Query with both vague and specific content should return False."""
        # If user asks about specific content, treat as specific
        assert is_vague_contextual_query("explain this page about ROS 2 nodes") is False
        assert is_vague_contextual_query("summarize the URDF section") is False

    def test_question_variations(self) -> None:
        """Different question formats should be handled."""
        assert is_vague_contextual_query("what is this?") is True
        assert is_vague_contextual_query("what is this") is True
        assert is_vague_contextual_query("What is this!") is True
