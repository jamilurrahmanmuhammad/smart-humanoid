# Data Model: RAG Chatbot Assistant

**Feature**: 008-rag-chatbot-assistant
**Date**: 2025-12-02
**Status**: Draft

---

## Overview

This document defines the data entities, relationships, and validation rules for the RAG Chatbot Assistant feature. Models are defined using Pydantic for API layer and SQLAlchemy for persistence.

---

## Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐
│   ChatSession   │───1:N─│   ChatMessage   │
└─────────────────┘       └─────────────────┘
        │                         │
        │                         │ 1:N
        │                         ▼
        │                 ┌─────────────────┐
        │                 │    Citation     │
        │                 └─────────────────┘
        │
        │ (references)
        ▼
┌─────────────────┐
│  ContentChunk   │ (Qdrant - Vector Store)
└─────────────────┘
        │
        │ (indexed from)
        ▼
┌─────────────────┐
│  BookContent    │ (Source MDX files)
└─────────────────┘
```

---

## 1. ChatSession

Represents a conversation between a learner and the chatbot. Sessions are ephemeral during active use.

### Pydantic Model (API Layer)

```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

class PersonaType(str, Enum):
    """Learner persona types per Constitution Section XIII"""
    EXPLORER = "Explorer"
    BUILDER = "Builder"
    ENGINEER = "Engineer"
    DEFAULT = "Default"  # No persona selected

class ChatSession(BaseModel):
    """Chat session for API responses"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True
    )

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique session identifier (UUID)"
    )
    persona: PersonaType = Field(
        default=PersonaType.DEFAULT,
        description="Learner persona for response adaptation"
    )
    current_chapter: Optional[int] = Field(
        default=None,
        ge=1,
        le=20,
        description="Current chapter context (1-indexed)"
    )
    current_page: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Current page path for context"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Session creation timestamp"
    )
    is_active: bool = Field(
        default=True,
        description="Whether session is currently active"
    )
```

### SQLAlchemy Model (Persistence Layer)

```python
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class ChatSessionModel(Base):
    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True)
    persona = Column(
        Enum("Explorer", "Builder", "Engineer", "Default", name="persona_type"),
        default="Default",
        nullable=False
    )
    current_chapter = Column(Integer, nullable=True)
    current_page = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    messages = relationship("ChatMessageModel", back_populates="session", cascade="all, delete-orphan")
```

### Validation Rules

| Field | Rule | FR Reference |
|-------|------|--------------|
| id | UUID v4 format | - |
| persona | Must be valid PersonaType | FR-015 |
| current_chapter | 1-20 if provided | FR-012 |

---

## 2. ChatMessage

Individual message within a session. Each message has independent retention tracking per FR-027a.

### Pydantic Model (API Layer)

```python
class QueryType(str, Enum):
    """Query scope types"""
    GLOBAL = "global"           # Search entire book
    PAGE_SCOPED = "page"        # Prioritize current chapter
    SELECTION_SCOPED = "selection"  # Only use selected text

class MessageRole(str, Enum):
    """Message author role"""
    USER = "user"
    ASSISTANT = "assistant"

class ChatMessage(BaseModel):
    """Individual chat message"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True
    )

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique message identifier"
    )
    session_id: str = Field(
        description="Parent session ID"
    )
    role: MessageRole = Field(
        description="Message author (user or assistant)"
    )
    content: str = Field(
        min_length=1,
        max_length=10000,
        description="Message content"
    )
    query_type: QueryType = Field(
        default=QueryType.GLOBAL,
        description="Query scope for this message"
    )
    selected_text: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="User-selected text for selection-scoped queries"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Message creation timestamp"
    )
    expires_at: datetime = Field(
        description="Expiration timestamp (24h post-session per FR-027)"
    )
    citations: list["Citation"] = Field(
        default_factory=list,
        max_length=5,
        description="Source citations (max 5 per FR-009)"
    )
    has_safety_disclaimer: bool = Field(
        default=False,
        description="Whether response includes safety warning"
    )

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at
```

### SQLAlchemy Model (Persistence Layer)

```python
class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True)
    session_id = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(Enum("user", "assistant", name="message_role"), nullable=False)
    content = Column(Text, nullable=False)
    query_type = Column(
        Enum("global", "page", "selection", name="query_type"),
        default="global",
        nullable=False
    )
    selected_text = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    has_safety_disclaimer = Column(Boolean, default=False, nullable=False)

    # Relationships
    session = relationship("ChatSessionModel", back_populates="messages")
    citations = relationship("CitationModel", back_populates="message", cascade="all, delete-orphan")

    # Index for expiration cleanup
    __table_args__ = (
        Index("idx_expires_at", "expires_at"),
    )
