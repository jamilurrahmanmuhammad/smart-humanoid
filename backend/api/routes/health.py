"""Health check endpoints for monitoring and load balancers."""

from datetime import datetime, timezone

from fastapi import APIRouter

from models.schemas import HealthResponse
from core.readiness import check_readiness
from core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint for load balancers and monitoring.

    Returns basic health status without checking dependencies.
    """
    from main import __version__

    return HealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/debug/config")
async def debug_config():
    """Debug endpoint to see current config values."""
    settings = get_settings()
    return {
        "qdrant_url": settings.qdrant_url,
        "qdrant_collection_name": settings.qdrant_collection_name,
        "rag_similarity_threshold": settings.rag_similarity_threshold,
        "openai_embedding_model": settings.openai_embedding_model,
    }


@router.get("/debug/vector-search")
async def debug_vector_search():
    """Debug endpoint to test vector search directly."""
    from services.embedding import EmbeddingService
    from services.vector_store import VectorStoreClient

    settings = get_settings()

    # Test embedding
    embed_service = EmbeddingService()
    query_vector = await embed_service.embed("What is ROS 2?")

    # Test vector store directly
    vector_store = VectorStoreClient()
    chunks = await vector_store.search(
        query_vector=query_vector,
        limit=5,
    )

    return {
        "query_vector_length": len(query_vector),
        "query_vector_first_5": query_vector[:5],
        "collection_name": settings.qdrant_collection_name,
        "qdrant_url": settings.qdrant_url,
        "results_count": len(chunks),
        "results": [
            {
                "id": chunk.id,
                "heading": chunk.heading,
                "score": chunk.relevance_score,
                "text_preview": chunk.text[:100] if chunk.text else "",
            }
            for chunk in chunks
        ],
    }


@router.get("/debug/rag-pipeline")
async def debug_rag_pipeline():
    """Debug endpoint to test RAG pipeline directly."""
    from services.rag import RAGPipeline

    settings = get_settings()

    # Test RAGPipeline directly (same as chat endpoint does)
    pipeline = RAGPipeline()
    result = await pipeline.query(
        message="What is ROS 2?",
        filters=None,
    )

    return {
        "is_out_of_scope": result.is_out_of_scope,
        "context_length": len(result.context),
        "context_preview": result.context[:500] if result.context else "",
        "citations_count": len(result.citations),
        "citations": [
            {
                "chapter": c.chapter,
                "heading": c.heading,
                "relevance_score": c.relevance_score,
            }
            for c in result.citations
        ],
    }


@router.get("/ready", response_model=HealthResponse)
async def readiness_check() -> HealthResponse:
    """Readiness check - verifies all dependencies are available.

    FR-ENV-003: Feature MUST be marked as incomplete/non-operational until:
    (a) .env file exists with real credential values (not placeholders), and
    (b) the connectivity sanity-check passes for all external services.

    Checks:
    - Environment configuration validity
    - OpenAI API connectivity
    - Vector store (Qdrant) connectivity
    - Database (PostgreSQL) connectivity

    Returns:
        HealthResponse with status and dependency info.
    """
    from main import __version__

    result = await check_readiness()

    dependencies = {}

    # Add environment status
    dependencies["env_config"] = "valid" if result.env_valid else "invalid"

    # Add service statuses from connectivity report
    if result.connectivity_report:
        dependencies["openai"] = (
            "healthy" if result.connectivity_report.openai.healthy else "unhealthy"
        )
        dependencies["qdrant"] = (
            "healthy" if result.connectivity_report.qdrant.healthy else "unhealthy"
        )
        dependencies["database"] = (
            "healthy" if result.connectivity_report.database.healthy else "unhealthy"
        )
    else:
        # If no connectivity report, services weren't checked (env invalid)
        dependencies["openai"] = "unchecked"
        dependencies["qdrant"] = "unchecked"
        dependencies["database"] = "unchecked"

    # Determine overall status
    if result.ready:
        status = "healthy"
    elif result.env_valid:
        status = "degraded"  # Env valid but services unhealthy
    else:
        status = "unhealthy"  # Env invalid

    return HealthResponse(
        status=status,
        version=__version__,
        dependencies=dependencies,
        timestamp=datetime.now(timezone.utc),
    )
