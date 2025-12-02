#!/usr/bin/env python
"""Content indexing script for RAG chatbot.

Indexes textbook markdown files into Qdrant vector database.
Chunks content, generates embeddings, and stores with metadata.

Usage:
    python scripts/index_content.py
"""

import re
import sys
import uuid
from pathlib import Path
from dataclasses import dataclass

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

import yaml
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from core.config import get_settings


@dataclass
class ContentChunk:
    """A chunk of content with metadata."""
    text: str
    module_id: int
    chapter_id: int
    section_id: str
    heading: str
    persona: str
    source_path: str


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter dict, remaining content)
    """
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        return frontmatter or {}, body
    except yaml.YAMLError:
        return {}, content


def extract_module_chapter(filepath: Path) -> tuple[int, int]:
    """Extract module and chapter IDs from filepath.

    Example: module-1-robotic-nervous-system/chapter-2-ros2-architecture-explorer.md
    Returns: (1, 2)
    """
    path_str = str(filepath)

    # Extract module ID
    module_match = re.search(r'module-(\d+)', path_str)
    module_id = int(module_match.group(1)) if module_match else 0

    # Extract chapter ID
    chapter_match = re.search(r'chapter-(\d+)', path_str)
    chapter_id = int(chapter_match.group(1)) if chapter_match else 0

    return module_id, chapter_id


def extract_persona(filepath: Path, frontmatter: dict) -> str:
    """Extract persona from filepath or frontmatter.

    Looks for 'explorer', 'builder', or 'engineer' in filename or learningPath.
    """
    # Check frontmatter first
    if 'learningPath' in frontmatter:
        return frontmatter['learningPath'].lower()

    # Check filename
    filename = filepath.stem.lower()
    for persona in ['explorer', 'builder', 'engineer']:
        if persona in filename:
            return persona

    return 'explorer'  # default


def chunk_by_sections(content: str, max_chunk_size: int = 1500) -> list[dict]:
    """Split content into chunks by markdown sections.

    Tries to keep sections together, but splits large sections.

    Returns:
        List of dicts with 'text', 'heading', 'section_id'
    """
    chunks = []

    # Split by headings (## or ###)
    section_pattern = r'^(#{2,3})\s+(.+)$'
    lines = content.split('\n')

    current_chunk = []
    current_heading = "Introduction"
    current_section = "intro"

    for line in lines:
        match = re.match(section_pattern, line)

        if match:
            # Save current chunk if it has content
            if current_chunk:
                chunk_text = '\n'.join(current_chunk).strip()
                if chunk_text and len(chunk_text) > 50:  # Skip tiny chunks
                    chunks.append({
                        'text': chunk_text,
                        'heading': current_heading,
                        'section_id': current_section,
                    })

            # Start new chunk
            level = len(match.group(1))
            current_heading = match.group(2).strip()
            # Create section ID from heading
            current_section = re.sub(r'[^\w\s-]', '', current_heading.lower())
            current_section = re.sub(r'[\s]+', '-', current_section)[:50]
            current_chunk = [line]
        else:
            current_chunk.append(line)

            # Check if chunk is too large
            chunk_text = '\n'.join(current_chunk)
            if len(chunk_text) > max_chunk_size:
                # Split at paragraph boundary
                paragraphs = chunk_text.split('\n\n')
                if len(paragraphs) > 1:
                    # Save first part
                    first_part = '\n\n'.join(paragraphs[:-1]).strip()
                    if first_part:
                        chunks.append({
                            'text': first_part,
                            'heading': current_heading,
                            'section_id': current_section,
                        })
                    # Continue with last paragraph
                    current_chunk = [paragraphs[-1]]

    # Don't forget the last chunk
    if current_chunk:
        chunk_text = '\n'.join(current_chunk).strip()
        if chunk_text and len(chunk_text) > 50:
            chunks.append({
                'text': chunk_text,
                'heading': current_heading,
                'section_id': current_section,
            })

    return chunks


def process_file(filepath: Path) -> list[ContentChunk]:
    """Process a markdown file into content chunks."""
    content = filepath.read_text(encoding='utf-8')

    # Extract frontmatter
    frontmatter, body = extract_frontmatter(content)

    # Extract metadata
    module_id, chapter_id = extract_module_chapter(filepath)
    persona = extract_persona(filepath, frontmatter)

    # Skip non-chapter files (index.md, intro.md)
    if chapter_id == 0:
        return []

    # Chunk content
    raw_chunks = chunk_by_sections(body)

    # Create ContentChunk objects
    chunks = []
    for raw in raw_chunks:
        chunks.append(ContentChunk(
            text=raw['text'],
            module_id=module_id,
            chapter_id=chapter_id,
            section_id=raw['section_id'],
            heading=raw['heading'],
            persona=persona,
            source_path=str(filepath.relative_to(filepath.parent.parent.parent)),
        ))

    return chunks


def generate_embeddings(texts: list[str], client: OpenAI, model: str) -> list[list[float]]:
    """Generate embeddings for a batch of texts."""
    response = client.embeddings.create(
        model=model,
        input=texts,
    )
    return [item.embedding for item in response.data]


def main() -> int:
    """Index textbook content into Qdrant."""
    settings = get_settings()

    print("=" * 60)
    print("Content Indexing for RAG Chatbot")
    print("=" * 60)
    print()

    # Find content files
    docs_path = Path(__file__).parent.parent.parent / "docs"
    if not docs_path.exists():
        print(f"❌ Docs directory not found: {docs_path}")
        return 1

    md_files = list(docs_path.glob("**/chapter-*.md"))
    print(f"Found {len(md_files)} chapter files to index")
    print()

    if not md_files:
        print("❌ No chapter files found!")
        return 1

    # Process all files into chunks
    print("Processing files into chunks...")
    all_chunks: list[ContentChunk] = []
    for filepath in md_files:
        chunks = process_file(filepath)
        all_chunks.extend(chunks)
        print(f"   {filepath.name}: {len(chunks)} chunks")

    print(f"\nTotal chunks: {len(all_chunks)}")
    print()

    if not all_chunks:
        print("❌ No chunks generated!")
        return 1

    # Initialize clients
    print("Connecting to OpenAI...")
    openai_client = OpenAI(api_key=settings.openai_api_key.get_secret_value())

    print("Connecting to Qdrant...")
    qdrant_client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key.get_secret_value(),
    )

    # Generate embeddings in batches
    print("\nGenerating embeddings...")
    batch_size = 100
    all_embeddings = []

    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        texts = [chunk.text for chunk in batch]

        embeddings = generate_embeddings(
            texts,
            openai_client,
            settings.openai_embedding_model,
        )
        all_embeddings.extend(embeddings)

        print(f"   Processed {min(i + batch_size, len(all_chunks))}/{len(all_chunks)} chunks")

    # Upload to Qdrant
    print("\nUploading to Qdrant...")
    points = []

    for i, (chunk, embedding) in enumerate(zip(all_chunks, all_embeddings)):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": chunk.text,
                "module_id": chunk.module_id,
                "chapter_id": chunk.chapter_id,
                "section_id": chunk.section_id,
                "heading": chunk.heading,
                "persona": chunk.persona,
                "source_path": chunk.source_path,
            },
        )
        points.append(point)

    # Upsert in batches
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        qdrant_client.upsert(
            collection_name=settings.qdrant_collection_name,
            points=batch,
        )
        print(f"   Uploaded {min(i + batch_size, len(points))}/{len(points)} points")

    # Verify
    collection_info = qdrant_client.get_collection(settings.qdrant_collection_name)
    print()
    print("=" * 60)
    print(f"✅ Indexing complete!")
    print(f"   Collection: {settings.qdrant_collection_name}")
    print(f"   Total points: {collection_info.points_count}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