```

### Validation Rules

| Field | Rule | FR Reference |
|-------|------|--------------|
| content | 1-10,000 characters | - |
| selected_text | Max 2,000 characters | Edge case |
| citations | Max 5 items | FR-009 |
| expires_at | created_at + 24h | FR-027 |

---

## 3. Citation

Reference to source content for answer grounding per Constitution Section XVIII.

### Pydantic Model (API Layer)

```python
class Citation(BaseModel):
    """Source citation for grounded responses"""
    model_config = ConfigDict(str_strip_whitespace=True)

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Citation identifier"
    )
    message_id: str = Field(
        description="Parent message ID"
    )
    chapter: int = Field(
        ge=1,
        le=20,
        description="Source chapter number"
    )
    section: str = Field(
        max_length=100,
        description="Section identifier (e.g., '2.3.1')"
    )
    heading: str = Field(
        max_length=200,
        description="Section heading text"
    )
    quote: str = Field(
        max_length=500,
        description="Verbatim quote extract"
    )
    link: str = Field(
        max_length=500,
        description="Deep link to source location"
    )
    relevance_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Semantic similarity score"
    )
```

### SQLAlchemy Model (Persistence Layer)

```python
class CitationModel(Base):
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
```

### Validation Rules

| Field | Rule | FR Reference |
|-------|------|--------------|
| quote | Verbatim, max 500 chars | FR-005, Section XIX |
| link | Must resolve to book location | FR-010 |

---

## 4. ContentChunk (Qdrant Vector Store)

Indexed portion of book content for RAG retrieval. Stored in Qdrant, not PostgreSQL.

### Qdrant Payload Schema

```python
class ContentChunkPayload(BaseModel):
    """Metadata stored with each vector in Qdrant"""

    # Location identifiers
    module_id: int = Field(ge=1, le=4, description="Module number (1-4)")
    chapter_id: int = Field(ge=1, le=20, description="Chapter number")
    section_id: str = Field(max_length=20, description="Section ID (e.g., '2.3.1')")

    # Content metadata
    heading: str = Field(max_length=200, description="Section heading")
    text: str = Field(description="Chunk text content")
    persona: PersonaType = Field(description="Content variant persona")

    # Navigation
    path: str = Field(max_length=500, description="Docusaurus route path")
    chunk_index: int = Field(ge=0, description="Chunk position within section")

    # Future expansion
    language: str = Field(default="en", max_length=5, description="Content language")
```

### Qdrant Collection Configuration

```python
from qdrant_client.models import Distance, VectorParams

COLLECTION_CONFIG = {
    "collection_name": "textbook_chunks",
    "vectors_config": VectorParams(
        size=1536,  # text-embedding-3-small dimensions
        distance=Distance.COSINE
    )
}

