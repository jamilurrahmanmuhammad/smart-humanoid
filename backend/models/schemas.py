"""Pydantic request/response models for API layer.

Models defined per contracts/openapi.yaml specification.
Follows Constitution Section X-XI (Technology Platform) requirements.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


# =============================================================================
# Enums
# =============================================================================


class PersonaType(str, Enum):
    """Learner persona types per Constitution Section XIII.

    - Explorer: Software background, simulation-focused
    - Builder: Arduino/Raspberry Pi experience, maker context
    - Engineer: Industrial robotics, full technical depth
    - Default: Balanced style, no specialized background assumed
    """

    EXPLORER = "Explorer"
    BUILDER = "Builder"
    ENGINEER = "Engineer"
    DEFAULT = "Default"


class QueryType(str, Enum):
    """Query scope types.

    - global: Search entire book (FR-003)
    - page: Prioritize current chapter (FR-003)
    - selection: Only use selected text (FR-018)
    """

    GLOBAL = "global"
    PAGE = "page"
    SELECTION = "selection"


class MessageRole(str, Enum):
    """Message author role."""

    USER = "user"
    ASSISTANT = "assistant"


# =============================================================================
# Citation Schema
# =============================================================================


class Citation(BaseModel):
    """Source citation for grounded responses.

    FR References: FR-004 (citations), FR-005 (verbatim quotes), FR-010 (links)
    Constitution Section XVIII (Answer Grounding)
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    chapter: int = Field(ge=1, le=20, description="Source chapter number")
    section: str = Field(max_length=100, description="Section identifier (e.g., '2.3.1')")
    heading: str = Field(max_length=200, description="Section heading")
    quote: str = Field(max_length=500, description="Verbatim quote extract (FR-005)")
    link: str = Field(max_length=500, description="Deep link to source location (FR-010)")
    relevance_score: float = Field(
        ge=0.0, le=1.0, description="Semantic similarity score"
    )


# =============================================================================
# Chat Request/Response Schemas
# =============================================================================


class ChatRequest(BaseModel):
    """Incoming chat request.

    FR References: FR-003 (query types), FR-018 (selection-scoped)
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(
        min_length=1, max_length=2000, description="User's question"
    )
    session_id: Optional[str] = Field(
        default=None, description="Existing session ID (creates new if not provided)"
    )
    persona: PersonaType = Field(
        default=PersonaType.DEFAULT, description="Learner persona"
    )
    query_type: QueryType = Field(
        default=QueryType.GLOBAL, description="Query scope"
    )
    current_chapter: Optional[int] = Field(
        default=None,
        ge=1,
        le=20,
        description="Current chapter for page-scoped queries",
    )
    selected_text: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Selected text for selection-scoped queries",
    )


class ChatResponse(BaseModel):
    """Chat response with citations.

    FR References: FR-009 (max 5 citations), FR-019 (selection indicator),
                   FR-021 (safety disclaimer)
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    session_id: str = Field(description="Session identifier")
    message_id: str = Field(description="Response message ID")
    content: str = Field(description="Assistant response")
    citations: list[Citation] = Field(
        default_factory=list,
        max_length=5,
        description="Source citations (max 5 per FR-009)",
    )
    has_safety_disclaimer: bool = Field(
        default=False, description="Whether response includes safety warning (FR-021)"
    )
    query_type: QueryType = Field(description="Query scope used")
    is_selection_scoped: bool = Field(
        default=False,
        description="Indicates answer based on selection only (FR-019)",
    )

    @field_validator("citations", mode="before")
    @classmethod
    def validate_max_citations(cls, v: list) -> list:
        """Ensure citations don't exceed max of 5."""
        if len(v) > 5:
            raise ValueError("citations list cannot exceed 5 items (FR-009)")
        return v


# =============================================================================
# Streaming Schema
# =============================================================================


