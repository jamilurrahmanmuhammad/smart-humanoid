# Research: RAG Chatbot Assistant

**Feature**: 008-rag-chatbot-assistant
**Date**: 2025-12-02
**Status**: Complete

---

## Executive Summary

This document captures research findings for implementing a RAG-powered chatbot for the Smart Humanoid textbook. All technology choices align with Constitution Sections X-XI (Technology Platform) and support TDD-first development.

---

## 1. Backend Framework: FastAPI

### Decision
Use **FastAPI** as the backend framework for API layer and business logic.

### Rationale
- Constitution Section XI mandates FastAPI for the Intelligent Assistant backend
- Native async/await support critical for non-blocking RAG pipeline
- Built-in OpenAPI documentation generation
- WebSocket support for streaming chat responses
- Pydantic integration for request/response validation

### Key Patterns (from Context7)

```python
# WebSocket endpoint for streaming chat
@app.websocket("/ws/chat/{session_id}")
async def chat_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_json()
            # Process RAG pipeline, stream response
            await websocket.send_json({"response": "...", "citations": [...]})
    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")

# StreamingResponse for SSE alternative
from fastapi.responses import StreamingResponse
async def generate_response():
    async for chunk in rag_pipeline.stream():
        yield f"data: {chunk}\n\n"
```

### Alternatives Considered
| Alternative | Why Rejected |
|-------------|--------------|
| Flask | No native async, would require ASGI wrapper |
| Django | Heavier framework, overkill for API-only service |
| Starlette | FastAPI built on it; FastAPI adds validation layer |

---

## 2. AI Integration: OpenAI Agents SDK

### Decision
Use **OpenAI Agents SDK** (`openai-agents-python`) for LLM orchestration and tool management.

### Rationale
- Constitution Section XI specifies OpenAI Agents SDK for conversational capabilities
- Built-in tool orchestration for RAG retrieval functions
- Supports streaming responses
- Handoff patterns for future multi-agent expansion
- Tracing/debugging capabilities built-in

### Key Patterns (from Context7)

```python
from agents import Agent, Runner, function_tool

@function_tool
async def search_book_content(query: str, chapter: str | None = None) -> str:
    """Search the textbook for relevant content.

    Args:
        query: The search query
        chapter: Optional chapter to scope search
    """
    # Vector search via Qdrant
    results = await qdrant_client.query_points(...)
    return format_citations(results)

agent = Agent(
    name="Textbook Assistant",
    instructions="""You are a helpful assistant for the Physical AI textbook.
    Always ground answers in book content using search_book_content.
    Include citations in format: Chapter X, Section Y: 'quote'
    If content not found, say "I don't have information about this in the book."
    """,
    tools=[search_book_content],
    model="gpt-4o"
)

# Run with persona context
result = await Runner.run(
    agent,
    input=user_message,
    context={"persona": "Explorer", "current_chapter": 2}
)
```

### Alternatives Considered
| Alternative | Why Rejected |
|-------------|--------------|
| LangChain | More complex, Constitution specifies OpenAI SDK |
| Raw OpenAI API | Loses tool orchestration benefits |
| Anthropic SDK | Constitution mandates OpenAI integration |

---

## 3. Vector Database: Qdrant Cloud

### Decision
Use **Qdrant Cloud** (Free Tier) for vector storage and semantic search.

### Rationale
- Constitution Section XI mandates Qdrant Cloud for semantic search
- Free tier sufficient for textbook content (~100k chunks estimated)
- Native filtering for persona/chapter-scoped queries
- Python client with async support

### Key Patterns (from Context7)

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter, FieldCondition, MatchValue

# Collection setup
client.create_collection(
    collection_name="textbook_chunks",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Search with chapter filter (for page-scoped queries)
hits = client.query_points(
    collection_name="textbook_chunks",
    query=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="chapter", match=MatchValue(value=2)),
            FieldCondition(key="persona", match=MatchValue(value="Explorer"))
        ]
    ),
    limit=5
)
```

### Vector Metadata Schema
```python
{
    "id": "chunk_uuid",
    "vector": [0.123, ...],  # 1536 dimensions (text-embedding-3-small)
    "payload": {
        "module_id": 1,
        "chapter_id": 2,
        "section_id": "2.3",
        "persona": "Explorer",  # Explorer | Builder | Engineer
        "heading": "ROS 2 Nodes",
        "text": "A node is a process that...",
        "path": "/docs/module-1/chapter-2-ros2-architecture-explorer"
    }
}
```

### Alternatives Considered
| Alternative | Why Rejected |
|-------------|--------------|
| Pinecone | Not specified in Constitution |
| Weaviate | Free tier limitations |
| pgvector | Adds complexity to Neon setup |

---

## 4. Embeddings: text-embedding-3-small

### Decision
Use **text-embedding-3-small** for content vectorization.

### Rationale
- Constitution Section XI specifies this model
- 1536 dimensions, good balance of quality/cost
- Fast enough for real-time query embedding

### Key Patterns (from Context7)

```python
from openai import OpenAI

