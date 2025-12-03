"""Contract tests for OpenAPI schema compliance.

TDD: Tests that API responses match the OpenAPI specification in contracts/openapi.yaml.
FR Reference: Contract validation for API consistency.

Note: These tests validate schema structures and API validation rules without
requiring full service connectivity. Integration tests cover end-to-end flows.
"""

import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError


class TestChatResponseSchema:
    """Tests for ChatResponse schema compliance."""

    @pytest.mark.contract
    def test_chat_response_has_required_fields(self) -> None:
        """ChatResponse must have session_id, message_id, content, citations, query_type."""
        from models.schemas import ChatResponse, Citation, QueryType

        response = ChatResponse(
            session_id="123e4567-e89b-12d3-a456-426614174000",
            message_id="123e4567-e89b-12d3-a456-426614174001",
            content="Test response content",
            citations=[],
            query_type=QueryType.GLOBAL,
        )

        # Verify required fields exist
        assert response.session_id == "123e4567-e89b-12d3-a456-426614174000"
        assert response.message_id == "123e4567-e89b-12d3-a456-426614174001"
        assert response.content == "Test response content"
        assert response.citations == []
        assert response.query_type == QueryType.GLOBAL

    @pytest.mark.contract
    def test_chat_response_citations_max_five(self) -> None:
        """ChatResponse citations must have max 5 items per FR-009."""
        from models.schemas import ChatResponse, Citation, QueryType

        # Create 6 citations
        citations = [
            Citation(
                chapter=i,
                section=f"{i}.1",
                heading=f"Section {i}",
                quote=f"Quote {i}",
                link=f"/docs/chapter-{i}",
            )
            for i in range(1, 7)
        ]

        # Should raise validation error for > 5 citations
        with pytest.raises(ValidationError):
            ChatResponse(
                session_id="test-session",
                message_id="test-message",
                content="Test",
                citations=citations,  # 6 citations
                query_type=QueryType.GLOBAL,
            )

        # 5 citations should be valid
        valid_response = ChatResponse(
            session_id="test-session",
            message_id="test-message",
            content="Test",
            citations=citations[:5],
            query_type=QueryType.GLOBAL,
        )
        assert len(valid_response.citations) == 5

    @pytest.mark.contract
    def test_chat_response_query_type_valid_enum(self) -> None:
        """ChatResponse query_type must be global, page, or selection."""
        from models.schemas import ChatResponse, QueryType

        # Test each valid query type
        for query_type in [QueryType.GLOBAL, QueryType.PAGE, QueryType.SELECTION]:
            response = ChatResponse(
                session_id="test-session",
                message_id="test-message",
                content="Test",
                citations=[],
                query_type=query_type,
            )
            assert response.query_type == query_type


class TestCitationSchema:
    """Tests for Citation schema compliance."""

    @pytest.mark.contract
    def test_citation_has_required_fields(self) -> None:
        """Citation must have chapter, section, heading, quote, link."""
        from models.schemas import Citation

        # Required fields only (relevance_score is optional per OpenAPI)
        citation = Citation(
            chapter=1,
            section="1.1",
            heading="Test Heading",
            quote="Test quote",
            link="/docs/test",
        )

        # Verify all required fields
        assert citation.chapter == 1
        assert citation.section == "1.1"
        assert citation.heading == "Test Heading"
        assert citation.quote == "Test quote"
        assert citation.link == "/docs/test"
        # relevance_score is optional
        assert citation.relevance_score is None

    @pytest.mark.contract
    def test_citation_chapter_range(self) -> None:
        """Citation chapter must be between 1 and 20."""
        from models.schemas import Citation

        # Valid chapters
        for chapter in [1, 10, 20]:
            citation = Citation(
                chapter=chapter,
                section="1.1",
                heading="Test",
                quote="Quote",
                link="/docs/test",
            )
            assert citation.chapter == chapter

        # Invalid chapters should raise validation error
        with pytest.raises(ValidationError):
            Citation(
                chapter=0,
                section="1.1",
                heading="Test",
                quote="Quote",
                link="/docs/test",
            )

        with pytest.raises(ValidationError):
            Citation(
                chapter=21,
                section="1.1",
                heading="Test",
                quote="Quote",
                link="/docs/test",
            )

    @pytest.mark.contract
    def test_citation_relevance_score_optional(self) -> None:
        """Citation relevance_score is optional per OpenAPI spec."""
        from models.schemas import Citation

        # Without relevance_score
        citation = Citation(
            chapter=1,
            section="1.1",
            heading="Test",
            quote="Quote",
            link="/docs/test",
        )
        assert citation.relevance_score is None

        # With relevance_score
        citation_with_score = Citation(
            chapter=1,
            section="1.1",
            heading="Test",
            quote="Quote",
            link="/docs/test",
            relevance_score=0.95,
        )
        assert citation_with_score.relevance_score == 0.95

    @pytest.mark.contract
    def test_citation_relevance_score_bounds(self) -> None:
        """Citation relevance_score must be between 0 and 1."""
        from models.schemas import Citation

        # Valid scores
        for score in [0.0, 0.5, 1.0]:
            citation = Citation(
                chapter=1,
                section="1.1",
                heading="Test",
                quote="Quote",
                link="/docs/test",
                relevance_score=score,
            )
            assert citation.relevance_score == score

        # Invalid scores
        with pytest.raises(ValidationError):
            Citation(
                chapter=1,
                section="1.1",
                heading="Test",
                quote="Quote",
                link="/docs/test",
                relevance_score=-0.1,
            )

        with pytest.raises(ValidationError):
            Citation(
                chapter=1,
                section="1.1",
                heading="Test",
                quote="Quote",
                link="/docs/test",
                relevance_score=1.1,
            )


