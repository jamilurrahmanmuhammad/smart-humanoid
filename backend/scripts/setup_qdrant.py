#!/usr/bin/env python
"""Qdrant collection setup script.

Creates and configures the textbook_chunks collection with proper
vector configuration and payload indexes.

Usage:
    python scripts/setup_qdrant.py
"""

import sys
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PayloadSchemaType

from core.config import get_settings


def main() -> int:
    """Set up Qdrant collection for textbook content."""
    settings = get_settings()

    print("=" * 60)
    print("Qdrant Collection Setup")
    print("=" * 60)
    print()

    # Connect to Qdrant
    print(f"Connecting to Qdrant at {settings.qdrant_url}...")
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key.get_secret_value(),
    )

    collection_name = settings.qdrant_collection_name
    print(f"Collection name: {collection_name}")
    print()

    # Check if collection exists
    collections = client.get_collections().collections
    existing_names = [c.name for c in collections]

    if collection_name in existing_names:
        print(f"⚠️  Collection '{collection_name}' already exists.")
        response = input("Delete and recreate? [y/N]: ").strip().lower()
        if response == 'y':
            print(f"Deleting collection '{collection_name}'...")
            client.delete_collection(collection_name)
        else:
            print("Keeping existing collection.")
            return 0

    # Create collection
    print(f"Creating collection '{collection_name}'...")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=1536,  # text-embedding-3-small dimensions
            distance=Distance.COSINE,
        ),
    )
    print("   ✅ Collection created")

    # Create payload indexes for efficient filtering
    print("Creating payload indexes...")

    # Index for chapter filtering (FR-003: page-scoped queries)
    client.create_payload_index(
        collection_name=collection_name,
        field_name="chapter_id",
        field_schema=PayloadSchemaType.INTEGER,
    )
    print("   ✅ chapter_id index created")

    # Index for module filtering
    client.create_payload_index(
        collection_name=collection_name,
        field_name="module_id",
        field_schema=PayloadSchemaType.INTEGER,
    )
    print("   ✅ module_id index created")

    # Index for persona filtering (FR-015: persona-aware responses)
    client.create_payload_index(
        collection_name=collection_name,
        field_name="persona",
        field_schema=PayloadSchemaType.KEYWORD,
    )
    print("   ✅ persona index created")

    # Index for section filtering
    client.create_payload_index(
        collection_name=collection_name,
        field_name="section_id",
        field_schema=PayloadSchemaType.KEYWORD,
    )
    print("   ✅ section_id index created")

    print()
    print("=" * 60)
    print(f"✅ Qdrant collection '{collection_name}' ready!")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
