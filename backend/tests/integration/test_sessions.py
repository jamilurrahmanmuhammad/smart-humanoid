"""Integration tests for session management API.

TDD: Tests for T097-T104 - Session CRUD endpoints.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def mock_env(monkeypatch):
    """Set up environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
    monkeypatch.setenv("QDRANT_URL", "http://localhost:6333")
    monkeypatch.setenv("DEBUG", "false")


class TestPostSessions:
    """Tests for POST /sessions endpoint (T097)."""

    @pytest.mark.integration
    def test_creates_session_with_defaults(self, mock_env) -> None:
        """POST /sessions should create session with default persona (FR-012)."""
        from main import app
        from core.database import get_async_session

        # Override dependency
        async def mock_db():
            mock_session = AsyncMock()
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()
            yield mock_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.post("/sessions", json={})

            assert response.status_code == 200
            data = response.json()
            assert "id" in data
            assert data["persona"] == "Default"
            assert data["is_active"] is True
            assert "created_at" in data
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.integration
    def test_creates_session_with_persona(self, mock_env) -> None:
        """POST /sessions should create session with specified persona (FR-015)."""
        from main import app
        from core.database import get_async_session

        async def mock_db():
            mock_session = AsyncMock()
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()
            yield mock_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.post(
                    "/sessions",
                    json={"persona": "Explorer", "current_chapter": 3},
                )

            assert response.status_code == 200
            data = response.json()
            assert data["persona"] == "Explorer"
            assert data["current_chapter"] == 3
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.integration
    def test_creates_session_with_page_context(self, mock_env) -> None:
        """POST /sessions should store current page context."""
        from main import app
        from core.database import get_async_session

        async def mock_db():
            mock_session = AsyncMock()
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()
            yield mock_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.post(
                    "/sessions",
                    json={
                        "persona": "Builder",
                        "current_chapter": 5,
                        "current_page": "/chapter-5/ros2-nodes",
                    },
                )

            assert response.status_code == 200
            data = response.json()
            assert data["current_page"] == "/chapter-5/ros2-nodes"
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.integration
    def test_returns_session_response_schema(self, mock_env) -> None:
        """POST /sessions should return SessionResponse schema."""
        from main import app
        from core.database import get_async_session

        async def mock_db():
            mock_session = AsyncMock()
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()
            yield mock_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.post("/sessions", json={})

            assert response.status_code == 200
            data = response.json()

            # Validate all required fields from SessionResponse
            required_fields = [
                "id", "persona", "current_chapter", "current_page",
                "created_at", "is_active"
            ]
            for field in required_fields:
                assert field in data, f"Missing field: {field}"
        finally:
            app.dependency_overrides.clear()


class TestGetSession:
    """Tests for GET /sessions/{id} endpoint (T099)."""

    @pytest.mark.integration
    def test_returns_session_by_id(self, mock_env) -> None:
        """GET /sessions/{id} should return session details (FR-012)."""
        from main import app
        from core.database import get_async_session
        from models.database import ChatSessionModel

        session_id = str(uuid4())
        mock_session_model = MagicMock(spec=ChatSessionModel)
        mock_session_model.id = session_id
        mock_session_model.persona = "Explorer"
        mock_session_model.current_chapter = 2
        mock_session_model.current_page = "/chapter-2/intro"
        mock_session_model.created_at = datetime.now(timezone.utc)
        mock_session_model.is_active = True
        mock_session_model.messages = []

        async def mock_db():
            mock_db_session = AsyncMock()
            mock_db_session.get = AsyncMock(return_value=mock_session_model)
            yield mock_db_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.get(f"/sessions/{session_id}")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == session_id
            assert data["persona"] == "Explorer"
            assert data["current_chapter"] == 2
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.integration
    def test_returns_404_for_unknown_session(self, mock_env) -> None:
        """GET /sessions/{id} should return 404 if session not found."""
        from main import app
        from core.database import get_async_session

        unknown_id = str(uuid4())

        async def mock_db():
            mock_db_session = AsyncMock()
            mock_db_session.get = AsyncMock(return_value=None)
            yield mock_db_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.get(f"/sessions/{unknown_id}")

            assert response.status_code == 404
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.integration
    def test_returns_session_detail_response(self, mock_env) -> None:
        """GET /sessions/{id} should return SessionDetailResponse with message count."""
        from main import app
        from core.database import get_async_session
        from models.database import ChatSessionModel, ChatMessageModel

        session_id = str(uuid4())
        now = datetime.now(timezone.utc)

        mock_message1 = MagicMock(spec=ChatMessageModel)
        mock_message1.created_at = now - timedelta(hours=1)
        mock_message1.expires_at = now + timedelta(hours=23)

        mock_message2 = MagicMock(spec=ChatMessageModel)
        mock_message2.created_at = now
        mock_message2.expires_at = now + timedelta(hours=24)

        mock_session_model = MagicMock(spec=ChatSessionModel)
        mock_session_model.id = session_id
        mock_session_model.persona = "Default"
        mock_session_model.current_chapter = None
        mock_session_model.current_page = None
        mock_session_model.created_at = now
        mock_session_model.is_active = True
        mock_session_model.messages = [mock_message1, mock_message2]

        async def mock_db():
            mock_db_session = AsyncMock()
            mock_db_session.get = AsyncMock(return_value=mock_session_model)
            yield mock_db_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.get(f"/sessions/{session_id}")

            assert response.status_code == 200
            data = response.json()
            assert "message_count" in data
            assert "last_activity" in data
        finally:
            app.dependency_overrides.clear()