class StreamChunk(BaseModel):
    """Streaming response chunk for WebSocket/SSE.

    Chunk types:
    - content: Text content chunk
    - citation: Citation data
    - done: Final chunk with session/message IDs
    - error: Error information

    FR Reference: NFR-001 (streaming for <5s first token)
    """

    # NOTE: Do NOT use str_strip_whitespace=True here!
    # Content chunks from OpenAI have leading spaces that must be preserved
    # for proper text formatting (e.g., ' Robot' -> 'Robot' would break output)
    model_config = ConfigDict()

    type: str = Field(description="Chunk type: content | citation | done | error")
    content: Optional[str] = Field(default=None, description="Text chunk")
    citation: Optional[Citation] = Field(default=None, description="Citation data")
    session_id: Optional[str] = Field(
        default=None, description="Session ID (on done)"
    )
    message_id: Optional[str] = Field(
        default=None, description="Message ID (on done)"
    )
    error: Optional[str] = Field(default=None, description="Error type (on error)")
    message: Optional[str] = Field(
        default=None, description="Error message (on error)"
    )


# =============================================================================
# Session Schemas
# =============================================================================


class CreateSessionRequest(BaseModel):
    """Request to create a new chat session.

    FR Reference: FR-012 (session context), FR-015 (persona)
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    persona: PersonaType = Field(
        default=PersonaType.DEFAULT, description="Learner persona"
    )
    current_chapter: Optional[int] = Field(
        default=None, ge=1, le=20, description="Current chapter context"
    )
    current_page: Optional[str] = Field(
        default=None, max_length=255, description="Current page path"
    )


class SessionResponse(BaseModel):
    """Session information response.

    FR Reference: FR-012 (session context)
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    id: str = Field(description="Session UUID")
    persona: PersonaType = Field(description="Learner persona")
    current_chapter: Optional[int] = Field(default=None, description="Current chapter")
    current_page: Optional[str] = Field(default=None, description="Current page path")
    created_at: datetime = Field(description="Session creation timestamp")
    is_active: bool = Field(description="Whether session is active")


class SessionDetailResponse(SessionResponse):
    """Detailed session response with message statistics.

    Extends SessionResponse with message count and activity tracking.
    """

    message_count: Optional[int] = Field(
        default=None, description="Total messages in session"
    )
    last_activity: Optional[datetime] = Field(
        default=None, description="Timestamp of last message"
    )


# =============================================================================
# Message Schemas
# =============================================================================


class MessageSummary(BaseModel):
    """Summary of a chat message.

    Used in message list responses.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    id: str = Field(description="Message UUID")
    role: str = Field(description="Message role: user | assistant")
    content: str = Field(description="Message content")
    created_at: datetime = Field(description="Message timestamp")
    query_type: QueryType = Field(description="Query scope")
    citations: Optional[list[Citation]] = Field(
        default=None, description="Citations (for assistant messages)"
    )
    has_safety_disclaimer: Optional[bool] = Field(
        default=None, description="Safety disclaimer flag"
    )


class MessageListResponse(BaseModel):
    """Paginated list of messages.

    FR Reference: FR-027 (only returns non-expired messages)
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    messages: list[MessageSummary] = Field(description="Message list")
    has_more: bool = Field(description="More messages available")
    next_cursor: Optional[str] = Field(
        default=None, description="Cursor for next page"
    )


# =============================================================================
# Error Schema
# =============================================================================


class ErrorResponse(BaseModel):
    """Error response schema.

    FR Reference: FR-028 (error handling)
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    error: str = Field(description="Error type")
    message: str = Field(description="Human-readable error message")
    code: Optional[str] = Field(
        default=None, description="Error code for client handling"
    )
    details: Optional[dict[str, Any]] = Field(
        default=None, description="Additional error details"
    )


# =============================================================================
# Health Schema
# =============================================================================


class HealthResponse(BaseModel):
    """Service health status response."""

    model_config = ConfigDict(str_strip_whitespace=True)

    status: str = Field(description="Health status: healthy | degraded | unhealthy")
    timestamp: datetime = Field(description="Check timestamp")
    dependencies: Optional[dict[str, str]] = Field(
        default=None, description="Dependency health status"
    )
    version: Optional[str] = Field(default=None, description="Service version")
