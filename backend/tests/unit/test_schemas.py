"""Unit tests for Pydantic request/response schemas.

TDD: RED phase - these tests should FAIL until T021-T031 are implemented.
Tests verify schemas match contracts/openapi.yaml specification.
"""

from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError


class TestPersonaTypeEnum:
    """Tests for PersonaType enum."""

    @pytest.mark.unit
    def test_persona_type_values(self) -> None:
        """PersonaType should have correct enum values."""
        from models.schemas import PersonaType

        assert PersonaType.EXPLORER == "Explorer"
        assert PersonaType.BUILDER == "Builder"
        assert PersonaType.ENGINEER == "Engineer"
        assert PersonaType.DEFAULT == "Default"

    @pytest.mark.unit
    def test_persona_type_from_string(self) -> None:
        """PersonaType should be creatable from string."""
        from models.schemas import PersonaType

        assert PersonaType("Explorer") == PersonaType.EXPLORER
        assert PersonaType("Default") == PersonaType.DEFAULT


class TestQueryTypeEnum:
    """Tests for QueryType enum."""

    @pytest.mark.unit
    def test_query_type_values(self) -> None:
        """QueryType should have correct enum values."""
        from models.schemas import QueryType

        assert QueryType.GLOBAL == "global"
        assert QueryType.PAGE == "page"
        assert QueryType.SELECTION == "selection"


class TestChatRequest:
    """Tests for ChatRequest schema (T020-T021)."""

    @pytest.mark.unit
    def test_chat_request_minimal(self) -> None:
        """ChatRequest should accept minimal valid request."""
        from models.schemas import ChatRequest

        request = ChatRequest(message="What is ROS 2?")

        assert request.message == "What is ROS 2?"
        assert request.persona.value == "Default"
        assert request.query_type.value == "global"
        assert request.session_id is None

    @pytest.mark.unit
    def test_chat_request_full(self) -> None:
        """ChatRequest should accept all optional fields."""
        from models.schemas import ChatRequest, PersonaType, QueryType

        session_id = str(uuid4())
        request = ChatRequest(
            message="Explain nodes",
            session_id=session_id,
            persona=PersonaType.BUILDER,
            query_type=QueryType.PAGE,
            current_chapter=2,
            selected_text=None,
        )

        assert request.message == "Explain nodes"
        assert request.session_id == session_id
        assert request.persona == PersonaType.BUILDER
        assert request.query_type == QueryType.PAGE
        assert request.current_chapter == 2

    @pytest.mark.unit
    def test_chat_request_message_min_length(self) -> None:
        """ChatRequest message must have at least 1 character (FR-003)."""
        from models.schemas import ChatRequest

        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(message="")

        assert "message" in str(exc_info.value)

    @pytest.mark.unit
    def test_chat_request_message_max_length(self) -> None:
        """ChatRequest message must not exceed 2000 characters."""
        from models.schemas import ChatRequest

        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(message="x" * 2001)

        assert "message" in str(exc_info.value)

    @pytest.mark.unit
    def test_chat_request_selected_text_max_length(self) -> None:
        """ChatRequest selected_text must not exceed 2000 characters (FR-018)."""
        from models.schemas import ChatRequest, QueryType

        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(
                message="Explain this",
                query_type=QueryType.SELECTION,
                selected_text="x" * 2001,
            )

        assert "selected_text" in str(exc_info.value)

    @pytest.mark.unit
    def test_chat_request_chapter_range(self) -> None:
        """ChatRequest current_chapter must be 1-20."""
        from models.schemas import ChatRequest

        # Valid range
        request = ChatRequest(message="Test", current_chapter=1)
        assert request.current_chapter == 1

        request = ChatRequest(message="Test", current_chapter=20)
        assert request.current_chapter == 20

        # Invalid: below range
        with pytest.raises(ValidationError):
            ChatRequest(message="Test", current_chapter=0)

        # Invalid: above range
        with pytest.raises(ValidationError):
            ChatRequest(message="Test", current_chapter=21)

    @pytest.mark.unit
    def test_chat_request_invalid_persona(self) -> None:
        """ChatRequest should reject invalid persona values."""
        from models.schemas import ChatRequest

        with pytest.raises(ValidationError):
            ChatRequest(message="Test", persona="InvalidPersona")