class TestDeleteSession:
    """Tests for DELETE /sessions/{id} endpoint (T101)."""

    @pytest.mark.integration
    def test_marks_session_inactive(self, mock_env) -> None:
        """DELETE /sessions/{id} should mark session as inactive (FR-012)."""
        from main import app
        from core.database import get_async_session
        from models.database import ChatSessionModel

        session_id = str(uuid4())
        mock_session_model = MagicMock(spec=ChatSessionModel)
        mock_session_model.id = session_id
        mock_session_model.is_active = True

        async def mock_db():
            mock_db_session = AsyncMock()
            mock_db_session.get = AsyncMock(return_value=mock_session_model)
            mock_db_session.commit = AsyncMock()
            yield mock_db_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.delete(f"/sessions/{session_id}")

            assert response.status_code == 204
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.integration
    def test_returns_404_for_unknown_session(self, mock_env) -> None:
        """DELETE /sessions/{id} should return 404 if session not found."""
        from main import app
        from core.database import get_async_session

        unknown_id = str(uuid4())

        async def mock_db():
            mock_db_session = AsyncMock()
            mock_db_session.get = AsyncMock(return_value=None)
            yield mock_db_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.delete(f"/sessions/{unknown_id}")

            assert response.status_code == 404
        finally:
            app.dependency_overrides.clear()


