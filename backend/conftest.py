"""Pytest configuration and shared fixtures for RAG Chatbot tests."""

import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# Will be imported once main.py is created
# from main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create async HTTP client for testing API endpoints."""
    # Placeholder until main.py app is available
    # transport = ASGITransport(app=app)
    # async with AsyncClient(transport=transport, base_url="http://test") as client:
    #     yield client
    yield None  # type: ignore


@pytest.fixture
def sample_chat_request() -> dict[str, Any]:
    """Sample chat request payload for tests."""
    return {
        "message": "What is ROS 2?",
        "persona": "Explorer",
        "query_type": "global",
    }


@pytest.fixture
def sample_session_data() -> dict[str, Any]:
    """Sample session data for tests."""
    return {
        "id": "test-session-123",
        "persona": "Explorer",
        "current_chapter": 1,
        "is_active": True,
    }


@pytest.fixture
def sample_citation() -> dict[str, Any]:
    """Sample citation data for tests."""
    return {
        "chapter": 1,
        "section": "1.2.1",
        "heading": "Introduction to ROS 2",
        "quote": "ROS 2 is the next generation Robot Operating System...",
        "link": "/module-1/chapter-1#introduction-to-ros-2",
        "relevance_score": 0.95,
    }
