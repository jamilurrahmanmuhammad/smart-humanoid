#!/usr/bin/env python
"""Test Qdrant directly to debug empty results."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from qdrant_client import QdrantClient
from core.config import get_settings
from services.embedding import EmbeddingService
import asyncio


async def test():
    settings = get_settings()

    print(f"=== Configuration ===")
    print(f"Collection: {settings.qdrant_collection_name}")
    print(f"Qdrant URL: {settings.qdrant_url}")
    print()

    # Create client
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key.get_secret_value(),
    )

    # Check collection exists and has points
    collection = client.get_collection(settings.qdrant_collection_name)
    print(f"Collection points_count: {collection.points_count}")
    print()

    # Generate embedding
    embed_service = EmbeddingService()
    query_vector = await embed_service.embed("What is ROS 2?")
    print(f"Query vector length: {len(query_vector)}")
    print()

    # Query directly
    print("=== Direct query_points ===")
    response = client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_vector,
        limit=5,
        with_payload=True,
    )
    print(f"Response type: {type(response)}")
    print(f"Response.points type: {type(response.points)}")
    print(f"Response.points length: {len(response.points)}")

    if response.points:
        for i, point in enumerate(response.points):
            print(f"  Point {i}: score={point.score}, heading={point.payload.get('heading', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(test())