class TestGetSessionMessages:
    """Tests for GET /sessions/{id}/messages endpoint (T103)."""

    @pytest.mark.integration
    def test_returns_messages_for_session(self, mock_env) -> None:
        """GET /sessions/{id}/messages should return message list (FR-027)."""
        from main import app
        from core.database import get_async_session
        from models.database import ChatSessionModel, ChatMessageModel

        session_id = str(uuid4())
        now = datetime.now(timezone.utc)

        # Create mock messages
        mock_message1 = MagicMock(spec=ChatMessageModel)
        mock_message1.id = str(uuid4())
        mock_message1.role = "user"
        mock_message1.content = "What is ROS 2?"
        mock_message1.created_at = now - timedelta(minutes=5)
        mock_message1.expires_at = now + timedelta(hours=24)
        mock_message1.query_type = "global"
        mock_message1.has_safety_disclaimer = False
        mock_message1.citations = []

        mock_message2 = MagicMock(spec=ChatMessageModel)
        mock_message2.id = str(uuid4())
        mock_message2.role = "assistant"
        mock_message2.content = "ROS 2 is a robotics middleware..."
        mock_message2.created_at = now - timedelta(minutes=4)
        mock_message2.expires_at = now + timedelta(hours=24)
        mock_message2.query_type = "global"
        mock_message2.has_safety_disclaimer = False
        mock_message2.citations = []

        mock_session_model = MagicMock(spec=ChatSessionModel)
        mock_session_model.id = session_id
        mock_session_model.is_active = True
        mock_session_model.messages = [mock_message1, mock_message2]

        async def mock_db():
            mock_db_session = AsyncMock()
            mock_db_session.get = AsyncMock(return_value=mock_session_model)
            yield mock_db_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.get(f"/sessions/{session_id}/messages")

            assert response.status_code == 200
            data = response.json()
            assert "messages" in data
            assert "has_more" in data
            assert len(data["messages"]) == 2
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.integration
    def test_excludes_expired_messages(self, mock_env) -> None:
        """GET /sessions/{id}/messages should exclude expired messages (FR-027)."""
        from main import app
        from core.database import get_async_session
        from models.database import ChatSessionModel, ChatMessageModel

        session_id = str(uuid4())
        now = datetime.now(timezone.utc)

        # Create expired and valid messages
        expired_message = MagicMock(spec=ChatMessageModel)
        expired_message.id = str(uuid4())
        expired_message.role = "user"
        expired_message.content = "Old question"
        expired_message.created_at = now - timedelta(hours=25)
        expired_message.expires_at = now - timedelta(hours=1)  # Expired
        expired_message.query_type = "global"
        expired_message.has_safety_disclaimer = False
        expired_message.citations = []

        valid_message = MagicMock(spec=ChatMessageModel)
        valid_message.id = str(uuid4())
        valid_message.role = "user"
        valid_message.content = "New question"
        valid_message.created_at = now - timedelta(minutes=30)
        valid_message.expires_at = now + timedelta(hours=23)  # Valid
        valid_message.query_type = "global"
        valid_message.has_safety_disclaimer = False
        valid_message.citations = []

        mock_session_model = MagicMock(spec=ChatSessionModel)
        mock_session_model.id = session_id
        mock_session_model.is_active = True
        mock_session_model.messages = [expired_message, valid_message]

        async def mock_db():
            mock_db_session = AsyncMock()
            mock_db_session.get = AsyncMock(return_value=mock_session_model)
            yield mock_db_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.get(f"/sessions/{session_id}/messages")

            assert response.status_code == 200
            data = response.json()
            # Should only return valid (non-expired) message
            assert len(data["messages"]) == 1
            assert data["messages"][0]["content"] == "New question"
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.integration
    def test_returns_404_for_unknown_session(self, mock_env) -> None:
        """GET /sessions/{id}/messages should return 404 if session not found."""
        from main import app
        from core.database import get_async_session

        unknown_id = str(uuid4())

        async def mock_db():
            mock_db_session = AsyncMock()
            mock_db_session.get = AsyncMock(return_value=None)
            yield mock_db_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.get(f"/sessions/{unknown_id}/messages")

            assert response.status_code == 404
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.integration
    def test_supports_pagination(self, mock_env) -> None:
        """GET /sessions/{id}/messages should support pagination."""
        from main import app
        from core.database import get_async_session
        from models.database import ChatSessionModel, ChatMessageModel

        session_id = str(uuid4())
        now = datetime.now(timezone.utc)

        # Create multiple messages
        messages = []
        for i in range(15):
            msg = MagicMock(spec=ChatMessageModel)
            msg.id = str(uuid4())
            msg.role = "user" if i % 2 == 0 else "assistant"
            msg.content = f"Message {i}"
            msg.created_at = now - timedelta(minutes=15-i)
            msg.expires_at = now + timedelta(hours=24)
            msg.query_type = "global"
            msg.has_safety_disclaimer = False
            msg.citations = []
            messages.append(msg)

        mock_session_model = MagicMock(spec=ChatSessionModel)
        mock_session_model.id = session_id
        mock_session_model.is_active = True
        mock_session_model.messages = messages

        async def mock_db():
            mock_db_session = AsyncMock()
            mock_db_session.get = AsyncMock(return_value=mock_session_model)
            yield mock_db_session

        app.dependency_overrides[get_async_session] = mock_db

        try:
            with TestClient(app) as client:
                response = client.get(
                    f"/sessions/{session_id}/messages",
                    params={"limit": 10},
                )

            assert response.status_code == 200
            data = response.json()
            assert len(data["messages"]) == 10
            assert data["has_more"] is True
            assert data["next_cursor"] is not None
        finally:
            app.dependency_overrides.clear()
