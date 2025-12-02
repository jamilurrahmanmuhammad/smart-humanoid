#!/usr/bin/env python
"""Test RAG pipeline directly to debug issues."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from dotenv import load_dotenv
load_dotenv()

from services.rag import RAGPipeline
from core.config import get_settings


async def test():
    settings = get_settings()
    print(f"Configured similarity threshold: {settings.rag_similarity_threshold}")
    print()

    # Run RAG pipeline
    pipeline = RAGPipeline()
    result = await pipeline.query("What is ROS 2?")

    print(f"is_out_of_scope: {result.is_out_of_scope}")
    print(f"context length: {len(result.context)}")
    print(f"citations count: {len(result.citations)}")
    print()

    if result.context:
        print("Context preview (first 500 chars):")
        print(result.context[:500])
    else:
        print("No context returned")


if __name__ == "__main__":
    asyncio.run(test())
