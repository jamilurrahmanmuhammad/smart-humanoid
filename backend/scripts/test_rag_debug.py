#!/usr/bin/env python
"""Debug RAG pipeline with verbose output."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from dotenv import load_dotenv
load_dotenv()

from services.embedding import EmbeddingService
from services.vector_store import VectorStoreClient
from services.rag import RAGPipeline
from core.config import get_settings


async def test():
    settings = get_settings()
    print(f"=== Configuration ===")
    print(f"rag_similarity_threshold: {settings.rag_similarity_threshold}")
    print()

    # Test embedding service
    print("=== Testing Embedding Service ===")
    embed_service = EmbeddingService()
    query_vector = await embed_service.embed("What is ROS 2?")
    print(f"Query vector dimension: {len(query_vector)}")
    print()

    # Test vector store directly
    print("=== Testing Vector Store ===")
    vector_store = VectorStoreClient()
    print(f"Vector store collection: {vector_store.collection_name}")
    print(f"Vector store threshold: {vector_store._similarity_threshold}")

    chunks = await vector_store.search(
        query_vector=query_vector,
        limit=5,
    )
    print(f"Chunks returned from vector store: {len(chunks)}")
    if chunks:
        print("Top chunk:")
        print(f"  Score: {chunks[0].relevance_score:.4f}")
        print(f"  Heading: {chunks[0].heading}")
    print()

    # Test RAG pipeline
    print("=== Testing RAG Pipeline ===")
    pipeline = RAGPipeline()
    print(f"RAG RELEVANCE_THRESHOLD: {pipeline.RELEVANCE_THRESHOLD}")

    result = await pipeline.query("What is ROS 2?")

    print(f"is_out_of_scope: {result.is_out_of_scope}")
    print(f"context length: {len(result.context)}")
    print(f"citations count: {len(result.citations)}")


if __name__ == "__main__":
    asyncio.run(test())
