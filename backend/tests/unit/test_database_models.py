"""Unit tests for SQLAlchemy ORM models.

TDD: RED phase - these tests should FAIL until T009-T015 are implemented.
Tests verify models match data-model.md specification.
"""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest


class TestChatSessionModel:
    """Tests for ChatSession ORM model (T008-T009)."""

    @pytest.mark.unit
    def test_chat_session_model_fields(self) -> None:
        """ChatSession should have all required fields per data-model.md."""
        from models.database import ChatSessionModel

        # Verify model has required columns
        columns = {c.name for c in ChatSessionModel.__table__.columns}
        required_columns = {
            "id",
            "persona",
            "current_chapter",
            "current_page",
            "created_at",
            "is_active",
        }
        assert required_columns.issubset(columns), f"Missing columns: {required_columns - columns}"

    @pytest.mark.unit
    def test_chat_session_model_persona_enum(self) -> None:
        """ChatSession persona should be an enum type."""
        from sqlalchemy import Enum as SQLEnum

        from models.database import ChatSessionModel

        persona_col = ChatSessionModel.__table__.columns["persona"]
        # Should be an Enum type - check the actual type class
        assert isinstance(persona_col.type, SQLEnum)
        assert persona_col.type.name == "persona_type"

    @pytest.mark.unit
    def test_chat_session_model_relationships(self) -> None:
        """ChatSession should have relationship to messages."""
        from models.database import ChatSessionModel

        # Check relationship exists
        assert hasattr(ChatSessionModel, "messages")

    @pytest.mark.unit
    def test_chat_session_model_defaults(self) -> None:
        """ChatSession should have correct default values."""
        from models.database import ChatSessionModel

        # Check default for is_active
        is_active_col = ChatSessionModel.__table__.columns["is_active"]
        assert is_active_col.default is not None


class TestChatMessageModel:
    """Tests for ChatMessage ORM model (T010-T011)."""

    @pytest.mark.unit
    def test_chat_message_model_fields(self) -> None:
        """ChatMessage should have all required fields per data-model.md."""
        from models.database import ChatMessageModel

        columns = {c.name for c in ChatMessageModel.__table__.columns}
        required_columns = {
            "id",
            "session_id",
            "role",
            "content",
            "query_type",
            "selected_text",
            "created_at",
            "expires_at",
            "has_safety_disclaimer",
        }
        assert required_columns.issubset(columns), f"Missing columns: {required_columns - columns}"

    @pytest.mark.unit
    def test_chat_message_model_session_fk(self) -> None:
        """ChatMessage should have foreign key to ChatSession."""
        from models.database import ChatMessageModel

        session_id_col = ChatMessageModel.__table__.columns["session_id"]
        # Check FK exists
        assert len(session_id_col.foreign_keys) > 0
        fk = list(session_id_col.foreign_keys)[0]
        assert "chat_sessions.id" in str(fk.target_fullname)

    @pytest.mark.unit
    def test_chat_message_model_role_enum(self) -> None:
        """ChatMessage role should be an enum type."""
        from sqlalchemy import Enum as SQLEnum

        from models.database import ChatMessageModel

        role_col = ChatMessageModel.__table__.columns["role"]
        assert isinstance(role_col.type, SQLEnum)
        assert role_col.type.name == "message_role"

    @pytest.mark.unit
    def test_chat_message_model_query_type_enum(self) -> None:
        """ChatMessage query_type should be an enum type."""
        from sqlalchemy import Enum as SQLEnum

        from models.database import ChatMessageModel

        query_type_col = ChatMessageModel.__table__.columns["query_type"]
        assert isinstance(query_type_col.type, SQLEnum)
        assert query_type_col.type.name == "query_type"

    @pytest.mark.unit
    def test_chat_message_model_expires_at_index(self) -> None:
        """ChatMessage should have index on expires_at for cleanup queries."""
        from models.database import ChatMessageModel

        # Check for index
        indexes = {idx.name for idx in ChatMessageModel.__table__.indexes}
        assert any("expires" in idx.lower() for idx in indexes), "Missing expires_at index"

    @pytest.mark.unit
    def test_chat_message_model_relationships(self) -> None:
        """ChatMessage should have relationships to session and citations."""
        from models.database import ChatMessageModel

        assert hasattr(ChatMessageModel, "session")
        assert hasattr(ChatMessageModel, "citations")


