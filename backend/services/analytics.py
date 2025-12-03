"""Analytics service for instructor insights.

Provides analytics event creation and tracking without PII.
FR References: FR-025 (analytics storage), FR-026 (no PII), NFR-001 (latency tracking)
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4


class EventType(str, Enum):
    """Analytics event types."""

    QUERY_RECEIVED = "query_received"
    RESPONSE_SENT = "response_sent"


@dataclass
class AnalyticsEvent:
    """Analytics event data structure.

    Stores aggregate metrics without PII per FR-026.
    """

    event_type: str
    session_id: str
    message_id: str
    persona: str
    chapter: Optional[int]
    query_type: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # Response-specific fields
    has_citations: Optional[bool] = None
    has_safety_disclaimer: Optional[bool] = None
    first_token_ms: Optional[int] = None
    total_ms: Optional[int] = None

    # TTL for cleanup (24 hours per FR-027)
    expires_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=24)
    )

    def to_dict(self) -> dict:
        """Convert event to dictionary for storage/transmission.

        Returns:
            Dictionary with event data.
        """
        result = asdict(self)
        # Convert datetime to ISO format strings
        result["timestamp"] = self.timestamp.isoformat()
        result["expires_at"] = self.expires_at.isoformat()
        return result


class AnalyticsService:
    """Service for creating and managing analytics events.

    Tracks query and response metrics for instructor insights
    without storing PII.

    FR References:
    - FR-025: Analytics event storage
    - FR-026: No PII in analytics
    - NFR-001: Latency tracking for <5s first token
    """

    def create_event(
        self,
        event_type: str,
        session_id: str,
        message_id: str,
        persona: str,
        chapter: Optional[int],
        query_type: str,
    ) -> AnalyticsEvent:
        """Create a basic analytics event.

        Args:
            event_type: Type of event (query_received, response_sent).
            session_id: Session identifier.
            message_id: Message identifier.
            persona: User persona.
            chapter: Current chapter (if applicable).
            query_type: Query scope type.

        Returns:
            AnalyticsEvent with populated fields.
        """
        return AnalyticsEvent(
            event_type=event_type,
            session_id=session_id,
            message_id=message_id,
            persona=persona,
            chapter=chapter,
            query_type=query_type,
        )

    def create_response_event(
        self,
        session_id: str,
        message_id: str,
        persona: str,
        chapter: Optional[int],
        query_type: str,
        has_citations: bool,
        has_safety_disclaimer: bool,
        first_token_ms: int,
        total_ms: int,
    ) -> AnalyticsEvent:
        """Create a response analytics event with latency metrics.

        Args:
            session_id: Session identifier.
            message_id: Message identifier.
            persona: User persona.
            chapter: Current chapter (if applicable).
            query_type: Query scope type.
            has_citations: Whether response includes citations.
            has_safety_disclaimer: Whether response includes safety disclaimer.
            first_token_ms: Time to first token in milliseconds.
            total_ms: Total response time in milliseconds.

        Returns:
            AnalyticsEvent with response metrics.

        FR Reference: NFR-001 (latency tracking)
        """
        return AnalyticsEvent(
            event_type=EventType.RESPONSE_SENT,
            session_id=session_id,
            message_id=message_id,
            persona=persona,
            chapter=chapter,
            query_type=query_type,
            has_citations=has_citations,
            has_safety_disclaimer=has_safety_disclaimer,
            first_token_ms=first_token_ms,
            total_ms=total_ms,
        )