class TestSessionResponseSchema:
    """Tests for Session response schemas compliance."""

    @pytest.mark.contract
    def test_session_response_has_required_fields(self) -> None:
        """SessionResponse must have id, persona, created_at, is_active."""
        from datetime import datetime

        from models.schemas import PersonaType, SessionResponse

        response = SessionResponse(
            id="123e4567-e89b-12d3-a456-426614174000",
            persona=PersonaType.EXPLORER,
            created_at=datetime.now(),
            is_active=True,
        )

        # Required fields per OpenAPI spec
        assert response.id == "123e4567-e89b-12d3-a456-426614174000"
        assert response.persona == PersonaType.EXPLORER
        assert response.created_at is not None
        assert response.is_active is True

    @pytest.mark.contract
    def test_session_persona_valid_enum(self) -> None:
        """SessionResponse persona must be Explorer, Builder, Engineer, or Default."""
        from datetime import datetime

        from models.schemas import PersonaType, SessionResponse

        valid_personas = [
            PersonaType.EXPLORER,
            PersonaType.BUILDER,
            PersonaType.ENGINEER,
            PersonaType.DEFAULT,
        ]
        for persona in valid_personas:
            response = SessionResponse(
                id="test-id",
                persona=persona,
                created_at=datetime.now(),
                is_active=True,
            )
            assert response.persona == persona


class TestHealthResponseSchema:
    """Tests for Health response schema compliance."""

    @pytest.mark.contract
    def test_health_response_has_required_fields(self) -> None:
        """HealthResponse must have status and timestamp."""
        from datetime import datetime

        from models.schemas import HealthResponse

        response = HealthResponse(
            status="healthy",
            timestamp=datetime.now(),
        )

        # Required fields per OpenAPI spec
        assert response.status == "healthy"
        assert response.timestamp is not None

    @pytest.mark.contract
    def test_health_status_valid_values(self) -> None:
        """HealthResponse status must be healthy, degraded, or unhealthy."""
        from datetime import datetime

        from models.schemas import HealthResponse

        valid_statuses = ["healthy", "degraded", "unhealthy"]
        for status in valid_statuses:
            response = HealthResponse(
                status=status,
                timestamp=datetime.now(),
            )
            assert response.status == status


class TestErrorResponseSchema:
    """Tests for ErrorResponse schema compliance."""

    @pytest.mark.contract
    def test_error_response_has_required_fields(self) -> None:
        """ErrorResponse must have error and message fields."""
        from models.schemas import ErrorResponse

        response = ErrorResponse(
            error="validation_error",
            message="Invalid request format",
        )

        # Required fields per OpenAPI spec
        assert response.error == "validation_error"
        assert response.message == "Invalid request format"

    @pytest.mark.contract
    def test_error_response_optional_fields(self) -> None:
        """ErrorResponse code and details are optional."""
        from models.schemas import ErrorResponse

        # Without optional fields
        response = ErrorResponse(
            error="test_error",
            message="Test message",
        )
        assert response.code is None
        assert response.details is None

        # With optional fields
        response_full = ErrorResponse(
            error="test_error",
            message="Test message",
            code="TEST_CODE",
            details={"field": "value"},
        )
        assert response_full.code == "TEST_CODE"
        assert response_full.details == {"field": "value"}


