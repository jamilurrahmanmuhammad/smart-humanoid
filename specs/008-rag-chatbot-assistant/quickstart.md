# Quickstart: RAG Chatbot Assistant

**Feature**: 008-rag-chatbot-assistant
**Date**: 2025-12-02

---

## Prerequisites

### Required Software
- Python 3.11+
- Node.js 18+ (for frontend integration)
- Docker (optional, for local Qdrant)

### Required Accounts/Services
- OpenAI API key (for embeddings and chat completions)
- Qdrant Cloud account (free tier) or local Qdrant instance
- Neon Serverless Postgres account

---

## 1. Environment Setup

### Clone and Install

```bash
# Clone repository
git clone https://github.com/jamilurrahmanmuhammad/smart-humanoid.git
cd smart-humanoid

# Create Python virtual environment
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt
```

### Service Account Setup

Before creating your `.env` file, you need accounts for three external services:

#### 1. OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign in or create an account
3. Navigate to **API Keys** in the sidebar
4. Click **Create new secret key**
5. Copy the key (starts with `sk-`)

#### 2. Qdrant Cloud (Free Tier)

1. Go to [cloud.qdrant.io](https://cloud.qdrant.io)
2. Sign up for a free account
3. Create a new **Free Cluster** (1GB storage, sufficient for textbook)
4. Once created, copy:
   - **Cluster URL**: `https://xxx-xxx.aws.cloud.qdrant.io:6333`
   - **API Key**: Generate from cluster settings

#### 3. Neon Serverless Postgres (Free Tier)

1. Go to [neon.tech](https://neon.tech)
2. Click **Sign Up** and create a free account
3. Create a new project:
   - **Project name**: `smart-humanoid` (or any name)
   - **Database name**: `chatbot` (or any name)
   - **Region**: Choose closest to you
4. Once created, go to **Dashboard → Connection Details**
5. Select **Connection string** tab
6. Copy the connection string (format: `postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname`)
7. **Important**: Modify the connection string for asyncpg:
   - Change `postgresql://` to `postgresql+asyncpg://`
   - Add `?sslmode=require` at the end

**Example transformation:**
```
Before: postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/chatbot
After:  postgresql+asyncpg://user:pass@ep-xxx.us-east-1.aws.neon.tech/chatbot?sslmode=require
```

### Environment Variables

Create `.env` file from template:

```bash
# From backend directory
cp .env.example .env
```

Edit `.env` with your real credentials (never commit this file):

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...  # Your real key

# Qdrant Configuration
QDRANT_URL=https://xxx-xxx.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=...  # Your real key
QDRANT_COLLECTION_NAME=textbook_chunks

# Neon PostgreSQL Configuration
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Application Settings
APP_ENV=development
LOG_LEVEL=DEBUG
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

### Connectivity Check

**BLOCKING**: Before proceeding, verify all services are reachable:

```bash
# Run connectivity sanity-check (FR-ENV-002)
python scripts/check_connectivity.py
```

Expected output if all services are configured correctly:
```
============================================================
RAG Chatbot Connectivity Check
============================================================

1. Validating environment configuration...
   ✅ Environment configuration valid

2. Checking service connectivity...

   ✅ OpenAI API: OpenAI API connected successfully (245ms)
   ✅ Qdrant Vector DB: Qdrant connected successfully (312ms)
   ✅ PostgreSQL Database: Database connected successfully (187ms)

============================================================
✅ All services healthy - Application ready!
```

If any service fails, fix the credentials in `.env` before continuing.

---

## 2. Database Setup

### Run Migrations

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Run migrations
alembic upgrade head
```

### Verify Database

```bash
# Check tables created
psql $DATABASE_URL -c "\dt"

# Expected output:
#  Schema |      Name       | Type  | Owner
# --------+-----------------+-------+-------
#  public | chat_sessions   | table | user
#  public | chat_messages   | table | user
#  public | citations       | table | user
#  public | analytics_events| table | user
```

---

## 3. Vector Store Setup

### Create Qdrant Collection

```python
# scripts/setup_qdrant.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(
    url="https://your-cluster.cloud.qdrant.io",
    api_key="your-api-key"
)

# Create collection for textbook content
client.create_collection(
    collection_name="textbook_chunks",
    vectors_config=VectorParams(
        size=1536,  # text-embedding-3-small dimensions
        distance=Distance.COSINE
    )
)

# Create payload indexes for filtering
client.create_payload_index(
    collection_name="textbook_chunks",
    field_name="chapter_id",
    field_schema="integer"
)

client.create_payload_index(
    collection_name="textbook_chunks",
    field_name="persona",
    field_schema="keyword"
)

print("Qdrant collection created successfully!")
```

Run setup:
```bash
python scripts/setup_qdrant.py
```

---

## 4. Index Book Content

### Content Indexing Script

```python
# scripts/index_content.py
import asyncio
from pathlib import Path
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import frontmatter
import uuid

openai_client = OpenAI()
qdrant_client = QdrantClient(url="...", api_key="...")

CHUNK_SIZE = 512  # tokens
CHUNK_OVERLAP = 64

async def index_chapter(filepath: Path):
    """Index a single chapter file."""
    post = frontmatter.load(filepath)

    # Extract metadata from frontmatter
    metadata = {
        "module_id": post.get("module", 1),
        "chapter_id": post.get("chapter", 1),
        "persona": post.get("persona", "Explorer"),
        "path": str(filepath).replace("docs/", "/docs/").replace(".md", "")
    }

    # Chunk content
    chunks = chunk_text(post.content, CHUNK_SIZE, CHUNK_OVERLAP)

    # Generate embeddings
    embeddings = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=[c["text"] for c in chunks]
    )

    # Upsert to Qdrant
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=emb.embedding,
            payload={
                **metadata,
                "text": chunks[i]["text"],
                "heading": chunks[i].get("heading", ""),
                "section_id": chunks[i].get("section", ""),
                "chunk_index": i
            }
        )
        for i, emb in enumerate(embeddings.data)
    ]

    qdrant_client.upsert(
        collection_name="textbook_chunks",
        points=points
    )

    print(f"Indexed {len(points)} chunks from {filepath}")

