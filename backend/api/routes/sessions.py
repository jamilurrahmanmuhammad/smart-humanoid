"""Session management API routes.

FR References:
- FR-012: Session context management
- FR-015: Persona support
- FR-027: Message retention (24h TTL)
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from core.database import DBSession, get_async_session
from models.database import ChatMessageModel, ChatSessionModel
from models.schemas import (
    CreateSessionRequest,
    MessageListResponse,
    MessageSummary,
    PersonaType,
    QueryType,
    SessionDetailResponse,
    SessionResponse,
)

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionResponse)
async def create_session(
    request: CreateSessionRequest = CreateSessionRequest(),
    db: DBSession = None,
) -> SessionResponse:
    """Create a new chat session.

    FR Reference: FR-012 (session context), FR-015 (persona support)

    Args:
        request: Session creation parameters.
        db: Database session (injected).

    Returns:
        SessionResponse with new session details.
    """
    session_id = str(uuid4())
    now = datetime.now(timezone.utc)

    # Create session in database
    session_model = ChatSessionModel(
        id=session_id,
        persona=request.persona.value,
        current_chapter=request.current_chapter,
        current_page=request.current_page,
        created_at=now,
        is_active=True,
    )

    if db is not None:
        db.add(session_model)
        await db.commit()
        await db.refresh(session_model)

    return SessionResponse(
        id=session_id,
        persona=request.persona,
        current_chapter=request.current_chapter,
        current_page=request.current_page,
        created_at=now,
        is_active=True,
    )


@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_session(
    session_id: str,
    db: DBSession = None,
) -> SessionDetailResponse:
    """Get session details by ID.

    FR Reference: FR-012 (session context)

    Args:
        session_id: Session UUID.
        db: Database session (injected).

    Returns:
        SessionDetailResponse with session details and message stats.

    Raises:
        HTTPException: 404 if session not found.
    """
    session_model = None
    if db is not None:
        session_model = await db.get(ChatSessionModel, session_id)

    if session_model is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "not_found", "message": f"Session {session_id} not found"},
        )

    # Calculate message statistics
    now = datetime.now(timezone.utc)
    valid_messages = [
        m for m in session_model.messages
        if m.expires_at > now
    ]
    message_count = len(valid_messages)
    last_activity = max(
        (m.created_at for m in valid_messages),
        default=session_model.created_at,
    )

    return SessionDetailResponse(
        id=session_model.id,
        persona=PersonaType(session_model.persona),
        current_chapter=session_model.current_chapter,
        current_page=session_model.current_page,
        created_at=session_model.created_at,
        is_active=session_model.is_active,
        message_count=message_count,
        last_activity=last_activity,
    )


@router.delete("/{session_id}", status_code=204)
async def delete_session(
    session_id: str,
    db: DBSession = None,
) -> Response:
    """Mark session as inactive (soft delete).

    FR Reference: FR-012 (session management)

    Args:
        session_id: Session UUID.
        db: Database session (injected).

    Returns:
        Empty 204 response on success.

    Raises:
        HTTPException: 404 if session not found.
    """
    session_model = None
    if db is not None:
        session_model = await db.get(ChatSessionModel, session_id)

    if session_model is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "not_found", "message": f"Session {session_id} not found"},
        )

    # Mark as inactive (soft delete)
    session_model.is_active = False

    if db is not None:
        await db.commit()

    return Response(status_code=204)


@router.get("/{session_id}/messages", response_model=MessageListResponse)
async def get_session_messages(
    session_id: str,
    db: DBSession = None,
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str | None = Query(default=None),
) -> MessageListResponse:
    """Get messages for a session with pagination.

    FR Reference: FR-027 (only returns non-expired messages)

    Args:
        session_id: Session UUID.
        db: Database session (injected).
        limit: Maximum messages to return (default 20, max 100).
        cursor: Pagination cursor for next page.

    Returns:
        MessageListResponse with paginated messages.

    Raises:
        HTTPException: 404 if session not found.
    """
    session_model = None
    if db is not None:
        session_model = await db.get(ChatSessionModel, session_id)

    if session_model is None:
        raise HTTPException(
            status_code=404,
            detail={"error": "not_found", "message": f"Session {session_id} not found"},
        )

    # Filter out expired messages (FR-027)
    now = datetime.now(timezone.utc)
    valid_messages = [
        m for m in session_model.messages
        if m.expires_at > now
    ]

    # Sort by created_at
    valid_messages.sort(key=lambda m: m.created_at)

    # Apply pagination
    if cursor:
        # cursor is the message ID to start after
        cursor_idx = next(
            (i for i, m in enumerate(valid_messages) if m.id == cursor),
            -1,
        )
        if cursor_idx >= 0:
            valid_messages = valid_messages[cursor_idx + 1:]

    has_more = len(valid_messages) > limit
    paginated_messages = valid_messages[:limit]

    next_cursor = None
    if has_more and paginated_messages:
        next_cursor = paginated_messages[-1].id

    # Convert to response schema
    message_summaries = [
        MessageSummary(
            id=m.id,
            role=m.role,
            content=m.content,
            created_at=m.created_at,
            query_type=QueryType(m.query_type),
            citations=None,  # TODO: Load citations if needed
            has_safety_disclaimer=m.has_safety_disclaimer,
        )
        for m in paginated_messages
    ]

    return MessageListResponse(
        messages=message_summaries,
        has_more=has_more,
        next_cursor=next_cursor,
    )