class TestChatRequestValidation:
    """Tests for ChatRequest validation per OpenAPI spec."""

    @pytest.mark.contract
    def test_message_required(self) -> None:
        """ChatRequest requires message field."""
        from models.schemas import ChatRequest

        with pytest.raises(ValidationError):
            ChatRequest()  # No message provided

    @pytest.mark.contract
    def test_message_min_length(self) -> None:
        """ChatRequest message must have at least 1 character."""
        from models.schemas import ChatRequest

        with pytest.raises(ValidationError):
            ChatRequest(message="")  # Empty message

        # Single character is valid
        request = ChatRequest(message="x")
        assert request.message == "x"

    @pytest.mark.contract
    def test_message_max_length(self) -> None:
        """ChatRequest message must be <= 2000 characters."""
        from models.schemas import ChatRequest

        # Message too long
        with pytest.raises(ValidationError):
            ChatRequest(message="x" * 2001)

        # Exactly 2000 is valid
        request = ChatRequest(message="x" * 2000)
        assert len(request.message) == 2000

    @pytest.mark.contract
    def test_selected_text_max_length(self) -> None:
        """ChatRequest selected_text must be <= 2000 characters."""
        from models.schemas import ChatRequest, QueryType

        # Selected text too long
        with pytest.raises(ValidationError):
            ChatRequest(
                message="Explain this",
                query_type=QueryType.SELECTION,
                selected_text="x" * 2001,
            )

        # Exactly 2000 is valid
        request = ChatRequest(
            message="Explain this",
            query_type=QueryType.SELECTION,
            selected_text="x" * 2000,
        )
        assert len(request.selected_text) == 2000

    @pytest.mark.contract
    def test_persona_defaults_to_default(self) -> None:
        """ChatRequest persona defaults to Default if not provided."""
        from models.schemas import ChatRequest, PersonaType

        request = ChatRequest(message="Test message")
        assert request.persona == PersonaType.DEFAULT

    @pytest.mark.contract
    def test_query_type_defaults_to_global(self) -> None:
        """ChatRequest query_type defaults to global if not provided."""
        from models.schemas import ChatRequest, QueryType

        request = ChatRequest(message="Test message")
        assert request.query_type == QueryType.GLOBAL

    @pytest.mark.contract
    def test_current_chapter_range(self) -> None:
        """ChatRequest current_chapter must be between 1 and 20."""
        from models.schemas import ChatRequest

        # Valid chapters
        for chapter in [1, 10, 20]:
            request = ChatRequest(message="Test", current_chapter=chapter)
            assert request.current_chapter == chapter

        # Invalid chapters
        with pytest.raises(ValidationError):
            ChatRequest(message="Test", current_chapter=0)

        with pytest.raises(ValidationError):
            ChatRequest(message="Test", current_chapter=21)


class TestAPIEndpointValidation:
    """Tests for API endpoint validation using TestClient."""

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

    @pytest.mark.contract
    def test_chat_rejects_invalid_persona(self, mock_env) -> None:
        """POST /chat rejects invalid persona values."""
        from fastapi.testclient import TestClient

        from main import app

        client = TestClient(app)
        response = client.post(
            "/chat",
            json={"message": "Test", "persona": "InvalidPersona"}
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.contract
    def test_chat_rejects_invalid_query_type(self, mock_env) -> None:
        """POST /chat rejects invalid query_type values."""
        from fastapi.testclient import TestClient

        from main import app

        client = TestClient(app)
        response = client.post(
            "/chat",
            json={"message": "Test", "query_type": "invalid_type"}
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.contract
    def test_chat_rejects_missing_message(self, mock_env) -> None:
        """POST /chat requires message field."""
        from fastapi.testclient import TestClient

        from main import app

        client = TestClient(app)
        response = client.post("/chat", json={})

        assert response.status_code == 422  # Validation error

    @pytest.mark.contract
    def test_health_endpoint_returns_required_fields(self, mock_env) -> None:
        """GET /health returns status and timestamp."""
        from fastapi.testclient import TestClient

        from main import app

        client = TestClient(app)
        response = client.get("/health")

        # Accept 200 or 503 based on service availability
        assert response.status_code in [200, 503]
        data = response.json()

        # Required fields per OpenAPI spec
        assert "status" in data
        assert "timestamp" in data
        assert data["status"] in ["healthy", "degraded", "unhealthy"]
