#!/usr/bin/env python
"""Test synchronous Qdrant calls in async context to match server behavior."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from dotenv import load_dotenv
load_dotenv()

from qdrant_client import QdrantClient
from openai import OpenAI
from core.config import get_settings


async def test_like_server():
    """Mimic what the server does exactly."""
    settings = get_settings()

    print(f"=== Config ===")
    print(f"Qdrant URL: {settings.qdrant_url}")
    print(f"Collection: {settings.qdrant_collection_name}")
    print()

    # Create clients just like the services do
    openai_client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
    qdrant_client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key.get_secret_value(),
        timeout=30,
    )

    # Generate embedding
    print("Generating embedding...")
    response = openai_client.embeddings.create(
        model=settings.openai_embedding_model,
        input="What is ROS 2?",
    )
    query_vector = response.data[0].embedding
    print(f"Query vector length: {len(query_vector)}")
    print(f"Query vector first 5: {query_vector[:5]}")
    print()

    # Query Qdrant exactly like VectorStoreClient does
    print("Querying Qdrant...")
    response = qdrant_client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_vector,
        limit=10,
        query_filter=None,
        with_payload=True,
    )
    results = response.points

    print(f"Results count: {len(results)}")
    if results:
        for i, p in enumerate(results[:3]):
            print(f"  Point {i}: score={p.score}, heading={p.payload.get('heading', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(test_like_server())
