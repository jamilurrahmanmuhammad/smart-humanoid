"""Unit tests for analytics service.

TDD: RED phase - tests for T091-T096 analytics tasks.
"""

import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest


class TestAnalyticsEventCreation:
    """Tests for AnalyticsService event creation (T091-T092)."""

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

    @pytest.mark.unit
    def test_create_analytics_event(self, mock_env) -> None:
        """AnalyticsService should create events with correct payload (FR-025)."""
        from services.analytics import AnalyticsService, AnalyticsEvent

        service = AnalyticsService()

        event = service.create_event(
            event_type="query_received",
            session_id="session-123",
            message_id="msg-456",
            persona="Explorer",
            chapter=2,
            query_type="global",
        )

        assert isinstance(event, AnalyticsEvent)
        assert event.event_type == "query_received"
        assert event.session_id == "session-123"
        assert event.message_id == "msg-456"
        assert event.persona == "Explorer"
        assert event.chapter == 2
        assert event.query_type == "global"

    @pytest.mark.unit
    def test_analytics_event_no_pii(self, mock_env) -> None:
        """AnalyticsEvent should NOT contain PII fields (FR-026)."""
        from services.analytics import AnalyticsService

        service = AnalyticsService()

        event = service.create_event(
            event_type="response_sent",
            session_id="session-123",
            message_id="msg-456",
            persona="Builder",
            chapter=3,
            query_type="page",
        )

        # Verify no PII fields exist
        event_dict = event.to_dict()
        pii_fields = {"user_id", "email", "ip_address", "user_agent", "content", "message_text"}
        assert not any(field in event_dict for field in pii_fields)

    @pytest.mark.unit
    def test_analytics_event_has_timestamp(self, mock_env) -> None:
        """AnalyticsEvent should include timestamp."""
        from services.analytics import AnalyticsService

        service = AnalyticsService()

        event = service.create_event(
            event_type="query_received",
            session_id="session-123",
            message_id="msg-456",
            persona="Default",
            chapter=1,
            query_type="global",
        )

        assert event.timestamp is not None
        assert isinstance(event.timestamp, datetime)

    @pytest.mark.unit
    def test_analytics_event_types(self, mock_env) -> None:
        """AnalyticsService should support required event types."""
        from services.analytics import AnalyticsService, EventType

        # Should have query_received and response_sent event types
        assert EventType.QUERY_RECEIVED == "query_received"
        assert EventType.RESPONSE_SENT == "response_sent"


class TestLatencyTracking:
    """Tests for latency tracking (T095-T096)."""

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

    @pytest.mark.unit
    def test_track_first_token_latency(self, mock_env) -> None:
        """AnalyticsService should track first_token_ms (NFR-001)."""
        from services.analytics import AnalyticsService

        service = AnalyticsService()

        event = service.create_response_event(
            session_id="session-123",
            message_id="msg-456",
            persona="Explorer",
            chapter=2,
            query_type="global",
            has_citations=True,
            has_safety_disclaimer=False,
            first_token_ms=150,
            total_ms=2500,
        )

        assert event.first_token_ms == 150

    @pytest.mark.unit
    def test_track_total_latency(self, mock_env) -> None:
        """AnalyticsService should track total_ms."""
        from services.analytics import AnalyticsService

        service = AnalyticsService()

        event = service.create_response_event(
            session_id="session-123",
            message_id="msg-456",
            persona="Builder",
            chapter=3,
            query_type="page",
            has_citations=False,
            has_safety_disclaimer=True,
            first_token_ms=200,
            total_ms=3000,
        )

        assert event.total_ms == 3000

    @pytest.mark.unit
    def test_response_event_includes_citation_flag(self, mock_env) -> None:
        """Response event should include has_citations flag."""
        from services.analytics import AnalyticsService

        service = AnalyticsService()

        event = service.create_response_event(
            session_id="session-123",
            message_id="msg-456",
            persona="Engineer",
            chapter=4,
            query_type="selection",
            has_citations=True,
            has_safety_disclaimer=False,
            first_token_ms=100,
            total_ms=2000,
        )

        assert event.has_citations is True

    @pytest.mark.unit
    def test_response_event_includes_safety_flag(self, mock_env) -> None:
        """Response event should include has_safety_disclaimer flag."""
        from services.analytics import AnalyticsService

        service = AnalyticsService()

        event = service.create_response_event(
            session_id="session-123",
            message_id="msg-456",
            persona="Default",
            chapter=5,
            query_type="global",
            has_citations=False,
            has_safety_disclaimer=True,
            first_token_ms=180,
            total_ms=2800,
        )

        assert event.has_safety_disclaimer is True
