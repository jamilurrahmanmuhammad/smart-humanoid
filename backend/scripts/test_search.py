#!/usr/bin/env python
"""Test vector search scores to debug threshold issues."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from dotenv import load_dotenv
load_dotenv()

from services.embedding import EmbeddingService
from qdrant_client import QdrantClient
from core.config import get_settings


async def test():
    settings = get_settings()

    # Generate embedding for test query
    embed_service = EmbeddingService()
    query_vector = await embed_service.embed("What is ROS 2?")

    # Search directly in Qdrant without threshold filtering
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key.get_secret_value(),
    )

    results = client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_vector,
        limit=5,
        with_payload=True,
    ).points

    print(f"Configured similarity threshold: {settings.rag_similarity_threshold}")
    print()
    print("Top 5 results with scores:")
    for i, point in enumerate(results):
        heading = point.payload.get("heading", "Unknown")
        score = point.score
        chapter = point.payload.get("chapter_id")
        print(f"{i+1}. Score: {score:.4f}, Chapter {chapter}: {heading}")


if __name__ == "__main__":
    asyncio.run(test())
