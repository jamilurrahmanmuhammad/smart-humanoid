"""Dependency injection for API routes."""

from typing import Annotated, AsyncGenerator

from fastapi import Depends

# TODO: Import database session and services once implemented
# from core.database import AsyncSession, get_async_session
# from services.rag import RAGPipeline
# from services.vector_store import VectorStore


async def get_db_session() -> AsyncGenerator[None, None]:
    """Get async database session."""
    # TODO: Implement once database is configured (T006-T007)
    yield None


# Type aliases for dependency injection
# DBSession = Annotated[AsyncSession, Depends(get_db_session)]