async def main():
    docs_path = Path("docs")
    chapter_files = list(docs_path.glob("**/chapter-*.md"))

    for filepath in chapter_files:
        await index_chapter(filepath)

    print(f"Indexing complete! Total files: {len(chapter_files)}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run indexing:
```bash
python scripts/index_content.py
```

---

## 5. Start Backend Server

### Run Development Server

```bash
# Start FastAPI server
uvicorn backend.main:app --reload --port 8000

# Server running at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Verify Health

```bash
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status":"healthy","timestamp":"2025-12-02T10:00:00Z","dependencies":{...}}
```

---

## 6. Test Chat Endpoint

### Send Test Message

```bash
# Create session and send message
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is embodied intelligence?",
    "persona": "Explorer"
  }'
```

### Expected Response

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "content": "Embodied intelligence refers to the capacity of an agent to interact with and learn from its physical environment...",
  "citations": [
    {
      "chapter": 1,
      "section": "1.2",
      "heading": "Understanding Embodied Intelligence",
      "quote": "Embodied intelligence is the capacity...",
      "link": "/docs/module-1/chapter-1-foundations-explorer#embodied-intelligence",
      "relevance_score": 0.92
    }
  ],
  "has_safety_disclaimer": false,
  "query_type": "global",
  "is_selection_scoped": false
}
```

---

## 7. Frontend Integration

### React Component Example

