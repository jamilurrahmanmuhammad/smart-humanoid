"""Chat API routes - POST /chat, POST /chat/stream, WebSocket /ws/chat."""

import json
import uuid
from typing import AsyncGenerator

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

from models.schemas import (
    ChatRequest,
    ChatResponse,
    Citation,
    PersonaType,
    QueryType,
    StreamChunk,
)
from services.agent import AgentRunner
from services.rag import RAGPipeline
from services.vector_store import SearchFilters

router = APIRouter(prefix="/chat", tags=["chat"])


def _build_search_filters(request: ChatRequest) -> SearchFilters | None:
    """Build search filters from chat request.

    Args:
        request: ChatRequest with optional filters.

    Returns:
        SearchFilters if any filters specified, None otherwise.
    """
    # Only apply persona filter if it's not the default
    # The default persona means "show all personas", not filter for "Default"
    has_persona_filter = (
        request.persona
        and request.persona != PersonaType.DEFAULT
    )

    if request.current_chapter or has_persona_filter:
        return SearchFilters(
            chapter_id=request.current_chapter,
            persona=request.persona.value if has_persona_filter else None,
        )
    return None


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message and return response with citations.

    FR References:
    - FR-001: RAG-based Q&A
    - FR-004: Inline citations
    - FR-012: Session creation

    Args:
        request: ChatRequest with message and optional parameters.

    Returns:
        ChatResponse with content, citations, and session info.
    """
    # Import inside function to avoid module-level import issues
    from services.rag import RAGPipeline as LocalRAGPipeline

    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    message_id = str(uuid.uuid4())

    # Build search filters
    filters = _build_search_filters(request)

    # Run RAG pipeline
    pipeline = LocalRAGPipeline()
    rag_result = await pipeline.query(
        message=request.message,
        filters=filters,
    )

    # If out of scope, return appropriate response
    if rag_result.is_out_of_scope:
        return ChatResponse(
            session_id=session_id,
            message_id=message_id,
            content="I don't have information about this topic in the textbook. "
            "Please ask about ROS 2, robotics, or physical AI topics covered in the course.",
            citations=[],
            query_type=request.query_type,
            is_selection_scoped=request.query_type == QueryType.SELECTION,
        )

    # Run agent with RAG context
    agent = AgentRunner()
    content_parts = []

    async for chunk in agent.run_stream(
        message=request.message,
        rag_context=rag_result.context,
    ):
        if chunk.type == "content" and chunk.content:
            content_parts.append(chunk.content)

    content = "".join(content_parts)

    return ChatResponse(
        session_id=session_id,
        message_id=message_id,
        content=content,
        citations=rag_result.citations,
        query_type=request.query_type,
        is_selection_scoped=request.query_type == QueryType.SELECTION,
    )


async def _generate_sse_stream(
    request: ChatRequest,
) -> AsyncGenerator[str, None]:
    """Generate SSE stream for chat response.

    Args:
        request: ChatRequest with message and parameters.

    Yields:
        SSE formatted event strings.
    """
    # Generate IDs
    session_id = request.session_id or str(uuid.uuid4())
    message_id = str(uuid.uuid4())

    # Send session info first
    session_event = {
        "type": "session",
        "session_id": session_id,
        "message_id": message_id,
    }
    yield f"data: {json.dumps(session_event)}\n\n"

    # Build search filters
    filters = _build_search_filters(request)

    # Run RAG pipeline
    pipeline = RAGPipeline()
    rag_result = await pipeline.query(
        message=request.message,
        filters=filters,
    )

    # Send citations if found
    if rag_result.citations:
        for citation in rag_result.citations:
            citation_event = {
                "type": "citation",
                "citation": {
                    "chapter": citation.chapter,
                    "section": citation.section,
                    "heading": citation.heading,
                    "quote": citation.quote,
                    "link": citation.link,
                    "relevance_score": citation.relevance_score,
                },
            }
            yield f"data: {json.dumps(citation_event)}\n\n"

    # Check for out of scope
    if rag_result.is_out_of_scope:
        content_event = {
            "type": "content",
            "content": "I don't have information about this topic in the textbook.",
        }
        yield f"data: {json.dumps(content_event)}\n\n"
    else:
        # Stream agent response
        agent = AgentRunner()
        async for chunk in agent.run_stream(
            message=request.message,
            rag_context=rag_result.context,
        ):
            if chunk.type == "content" and chunk.content:
                content_event = {"type": "content", "content": chunk.content}
                yield f"data: {json.dumps(content_event)}\n\n"

    # Send done event
    done_event = {"type": "done"}
    yield f"data: {json.dumps(done_event)}\n\n"


@router.post("/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    """Process a chat message with streaming SSE response.

    FR Reference: NFR-001 (streaming responses)

    Args:
        request: ChatRequest with message and optional parameters.

    Returns:
        StreamingResponse with SSE events.
    """
    return StreamingResponse(
        _generate_sse_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.websocket("/ws/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str) -> None:
    """WebSocket endpoint for real-time chat.

    Protocol:
    - Client sends: {"message": "...", "persona": "...", ...}
    - Server sends: {"type": "content|citation|done|error", ...}

    FR Reference: FR-003 (query types with filters)

    Args:
        websocket: WebSocket connection.
        session_id: Session identifier.
    """
    await websocket.accept()

    # Send welcome message
    await websocket.send_json({
        "type": "welcome",
        "session_id": session_id,
    })

    try:
        while True:
            # Receive message
            data = await websocket.receive_json()

            # Parse request
            try:
                request = ChatRequest(
                    message=data.get("message", ""),
                    session_id=session_id,
                    persona=data.get("persona"),
                    query_type=data.get("query_type", "global"),
                    current_chapter=data.get("current_chapter"),
                    selected_text=data.get("selected_text"),
                )
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "error": f"Invalid request: {e}",
                })
                continue

            # Process request
            message_id = str(uuid.uuid4())
            await websocket.send_json({
                "type": "message_start",
                "message_id": message_id,
            })

            # Build filters and run RAG
            filters = _build_search_filters(request)
            pipeline = RAGPipeline()
            rag_result = await pipeline.query(
                message=request.message,
                filters=filters,
            )

            # Send citations
            for citation in rag_result.citations:
                await websocket.send_json({
                    "type": "citation",
                    "citation": {
                        "chapter": citation.chapter,
                        "section": citation.section,
                        "heading": citation.heading,
                        "quote": citation.quote,
                        "link": citation.link,
                    },
                })

            # Stream response
            if rag_result.is_out_of_scope:
                await websocket.send_json({
                    "type": "content",
                    "content": "I don't have information about this topic.",
                })
            else:
                agent = AgentRunner()
                async for chunk in agent.run_stream(
                    message=request.message,
                    rag_context=rag_result.context,
                ):
                    if chunk.type == "content" and chunk.content:
                        await websocket.send_json({
                            "type": "content",
                            "content": chunk.content,
                        })

            # Send done
            await websocket.send_json({"type": "done"})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "error": str(e),
        })