client = OpenAI()

# Single query embedding
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=user_query,
)
query_embedding = response.data[0].embedding

# Batch embedding for content indexing
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=["chunk1 text", "chunk2 text", "chunk3 text"],
)
embeddings = [item.embedding for item in response.data]
```

---

## 5. Relational Database: Neon Serverless Postgres

### Decision
Use **Neon Serverless Postgres** with **SQLAlchemy 2.0 async** for session/metadata storage.

### Rationale
- Constitution Section XI mandates Neon for user data and history
- Serverless = no connection management overhead
- SQLAlchemy 2.0 async aligns with FastAPI async patterns

### Key Patterns (from Context7)

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Engine setup for Neon
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@ep-xxx.region.aws.neon.tech/dbname",
    echo=True
)

async_session = async_sessionmaker(engine, expire_on_commit=False)

# Session context manager
async with async_session.begin() as session:
    session.add(chat_message)
    # Auto-commits on exit
```

### Alternatives Considered
| Alternative | Why Rejected |
|-------------|--------------|
| Supabase | Constitution specifies Neon |
| PlanetScale | MySQL, Constitution specifies Postgres |
| Raw asyncpg | Loses ORM benefits for complex queries |

---

## 6. Data Models: Pydantic

### Decision
Use **Pydantic v2** for all request/response validation and data models.

### Rationale
- Native FastAPI integration
- Type-safe serialization/deserialization
- Automatic OpenAPI schema generation
- ConfigDict for strict validation modes

### Key Patterns (from Context7)

```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum

class PersonaType(str, Enum):
    EXPLORER = "Explorer"
    BUILDER = "Builder"
    ENGINEER = "Engineer"

class QueryType(str, Enum):
    GLOBAL = "global"
    PAGE_SCOPED = "page"
    SELECTION_SCOPED = "selection"

class ChatMessage(BaseModel):
    model_config = ConfigDict(
        strict=True,
        str_strip_whitespace=True
    )

    id: str = Field(description="Unique message ID")
    session_id: str
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=10000)
    timestamp: datetime
    query_type: QueryType
    citations: list[Citation] = []
    expires_at: datetime  # 24h from creation per FR-027

class Citation(BaseModel):
    chapter: int
    section: str
    quote: str = Field(max_length=500)
    link: str
```

---

## 7. Testing Strategy: TDD with pytest

### Decision
Use **pytest** with **pytest-asyncio** for TDD development.

### Rationale
- User explicitly requested TDD approach
- pytest-asyncio for testing async endpoints
- httpx for async HTTP client testing
- Factory pattern for test data

### Test Structure
```
tests/
├── unit/
│   ├── test_rag_pipeline.py      # RAG retrieval logic
│   ├── test_persona_adapter.py   # Persona response adaptation
│   └── test_safety_guardrails.py # Safety filter tests
├── integration/
│   ├── test_chat_api.py          # API endpoint tests
│   └── test_vector_search.py     # Qdrant integration
└── contract/
    └── test_openapi_schema.py    # Contract validation
```

