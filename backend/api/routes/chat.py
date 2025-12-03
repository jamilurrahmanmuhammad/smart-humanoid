"""Chat API routes - POST /chat, POST /chat/stream, WebSocket /ws/chat."""

import json
import logging
import uuid
from typing import Any, AsyncGenerator

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, StreamingResponse

from models.schemas import (
    ChatRequest,
    ChatResponse,
    Citation,
    ErrorResponse,
    PersonaType,
    QueryType,
    StreamChunk,
)
from services.agent import AgentRunner
from services.rag import RAGPipeline, is_vague_contextual_query
from services.vector_store import SearchFilters

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


class ServiceUnavailableError(Exception):
    """Raised when a required service is unavailable."""

    pass


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


@router.post("", response_model=ChatResponse, responses={503: {"model": ErrorResponse}})
async def chat(request: ChatRequest) -> ChatResponse | JSONResponse:
    """Process a chat message and return response with citations.

    FR References:
    - FR-001: RAG-based Q&A
    - FR-004: Inline citations
    - FR-012: Session creation
    - FR-028: Graceful degradation

    Args:
        request: ChatRequest with message and optional parameters.

    Returns:
        ChatResponse with content, citations, and session info.
        503 JSONResponse if services are unavailable.
    """
    # Import inside function to avoid module-level import issues
    from services.rag import RAGPipeline as LocalRAGPipeline

    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    message_id = str(uuid.uuid4())

    # Build search filters
    filters = _build_search_filters(request)

    # Determine if this is a page-scoped query
    is_page_scoped = request.query_type == QueryType.PAGE or (
        request.current_chapter is not None and request.query_type != QueryType.SELECTION
    )

    try:
        # Run RAG pipeline
        pipeline = LocalRAGPipeline()
        rag_result = await pipeline.query(
            message=request.message,
            filters=filters,
            is_page_scoped=is_page_scoped,
        )
    except Exception as e:
        # Log the error internally without exposing details
        logger.error(f"RAG pipeline error: {type(e).__name__}")
        return JSONResponse(
            status_code=503,
            content={
                "error": "INDEX_UNAVAILABLE",
                "message": "The search index is temporarily unavailable. Please try again later.",
            },
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

    try:
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
    except Exception as e:
        # Log the error internally without exposing details
        logger.error(f"Agent error: {type(e).__name__}")
        return JSONResponse(
            status_code=503,
            content={
                "error": "SERVICE_UNAVAILABLE",
                "message": "The AI service is temporarily unavailable. Please try again later.",
            },
        )

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

    # Determine if this is a page-scoped query
    is_page_scoped = request.query_type == QueryType.PAGE or (
        request.current_chapter is not None and request.query_type != QueryType.SELECTION
    )

    # Run RAG pipeline
    pipeline = RAGPipeline()
    rag_result = await pipeline.query(
        message=request.message,
        filters=filters,
        is_page_scoped=is_page_scoped,
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

    # Maintain conversation history for this session
    conversation_history: list[dict[str, str]] = []
    # Store current page context (FR-032: Accept page content via WebSocket)
    # Max page content length per FR-034
    MAX_PAGE_CONTENT_LENGTH = 8000
    current_page_context: dict[str, Any] = {
        "chapter": None,
        "page": None,
        "page_content": None,  # FR-031: Store page content for vague queries
    }

    # Send welcome message
    await websocket.send_json({
        "type": "welcome",
        "session_id": session_id,
    })

    try:
        while True:
            # Receive message
            logger.info("Waiting for WebSocket message...")
            data = await websocket.receive_json()
            logger.info(f"Received WebSocket message: {data}")

            # Parse request - handle both direct format and wrapped format
            try:
                # Check if it's a context message - update page context
                if data.get("type") == "context":
                    context_data = data.get("data", {})
                    current_page_context["chapter"] = context_data.get("current_chapter")
                    current_page_context["page"] = context_data.get("current_page")
                    # FR-032: Accept page_content, FR-034: Truncate to 8000 chars
                    page_content = context_data.get("page_content")
                    if page_content:
                        current_page_context["page_content"] = page_content[:MAX_PAGE_CONTENT_LENGTH]
                    else:
                        current_page_context["page_content"] = None
                    logger.info(f"Updated page context: chapter={current_page_context['chapter']}, page={current_page_context['page']}, page_content_len={len(current_page_context.get('page_content') or '')}")
                    continue

                # Check if it's a ping message
                if data.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                    continue

                # Extract message from either format:
                # Format 1 (direct): {"message": "...", "query_type": "...", ...}
                # Format 2 (wrapped): {"type": "message", "data": {"content": "...", ...}}
                if data.get("type") == "message" and "data" in data:
                    # Wrapped format from frontend
                    wrapped_data = data["data"]
                    message = wrapped_data.get("content", "")
                    query_type = wrapped_data.get("query_type")
                    current_chapter = wrapped_data.get("current_chapter")
                    selected_text = wrapped_data.get("selected_text")
                    persona = wrapped_data.get("persona")
                else:
                    # Direct format
                    message = data.get("message", "")
                    query_type = data.get("query_type")
                    current_chapter = data.get("current_chapter")
                    selected_text = data.get("selected_text")
                    persona = data.get("persona")

                logger.info(f"Processing chat message: {message[:100]}...")

                # Build request kwargs, only including values that are provided
                request_kwargs: dict[str, Any] = {
                    "message": message,
                    "session_id": session_id,
                }

                # Only add optional fields if provided (avoid passing None)
                if persona:
                    request_kwargs["persona"] = persona
                if query_type:
                    request_kwargs["query_type"] = query_type

                # Use current_chapter from message, or fall back to page context
                effective_chapter = current_chapter if current_chapter is not None else current_page_context.get("chapter")
                if effective_chapter is not None:
                    request_kwargs["current_chapter"] = effective_chapter

                if selected_text:
                    request_kwargs["selected_text"] = selected_text

                request = ChatRequest(**request_kwargs)

                # Add user message to conversation history
                conversation_history.append({
                    "role": "user",
                    "content": message,
                })
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
            # Determine if this is a page-scoped query (has chapter context)
            is_page_scoped = request.query_type == QueryType.PAGE or (
                request.current_chapter is not None and request.query_type != QueryType.SELECTION
            )

            # FR-033: Check if this is a vague contextual query that needs page content
            page_content = current_page_context.get("page_content")
            is_vague = is_vague_contextual_query(request.message)

            rag_result = await pipeline.query(
                message=request.message,
                filters=filters,
                is_page_scoped=is_page_scoped,
            )

            # FR-033: If vague query + page content available, prepend to RAG context
            if is_vague and page_content:
                page_context_str = f"[Current Page Content]\n{page_content}\n\n"
                if rag_result.context:
                    rag_result.context = page_context_str + "[RAG Results]\n" + rag_result.context
                else:
                    rag_result.context = page_context_str
                logger.info(f"Injected page content for vague query: {request.message[:50]}...")

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

            # Stream response and collect for history
            response_parts: list[str] = []

            if rag_result.is_out_of_scope:
                out_of_scope_msg = "I don't have information about this topic in the textbook."
                await websocket.send_json({
                    "type": "content",
                    "content": out_of_scope_msg,
                })
                response_parts.append(out_of_scope_msg)
            else:
                agent = AgentRunner()
                # Pass conversation history (excluding the current user message which was just added)
                history_for_agent = conversation_history[:-1] if len(conversation_history) > 1 else None
                async for chunk in agent.run_stream(
                    message=request.message,
                    context=history_for_agent,
                    rag_context=rag_result.context,
                ):
                    if chunk.type == "content" and chunk.content:
                        await websocket.send_json({
                            "type": "content",
                            "content": chunk.content,
                        })
                        response_parts.append(chunk.content)

            # Add assistant response to conversation history
            full_response = "".join(response_parts)
            if full_response:
                conversation_history.append({
                    "role": "assistant",
                    "content": full_response,
                })

            # Keep conversation history reasonable (last 10 exchanges = 20 messages)
            if len(conversation_history) > 20:
                conversation_history[:] = conversation_history[-20:]

            # Send done
            await websocket.send_json({"type": "done"})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "error": str(e),
        })
