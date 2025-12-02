#!/usr/bin/env python
"""Check vector dimensions in Qdrant."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from qdrant_client import QdrantClient
from core.config import get_settings

settings = get_settings()
client = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key.get_secret_value(),
)

# Get collection info
collection = client.get_collection(settings.qdrant_collection_name)
print(f"Collection: {settings.qdrant_collection_name}")
print(f"Points count: {collection.points_count}")
print(f"Vectors config: {collection.config.params.vectors}")

# Scroll to get a sample point
sample = client.scroll(
    collection_name=settings.qdrant_collection_name,
    limit=1,
    with_vectors=True,
)
if sample[0]:
    point = sample[0][0]
    print(f"Sample vector dimension: {len(point.vector)}")
    print(f"Sample point ID: {point.id}")
    print(f"Sample vector first 5: {point.vector[:5]}")
