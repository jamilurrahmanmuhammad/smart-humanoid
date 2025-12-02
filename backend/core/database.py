"""Async database session factory.

Configures SQLAlchemy async engine and session for PostgreSQL.
Uses asyncpg driver for async operations.
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine as sa_create_async_engine,
)

from core.config import get_settings

# Module-level engine and session factory (initialized lazily)
_engine: AsyncEngine | None = None
_async_session_factory: async_sessionmaker[AsyncSession] | None = None


def create_async_engine() -> AsyncEngine:
    """Create async SQLAlchemy engine from settings.

    Returns:
        AsyncEngine configured for asyncpg PostgreSQL driver.
    """
    global _engine

    if _engine is None:
        settings = get_settings()
        database_url = settings.database_url.get_secret_value()

        _engine = sa_create_async_engine(
            database_url,
            echo=settings.debug,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )

    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get or create the async session factory.

    Returns:
        async_sessionmaker configured for the application.
    """
    global _async_session_factory

    if _async_session_factory is None:
        engine = create_async_engine()
        _async_session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    return _async_session_factory


# Export for tests
AsyncSessionFactory = async_sessionmaker[AsyncSession]


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides an async database session.

    Usage in FastAPI:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_async_session)):
            ...

    Yields:
        AsyncSession that is automatically closed after the request.
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Type alias for dependency injection
DBSession = Annotated[AsyncSession, Depends(get_async_session)]


async def close_db_connection() -> None:
    """Close database connection pool.

    Call this on application shutdown.
    """
    global _engine, _async_session_factory

    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _async_session_factory = None