class TestCitation:
    """Tests for Citation schema (T024-T025)."""

    @pytest.mark.unit
    def test_citation_all_required_fields(self) -> None:
        """Citation should require all fields per FR-004, FR-010."""
        from models.schemas import Citation

        citation = Citation(
            chapter=1,
            section="1.2.1",
            heading="Introduction to ROS 2",
            quote="ROS 2 is the next generation...",
            link="/module-1/chapter-1#intro",
            relevance_score=0.95,
        )

        assert citation.chapter == 1
        assert citation.section == "1.2.1"
        assert citation.heading == "Introduction to ROS 2"
        assert citation.quote == "ROS 2 is the next generation..."
        assert citation.link == "/module-1/chapter-1#intro"
        assert citation.relevance_score == 0.95

    @pytest.mark.unit
    def test_citation_chapter_range(self) -> None:
        """Citation chapter must be 1-20."""
        from models.schemas import Citation

        # Valid
        citation = Citation(
            chapter=20,
            section="20.1",
            heading="Test",
            quote="Test quote",
            link="/test",
            relevance_score=0.5,
        )
        assert citation.chapter == 20

        # Invalid
        with pytest.raises(ValidationError):
            Citation(
                chapter=21,
                section="21.1",
                heading="Test",
                quote="Test quote",
                link="/test",
                relevance_score=0.5,
            )

    @pytest.mark.unit
    def test_citation_relevance_score_range(self) -> None:
        """Citation relevance_score must be 0-1."""
        from models.schemas import Citation

        # Valid boundaries
        Citation(
            chapter=1,
            section="1.1",
            heading="Test",
            quote="Quote",
            link="/test",
            relevance_score=0.0,
        )
        Citation(
            chapter=1,
            section="1.1",
            heading="Test",
            quote="Quote",
            link="/test",
            relevance_score=1.0,
        )

        # Invalid
        with pytest.raises(ValidationError):
            Citation(
                chapter=1,
                section="1.1",
                heading="Test",
                quote="Quote",
                link="/test",
                relevance_score=1.5,
            )

    @pytest.mark.unit
    def test_citation_quote_max_length(self) -> None:
        """Citation quote must not exceed 500 characters (FR-005)."""
        from models.schemas import Citation

        with pytest.raises(ValidationError):
            Citation(
                chapter=1,
                section="1.1",
                heading="Test",
                quote="x" * 501,
                link="/test",
                relevance_score=0.5,
            )


class TestChatResponse:
    """Tests for ChatResponse schema (T022-T023)."""

    @pytest.mark.unit
    def test_chat_response_required_fields(self) -> None:
        """ChatResponse should have all required fields."""
        from models.schemas import ChatResponse, QueryType

        response = ChatResponse(
            session_id=str(uuid4()),
            message_id=str(uuid4()),
            content="ROS 2 is a robotics framework...",
            citations=[],
            query_type=QueryType.GLOBAL,
        )

        assert response.content == "ROS 2 is a robotics framework..."
        assert response.citations == []
        assert response.has_safety_disclaimer is False
        assert response.is_selection_scoped is False

    @pytest.mark.unit
    def test_chat_response_with_citations(self) -> None:
        """ChatResponse should include citations array."""
        from models.schemas import ChatResponse, Citation, QueryType

        citation = Citation(
            chapter=1,
            section="1.1",
            heading="Intro",
            quote="Test quote",
            link="/test",
            relevance_score=0.9,
        )

        response = ChatResponse(
            session_id=str(uuid4()),
            message_id=str(uuid4()),
            content="Response with citation",
            citations=[citation],
            query_type=QueryType.GLOBAL,
        )

        assert len(response.citations) == 1
        assert response.citations[0].chapter == 1

    @pytest.mark.unit
    def test_chat_response_max_citations(self) -> None:
        """ChatResponse citations array max 5 items (FR-009)."""
        from models.schemas import ChatResponse, Citation, QueryType

        citations = [
            Citation(
                chapter=i,
                section=f"{i}.1",
                heading=f"Heading {i}",
                quote=f"Quote {i}",
                link=f"/test{i}",
                relevance_score=0.9,
            )
            for i in range(1, 7)  # 6 citations
        ]

        with pytest.raises(ValidationError) as exc_info:
            ChatResponse(
                session_id=str(uuid4()),
                message_id=str(uuid4()),
                content="Too many citations",
                citations=citations,
                query_type=QueryType.GLOBAL,
            )

        assert "citations" in str(exc_info.value)

    @pytest.mark.unit
    def test_chat_response_safety_disclaimer(self) -> None:
        """ChatResponse should track safety disclaimer flag (FR-021)."""
        from models.schemas import ChatResponse, QueryType

        response = ChatResponse(
            session_id=str(uuid4()),
            message_id=str(uuid4()),
            content="Warning: Physical operation...",
            citations=[],
            query_type=QueryType.GLOBAL,
            has_safety_disclaimer=True,
        )

        assert response.has_safety_disclaimer is True


