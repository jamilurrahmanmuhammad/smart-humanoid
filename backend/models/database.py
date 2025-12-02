"""SQLAlchemy ORM models for persistence layer.

Models defined per data-model.md specification.
Follows Constitution Section X-XI (Technology Platform) requirements.
"""

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """SQLAlchemy declarative base class."""

    pass


# Python Enums for type safety
class PersonaType(str, PyEnum):
    """Learner persona types per Constitution Section XIII."""

    EXPLORER = "Explorer"
    BUILDER = "Builder"
    ENGINEER = "Engineer"
    DEFAULT = "Default"


class MessageRole(str, PyEnum):
    """Message author role."""

    USER = "user"
    ASSISTANT = "assistant"


class QueryType(str, PyEnum):
    """Query scope types."""

    GLOBAL = "global"
    PAGE = "page"
    SELECTION = "selection"


class ChatSessionModel(Base):
    """Chat session ORM model.

    Represents a conversation between a learner and the chatbot.
    FR: FR-012 (session context)
    """

    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True)
    persona = Column(
        Enum(
            "Explorer",
            "Builder",
            "Engineer",
            "Default",
            name="persona_type",
            create_constraint=True,
        ),
        default="Default",
        nullable=False,
    )
    current_chapter = Column(Integer, nullable=True)
    current_page = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    messages = relationship(
        "ChatMessageModel", back_populates="session", cascade="all, delete-orphan"
    )


class ChatMessageModel(Base):
    """Chat message ORM model.

    Individual message within a session with independent retention.
    FR: FR-027 (message retention)
    """

    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True)
    session_id = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(
        Enum("user", "assistant", name="message_role", create_constraint=True),
        nullable=False,
    )
    content = Column(Text, nullable=False)
    query_type = Column(
        Enum("global", "page", "selection", name="query_type", create_constraint=True),
        default="global",
        nullable=False,
    )
    selected_text = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    has_safety_disclaimer = Column(Boolean, default=False, nullable=False)

    # Relationships
    session = relationship("ChatSessionModel", back_populates="messages")
    citations = relationship(
        "CitationModel", back_populates="message", cascade="all, delete-orphan"
    )

    # Indexes
    __table_args__ = (Index("idx_messages_expires_at", "expires_at"),)


class CitationModel(Base):
    """Citation ORM model.

    Reference to source content for answer grounding.
    FR: FR-004 (citations), FR-005 (verbatim quotes), FR-010 (links)
    Constitution Section XVIII (Answer Grounding)
    """

    __tablename__ = "citations"

    id = Column(String(36), primary_key=True)
    message_id = Column(String(36), ForeignKey("chat_messages.id"), nullable=False)
    chapter = Column(Integer, nullable=False)
    section = Column(String(100), nullable=False)
    heading = Column(String(200), nullable=False)
    quote = Column(String(500), nullable=False)
    link = Column(String(500), nullable=False)
    relevance_score = Column(Float, nullable=False)

    # Relationships
    message = relationship("ChatMessageModel", back_populates="citations")


class AnalyticsEventModel(Base):
    """Analytics event ORM model.

    Anonymized interaction metadata - NO PII per FR-026.
    FR: FR-025 (analytics storage), FR-026 (no PII)
    """

    __tablename__ = "analytics_events"

    id = Column(String(36), primary_key=True)
    message_id = Column(String(36), nullable=False, unique=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    persona = Column(String(20), nullable=False)
    chapter = Column(Integer, nullable=True)
    query_type = Column(String(20), nullable=False)
    has_citations = Column(Boolean, nullable=False)
    has_safety_disclaimer = Column(Boolean, nullable=False)
    response_latency_ms = Column(Integer, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Indexes for cleanup and querying
    __table_args__ = (
        Index("idx_analytics_expires_at", "expires_at"),
        Index("idx_analytics_timestamp", "timestamp"),
    )
