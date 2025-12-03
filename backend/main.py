"""FastAPI application entry point for RAG Chatbot Assistant."""

# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import chat, health, sessions

# Version info
__version__ = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup/shutdown events."""
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Startup: Log connectivity status
    logger.info("Starting RAG Chatbot Assistant...")

    try:
        from core.readiness import log_startup_status

        result = await log_startup_status()
        if not result.ready:
            logger.warning(
                "Application starting in degraded mode - some features may not work"
            )
    except Exception as e:
        logger.warning(f"Could not complete startup checks: {e}")

    # TODO: Initialize async database session factory
    # TODO: Initialize Qdrant client pool

    yield

    # Shutdown: Clean up resources
    logger.info("Shutting down RAG Chatbot Assistant...")
    # TODO: Close database connections
    # TODO: Close vector store connections


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Smart Humanoid RAG Chatbot",
        description="RAG-powered chatbot for the Smart Humanoid textbook",
        version=__version__,
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:8080"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add request timing middleware for observability (T120)
    from api.middleware import RequestTimingMiddleware
    app.add_middleware(RequestTimingMiddleware)

    # Register routes
    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(sessions.router)

    return app


# Create application instance
app = create_app()


def run() -> None:
    """Run the application with uvicorn."""
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    run()