class TestStreamChunk:
    """Tests for StreamChunk schema (T026-T027)."""

    @pytest.mark.unit
    def test_stream_chunk_content_type(self) -> None:
        """StreamChunk should support content type."""
        from models.schemas import StreamChunk

        chunk = StreamChunk(type="content", content="Hello")

        assert chunk.type == "content"
        assert chunk.content == "Hello"
        assert chunk.citation is None

    @pytest.mark.unit
    def test_stream_chunk_citation_type(self) -> None:
        """StreamChunk should support citation type."""
        from models.schemas import Citation, StreamChunk

        citation = Citation(
            chapter=1,
            section="1.1",
            heading="Test",
            quote="Quote",
            link="/test",
            relevance_score=0.9,
        )

        chunk = StreamChunk(type="citation", citation=citation)

        assert chunk.type == "citation"
        assert chunk.citation is not None
        assert chunk.citation.chapter == 1

    @pytest.mark.unit
    def test_stream_chunk_done_type(self) -> None:
        """StreamChunk should support done type with IDs."""
        from models.schemas import StreamChunk

        session_id = str(uuid4())
        message_id = str(uuid4())

        chunk = StreamChunk(
            type="done",
            session_id=session_id,
            message_id=message_id,
        )

        assert chunk.type == "done"
        assert chunk.session_id == session_id
        assert chunk.message_id == message_id

    @pytest.mark.unit
    def test_stream_chunk_error_type(self) -> None:
        """StreamChunk should support error type."""
        from models.schemas import StreamChunk

        chunk = StreamChunk(
            type="error",
            error="connection_lost",
            message="Connection to LLM service was lost",
        )

        assert chunk.type == "error"
        assert chunk.error == "connection_lost"


class TestSessionSchemas:
    """Tests for Session schemas (T028-T029)."""

    @pytest.mark.unit
    def test_create_session_request_defaults(self) -> None:
        """CreateSessionRequest should have sensible defaults."""
        from models.schemas import CreateSessionRequest, PersonaType

        request = CreateSessionRequest()

        assert request.persona == PersonaType.DEFAULT
        assert request.current_chapter is None
        assert request.current_page is None

    @pytest.mark.unit
    def test_create_session_request_full(self) -> None:
        """CreateSessionRequest should accept all optional fields."""
        from models.schemas import CreateSessionRequest, PersonaType

        request = CreateSessionRequest(
            persona=PersonaType.EXPLORER,
            current_chapter=3,
            current_page="/module-1/chapter-3",
        )

        assert request.persona == PersonaType.EXPLORER
        assert request.current_chapter == 3
        assert request.current_page == "/module-1/chapter-3"

    @pytest.mark.unit
    def test_session_response_required_fields(self) -> None:
        """SessionResponse should have all required fields."""
        from models.schemas import PersonaType, SessionResponse

        response = SessionResponse(
            id=str(uuid4()),
            persona=PersonaType.BUILDER,
            created_at=datetime.utcnow(),
            is_active=True,
        )

        assert response.is_active is True
        assert response.persona == PersonaType.BUILDER

    @pytest.mark.unit
    def test_session_detail_response_extends_session(self) -> None:
        """SessionDetailResponse should extend SessionResponse."""
        from models.schemas import PersonaType, SessionDetailResponse

        response = SessionDetailResponse(
            id=str(uuid4()),
            persona=PersonaType.DEFAULT,
            created_at=datetime.utcnow(),
            is_active=True,
            message_count=5,
            last_activity=datetime.utcnow(),
        )

        assert response.message_count == 5
        assert response.last_activity is not None