### Key Testing Patterns
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_chat_returns_citation():
    """RED: Chat response must include at least one citation (FR-004)"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/chat", json={
            "message": "What is embodied intelligence?",
            "persona": "Explorer"
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data["citations"]) >= 1
        assert "chapter" in data["citations"][0]
```

---

## 8. Streaming Architecture

### Decision
Use **WebSocket** for primary chat interface with **SSE fallback**.

### Rationale
- WebSocket enables bidirectional communication for chat
- SSE fallback for environments blocking WebSocket
- Aligns with NFR-001 (5-second first token latency)

### Implementation Pattern
```python
# Primary: WebSocket streaming
@app.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    async for chunk in agent.stream(message):
        await websocket.send_json({"type": "chunk", "content": chunk})
    await websocket.send_json({"type": "done", "citations": citations})

# Fallback: SSE streaming
@app.get("/api/chat/stream")
async def chat_sse(message: str):
    async def generate():
        async for chunk in agent.stream(message):
            yield f"data: {json.dumps({'content': chunk})}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

---

## 9. Message-Based Retention Policy

### Decision
Implement **per-message TTL** with 24-hour expiration post-session.

### Rationale
- User clarification specified message-based (not conversation-based) retention
- Each message tracks its own `expires_at` timestamp
- Background job purges expired messages

### Implementation Pattern
```python
# Message creation with TTL
message = ChatMessage(
    id=str(uuid4()),
    session_id=session_id,
    content=content,
    timestamp=datetime.utcnow(),
    expires_at=datetime.utcnow() + timedelta(hours=24)
)

# Background purge job (runs hourly)
async def purge_expired_messages():
    async with async_session() as session:
        await session.execute(
            delete(ChatMessageModel).where(
                ChatMessageModel.expires_at < datetime.utcnow()
            )
        )
        await session.commit()
```

---

## 10. Safety Guardrails Implementation

### Decision
Implement **multi-layer safety** aligned with Constitution Sections XXIV-XXVII.

### Rationale
- Physical robotics content requires safety disclaimers
- Cannot provide step-by-step instructions for dangerous operations
- Must distinguish conceptual vs. hardware-ready guidance

### Implementation Pattern
```python
SAFETY_KEYWORDS = [
    "rewire", "bypass", "override", "disable safety",
    "motor control", "actuator", "voltage", "current"
]

SAFETY_DISCLAIMER = """
⚠️ **Safety Notice**: This involves physical hardware operations.
- Always consult official equipment manuals
- Work with qualified supervision for hands-on tasks
- This explanation is for conceptual understanding only
"""

@function_tool
async def search_book_content(query: str) -> str:
    results = await vector_search(query)

    # Check if query involves physical operations
    if any(kw in query.lower() for kw in SAFETY_KEYWORDS):
        return format_with_safety_disclaimer(results)

    return format_citations(results)
```

---

## 11. Persona Adaptation Strategy

### Decision
Adapt responses via **system prompt injection** based on persona type.

### Rationale
- Constitution Section XIII requires three personas
- Same RAG results, different explanation styles
- No separate model fine-tuning required

### Implementation Pattern
```python
PERSONA_PROMPTS = {
    "Explorer": """
        Adapt your response for a software developer new to robotics.
        Use software analogies (processes, threads, message queues).
        Avoid hardware-specific jargon. Focus on simulation concepts.
    """,
    "Builder": """
        Adapt for a maker with Arduino/Raspberry Pi experience.
        Use practical, hands-on examples. Moderate technical depth.
        Reference common maker tools and platforms.
    """,
    "Engineer": """
        Adapt for industrial robotics professionals.
        Full technical depth. Real-world hardware considerations.
        Include performance metrics and trade-offs.
    """
}

def build_agent_instructions(persona: str) -> str:
    base = "You are a textbook assistant..."
    return base + PERSONA_PROMPTS.get(persona, "")
```

---

## 12. Content Chunking Strategy

### Decision
Use **semantic chunking** with 512-token chunks and 64-token overlap.

### Rationale
- Balances context preservation with retrieval precision
- 512 tokens fits well within embedding model context
- Overlap prevents losing context at chunk boundaries

### Chunking Metadata
```python
chunk = {
    "text": "chunk content...",
    "metadata": {
        "module_id": 1,
        "chapter_id": 2,
        "section_id": "2.3.1",
        "heading": "Understanding ROS 2 Nodes",
        "persona": "Explorer",
        "chunk_index": 5,
        "path": "/docs/module-1/chapter-2-ros2-architecture-explorer#nodes",
        "language": "en"
    }
}
```

---

## Unresolved Items

None - all technical decisions resolved.

---

## References

1. FastAPI Documentation - WebSocket endpoints, StreamingResponse
2. OpenAI Agents SDK - Tool definition, Runner patterns
3. Qdrant Client - Vector search with filters
4. SQLAlchemy 2.0 - Async session management
5. Pydantic v2 - Model validation, ConfigDict
6. Constitution Sections X-XI, XIII, XVIII-XX, XXIV-XXVII