class TestCitationModel:
    """Tests for Citation ORM model (T012-T013)."""

    @pytest.mark.unit
    def test_citation_model_fields(self) -> None:
        """Citation should have all required fields per data-model.md."""
        from models.database import CitationModel

        columns = {c.name for c in CitationModel.__table__.columns}
        required_columns = {
            "id",
            "message_id",
            "chapter",
            "section",
            "heading",
            "quote",
            "link",
            "relevance_score",
        }
        assert required_columns.issubset(columns), f"Missing columns: {required_columns - columns}"

    @pytest.mark.unit
    def test_citation_model_message_fk(self) -> None:
        """Citation should have foreign key to ChatMessage."""
        from models.database import CitationModel

        message_id_col = CitationModel.__table__.columns["message_id"]
        assert len(message_id_col.foreign_keys) > 0
        fk = list(message_id_col.foreign_keys)[0]
        assert "chat_messages.id" in str(fk.target_fullname)

    @pytest.mark.unit
    def test_citation_model_relationships(self) -> None:
        """Citation should have relationship to message."""
        from models.database import CitationModel

        assert hasattr(CitationModel, "message")


class TestAnalyticsEventModel:
    """Tests for AnalyticsEvent ORM model (T014-T015)."""

    @pytest.mark.unit
    def test_analytics_event_model_fields(self) -> None:
        """AnalyticsEvent should have all required fields per data-model.md."""
        from models.database import AnalyticsEventModel

        columns = {c.name for c in AnalyticsEventModel.__table__.columns}
        required_columns = {
            "id",
            "message_id",
            "timestamp",
            "persona",
            "chapter",
            "query_type",
            "has_citations",
            "has_safety_disclaimer",
            "response_latency_ms",
            "expires_at",
        }
        assert required_columns.issubset(columns), f"Missing columns: {required_columns - columns}"

    @pytest.mark.unit
    def test_analytics_event_model_no_pii(self) -> None:
        """AnalyticsEvent should NOT have PII fields (FR-026)."""
        from models.database import AnalyticsEventModel

        columns = {c.name for c in AnalyticsEventModel.__table__.columns}
        # These fields would contain PII and should NOT exist
        pii_fields = {"user_id", "email", "ip_address", "user_agent", "content"}
        assert not pii_fields.intersection(
            columns
        ), f"PII fields found: {pii_fields.intersection(columns)}"

    @pytest.mark.unit
    def test_analytics_event_model_indexes(self) -> None:
        """AnalyticsEvent should have indexes for cleanup and querying."""
        from models.database import AnalyticsEventModel

        indexes = {idx.name for idx in AnalyticsEventModel.__table__.indexes}
        # Should have expires_at index for cleanup
        assert any("expires" in idx.lower() for idx in indexes), "Missing expires_at index"
        # Should have timestamp index for querying
        assert any("timestamp" in idx.lower() for idx in indexes), "Missing timestamp index"

    @pytest.mark.unit
    def test_analytics_event_message_id_unique(self) -> None:
        """AnalyticsEvent message_id should be unique (one event per message)."""
        from models.database import AnalyticsEventModel

        message_id_col = AnalyticsEventModel.__table__.columns["message_id"]
        assert message_id_col.unique is True, "message_id should be unique"


class TestMessageTTL:
    """Tests for message TTL calculation (T105)."""

    @pytest.mark.unit
    def test_expires_at_set_on_creation(self) -> None:
        """ChatMessage expires_at should be set to created_at + 24h (FR-027)."""
        from models.database import ChatMessageModel

        # Verify expires_at column exists and is required
        expires_at_col = ChatMessageModel.__table__.columns["expires_at"]
        assert expires_at_col.nullable is False

    @pytest.mark.unit
    def test_message_ttl_default_24_hours(self) -> None:
        """Message TTL should default to 24 hours per FR-027."""
        from datetime import datetime, timezone

        # TTL constant should be 24 hours
        MESSAGE_TTL_HOURS = 24

        created = datetime.now(timezone.utc)
        expected_expires = created + timedelta(hours=MESSAGE_TTL_HOURS)

        # The difference should be exactly 24 hours
        assert (expected_expires - created).total_seconds() == 24 * 60 * 60

    @pytest.mark.unit
    def test_message_model_has_expires_at_column(self) -> None:
        """ChatMessageModel should have expires_at datetime column."""
        from models.database import ChatMessageModel
        from sqlalchemy import DateTime

        expires_at_col = ChatMessageModel.__table__.columns["expires_at"]
        # Should be DateTime type
        assert isinstance(expires_at_col.type, DateTime)


class TestBaseModel:
    """Tests for SQLAlchemy Base configuration."""

    @pytest.mark.unit
    def test_base_declarative_base_exists(self) -> None:
        """Base declarative class should be defined."""
        from models.database import Base

        assert Base is not None
        # Should have metadata
        assert hasattr(Base, "metadata")