```tsx
// components/ChatWidget.tsx
import { useState, useEffect, useRef } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
}

interface Citation {
  chapter: number;
  section: string;
  quote: string;
  link: string;
}

export function ChatWidget() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const ws = new WebSocket(
      `ws://localhost:8000/api/v1/ws/chat/${sessionId || 'new'}`
    );

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);

      switch (msg.type) {
        case 'welcome':
          setSessionId(msg.data.session_id);
          break;
        case 'content':
          setMessages(prev => {
            const last = prev[prev.length - 1];
            if (last?.role === 'assistant') {
              return [
                ...prev.slice(0, -1),
                { ...last, content: last.content + msg.data.chunk }
              ];
            }
            return [...prev, { role: 'assistant', content: msg.data.chunk }];
          });
          break;
        case 'citation':
          setMessages(prev => {
            const last = prev[prev.length - 1];
            if (last?.role === 'assistant') {
              return [
                ...prev.slice(0, -1),
                {
                  ...last,
                  citations: [...(last.citations || []), msg.data]
                }
              ];
            }
            return prev;
          });
          break;
      }
    };

    wsRef.current = ws;
    return () => ws.close();
  }, [sessionId]);

  const sendMessage = () => {
    if (!input.trim() || !wsRef.current) return;

    setMessages(prev => [...prev, { role: 'user', content: input }]);

    wsRef.current.send(JSON.stringify({
      type: 'message',
      data: { content: input, query_type: 'global' }
    }));

    setInput('');
  };

  return (
    <div className="chat-widget">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <p>{msg.content}</p>
            {msg.citations && (
              <div className="citations">
                {msg.citations.map((c, j) => (
                  <a key={j} href={c.link}>
                    Ch {c.chapter}, {c.section}
                  </a>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        placeholder="Ask a question..."
      />
    </div>
  );
}
```

---

## 8. Run Tests (TDD)

### Run Test Suite

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/unit/ -v          # Unit tests
pytest tests/integration/ -v   # Integration tests
pytest tests/contract/ -v      # Contract tests

# Run with coverage
pytest tests/ --cov=backend --cov-report=html
```

### Example Test (RED phase)

```python
# tests/unit/test_rag_pipeline.py
import pytest
from backend.services.rag import RAGPipeline

@pytest.mark.asyncio
async def test_response_includes_citation():
    """FR-004: Every response MUST include citations."""
    pipeline = RAGPipeline()
    response = await pipeline.query("What is embodied intelligence?")

    assert response.citations is not None
    assert len(response.citations) >= 1
    assert response.citations[0].chapter is not None
    assert response.citations[0].quote is not None
```

---

## 9. Project Structure

```
smart-humanoid/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py      # Chat endpoints
│   │   │   ├── sessions.py  # Session endpoints
│   │   │   └── health.py    # Health check
│   │   └── deps.py          # Dependencies
│   ├── models/
│   │   ├── schemas.py       # Pydantic models
│   │   └── database.py      # SQLAlchemy models
│   ├── services/
│   │   ├── rag.py           # RAG pipeline
│   │   ├── agent.py         # OpenAI Agent
│   │   └── vector_store.py  # Qdrant client
│   └── core/
│       ├── config.py        # Settings
│       └── security.py      # Auth helpers
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── scripts/
│   ├── setup_qdrant.py
│   └── index_content.py
├── specs/008-rag-chatbot-assistant/
│   ├── spec.md
│   ├── plan.md
│   ├── research.md
│   ├── data-model.md
│   ├── quickstart.md
│   └── contracts/
│       ├── openapi.yaml
│       └── websocket.md
└── requirements.txt
```

---

## 10. Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Connection refused" to Qdrant | Check QDRANT_URL and API key |
| "Invalid API key" from OpenAI | Verify OPENAI_API_KEY in .env |
| Empty search results | Run index_content.py to populate vectors |
| "Session expired" error | Sessions are ephemeral; create new session |
| Slow responses (>5s) | Check network latency to Qdrant/OpenAI |

### Debug Mode

```bash
# Enable verbose logging
LOG_LEVEL=DEBUG uvicorn backend.main:app --reload
```

---

## Next Steps

1. **Run `/sp.tasks`** to generate implementation tasks
2. **Start TDD cycle**: Write failing tests first (RED)
3. **Implement features** to make tests pass (GREEN)
4. **Refactor** while keeping tests green
5. **Create PR** when feature is complete