# Payload indexes for filtered search
PAYLOAD_INDEXES = [
    {"field_name": "module_id", "field_schema": "integer"},
    {"field_name": "chapter_id", "field_schema": "integer"},
    {"field_name": "persona", "field_schema": "keyword"},
    {"field_name": "language", "field_schema": "keyword"},
]
```

---

## 5. AnalyticsEvent

Anonymized interaction metadata for instructor insights per FR-025, FR-026.

### Pydantic Model

```python
class AnalyticsEvent(BaseModel):
    """Anonymized analytics event - no PII"""
    model_config = ConfigDict(use_enum_values=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message_id: str = Field(description="Reference to message (for dedup)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    persona: PersonaType = Field(description="Learner persona")
    chapter: Optional[int] = Field(default=None, description="Chapter context")
    query_type: QueryType = Field(description="Query scope")
    has_citations: bool = Field(description="Whether response included citations")
    has_safety_disclaimer: bool = Field(description="Whether safety warning included")
    response_latency_ms: int = Field(ge=0, description="Time to first token (ms)")
    expires_at: datetime = Field(description="24h retention per FR-027a")
```

### SQLAlchemy Model

```python
class AnalyticsEventModel(Base):
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

    __table_args__ = (
        Index("idx_analytics_expires_at", "expires_at"),
        Index("idx_analytics_timestamp", "timestamp"),
    )
```

---

## 6. Request/Response Models

### Chat Request

```python
class ChatRequest(BaseModel):
    """Incoming chat request"""
    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(
        min_length=1,
        max_length=2000,
        description="User's question"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Existing session ID (creates new if not provided)"
    )
    persona: PersonaType = Field(
        default=PersonaType.DEFAULT,
        description="Learner persona"
    )
    query_type: QueryType = Field(
        default=QueryType.GLOBAL,
        description="Query scope"
    )
    current_chapter: Optional[int] = Field(
        default=None,
        ge=1,
        le=20,
        description="Current chapter for page-scoped queries"
    )
    selected_text: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Selected text for selection-scoped queries"
    )
```

### Chat Response

```python
class ChatResponse(BaseModel):
    """Chat response with citations"""

    session_id: str = Field(description="Session identifier")
    message_id: str = Field(description="Response message ID")
    content: str = Field(description="Assistant response")
    citations: list[Citation] = Field(
        default_factory=list,
        description="Source citations"
    )
    has_safety_disclaimer: bool = Field(
        default=False,
        description="Whether safety warning included"
    )
    query_type: QueryType = Field(description="Query scope used")
    is_selection_scoped: bool = Field(
        default=False,
        description="Whether answer based on selection only"
    )
```

### Stream Chunk

```python
class StreamChunk(BaseModel):
    """Streaming response chunk"""

    type: str = Field(description="Chunk type: 'content' | 'citation' | 'done'")
    content: Optional[str] = Field(default=None, description="Text chunk")
    citation: Optional[Citation] = Field(default=None, description="Citation data")
    session_id: Optional[str] = Field(default=None, description="Session ID (on done)")
    message_id: Optional[str] = Field(default=None, description="Message ID (on done)")
```

---

## Database Migrations

### Initial Migration (001_initial_schema.py)

```python
"""Initial schema for RAG Chatbot Assistant

Revision ID: 001
Create Date: 2025-12-02
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Chat sessions table
    op.create_table(
        'chat_sessions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('persona', sa.Enum('Explorer', 'Builder', 'Engineer', 'Default', name='persona_type'), nullable=False),
        sa.Column('current_chapter', sa.Integer, nullable=True),
        sa.Column('current_page', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False)
    )

    # Chat messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('session_id', sa.String(36), sa.ForeignKey('chat_sessions.id'), nullable=False),
        sa.Column('role', sa.Enum('user', 'assistant', name='message_role'), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('query_type', sa.Enum('global', 'page', 'selection', name='query_type'), nullable=False),
        sa.Column('selected_text', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('expires_at', sa.DateTime, nullable=False),
        sa.Column('has_safety_disclaimer', sa.Boolean, default=False, nullable=False)
    )
    op.create_index('idx_messages_expires_at', 'chat_messages', ['expires_at'])

    # Citations table
    op.create_table(
        'citations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('message_id', sa.String(36), sa.ForeignKey('chat_messages.id'), nullable=False),
        sa.Column('chapter', sa.Integer, nullable=False),
        sa.Column('section', sa.String(100), nullable=False),
        sa.Column('heading', sa.String(200), nullable=False),
        sa.Column('quote', sa.String(500), nullable=False),
        sa.Column('link', sa.String(500), nullable=False),
        sa.Column('relevance_score', sa.Float, nullable=False)
    )

    # Analytics events table
    op.create_table(
        'analytics_events',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('message_id', sa.String(36), nullable=False, unique=True),
        sa.Column('timestamp', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('persona', sa.String(20), nullable=False),
        sa.Column('chapter', sa.Integer, nullable=True),
        sa.Column('query_type', sa.String(20), nullable=False),
        sa.Column('has_citations', sa.Boolean, nullable=False),
        sa.Column('has_safety_disclaimer', sa.Boolean, nullable=False),
        sa.Column('response_latency_ms', sa.Integer, nullable=False),
        sa.Column('expires_at', sa.DateTime, nullable=False)
    )
    op.create_index('idx_analytics_expires_at', 'analytics_events', ['expires_at'])
    op.create_index('idx_analytics_timestamp', 'analytics_events', ['timestamp'])

def downgrade():
    op.drop_table('analytics_events')
    op.drop_table('citations')
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
```

---

## State Transitions

### Message Lifecycle

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Created  │────▶│  Active  │────▶│ Expired  │────▶│  Purged  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
     │                │                │                │
     │                │                │                │
     ▼                ▼                ▼                ▼
  timestamp       in session      expires_at <      deleted by
  = now()         or < 24h        now()             background
                                                    job
```

### Session Lifecycle

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Created  │────▶│  Active  │────▶│ Inactive │
└──────────┘     └──────────┘     └──────────┘
     │                │                │
     │                │                │
     ▼                ▼                ▼
  is_active       messages          is_active
  = true          being added       = false
                                    (no new messages)
```

---

## FR Traceability

| Entity | Fields | FR Reference |
|--------|--------|--------------|
| ChatSession | persona | FR-015 |
| ChatSession | current_chapter, current_page | FR-012 |
| ChatMessage | expires_at | FR-027, FR-027a |
| ChatMessage | citations (max 5) | FR-009 |
| ChatMessage | query_type | FR-003 |
| ChatMessage | selected_text | FR-018, FR-020 |
| ChatMessage | has_safety_disclaimer | FR-021 |
| Citation | quote (verbatim) | FR-005 |
| Citation | link | FR-010 |
| AnalyticsEvent | no PII fields | FR-026 |
| ContentChunk | persona | FR-016 |