class TestErrorResponse:
    """Tests for ErrorResponse schema (T030-T031)."""

    @pytest.mark.unit
    def test_error_response_required_fields(self) -> None:
        """ErrorResponse should have required error and message fields."""
        from models.schemas import ErrorResponse

        error = ErrorResponse(
            error="validation_error",
            message="Invalid persona type",
        )

        assert error.error == "validation_error"
        assert error.message == "Invalid persona type"
        assert error.code is None
        assert error.details is None

    @pytest.mark.unit
    def test_error_response_with_code(self) -> None:
        """ErrorResponse should support optional code field."""
        from models.schemas import ErrorResponse

        error = ErrorResponse(
            error="validation_error",
            message="Selection too long",
            code="SELECTION_TOO_LONG",
        )

        assert error.code == "SELECTION_TOO_LONG"

    @pytest.mark.unit
    def test_error_response_with_details(self) -> None:
        """ErrorResponse should support optional details object."""
        from models.schemas import ErrorResponse

        error = ErrorResponse(
            error="validation_error",
            message="Multiple validation errors",
            code="VALIDATION_FAILED",
            details={"field": "message", "constraint": "max_length"},
        )

        assert error.details == {"field": "message", "constraint": "max_length"}


class TestMessageSchemas:
    """Tests for Message-related schemas."""

    @pytest.mark.unit
    def test_message_summary_required_fields(self) -> None:
        """MessageSummary should have all required fields."""
        from models.schemas import MessageSummary, QueryType

        summary = MessageSummary(
            id=str(uuid4()),
            role="user",
            content="What is ROS 2?",
            created_at=datetime.utcnow(),
            query_type=QueryType.GLOBAL,
        )

        assert summary.role == "user"
        assert summary.content == "What is ROS 2?"

    @pytest.mark.unit
    def test_message_list_response(self) -> None:
        """MessageListResponse should have messages array and pagination."""
        from models.schemas import MessageListResponse, MessageSummary, QueryType

        messages = [
            MessageSummary(
                id=str(uuid4()),
                role="user",
                content="Question",
                created_at=datetime.utcnow(),
                query_type=QueryType.GLOBAL,
            )
        ]

        response = MessageListResponse(
            messages=messages,
            has_more=True,
            next_cursor="abc123",
        )

        assert len(response.messages) == 1
        assert response.has_more is True
        assert response.next_cursor == "abc123"


class TestHealthResponse:
    """Tests for HealthResponse schema."""

    @pytest.mark.unit
    def test_health_response_healthy(self) -> None:
        """HealthResponse should represent healthy status."""
        from models.schemas import HealthResponse

        response = HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow(),
            version="1.0.0",
        )

        assert response.status == "healthy"
        assert response.version == "1.0.0"

    @pytest.mark.unit
    def test_health_response_with_dependencies(self) -> None:
        """HealthResponse should include dependency status."""
        from models.schemas import HealthResponse

        response = HealthResponse(
            status="degraded",
            timestamp=datetime.utcnow(),
            dependencies={
                "database": "healthy",
                "vector_store": "healthy",
                "llm_service": "unhealthy",
            },
        )

        assert response.status == "degraded"
        assert response.dependencies["llm_service"] == "unhealthy"
