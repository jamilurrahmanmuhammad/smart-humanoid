# Implementation Plan: RAG Chatbot Assistant

**Branch**: `008-rag-chatbot-assistant` | **Date**: 2025-12-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/008-rag-chatbot-assistant/spec.md`

---

## Summary

Implement a RAG-powered chatbot for the Smart Humanoid textbook that provides citation-grounded, persona-aware responses with safety guardrails. Uses TDD approach with FastAPI backend, OpenAI Agents SDK, Qdrant vector search, and Neon PostgreSQL.

**Key Capabilities:**
- Global, page-scoped, and selection-scoped queries
- Persona adaptation (Explorer/Builder/Engineer)
- Citation-grounded responses (max 5 citations)
- Safety disclaimers for physical robotics content
- Message-based 24-hour retention policy

---

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.109+, OpenAI Agents SDK, Qdrant Client, SQLAlchemy 2.0, Pydantic 2.x
**Storage**: Neon Serverless Postgres (sessions/metadata), Qdrant Cloud (vectors)
**Testing**: pytest, pytest-asyncio, httpx
**Target Platform**: Linux server (Docker containerized)
**Project Type**: Web application (backend API + frontend widget)
**Performance Goals**: <5s first token latency (NFR-001), 95% citation accuracy (SC-001)
**Constraints**: Max 5 citations per response (FR-009), 2000 char selection limit
**Scale/Scope**: ~100k content chunks, concurrent users TBD

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Section | Requirement | Status | Implementation |
|---------|-------------|--------|----------------|
| X-XI Technology Platform | FastAPI, Qdrant, Neon, OpenAI | PASS | All technologies aligned |
| XIII Adaptive Content | Three personas | PASS | Persona system prompt injection |
| XVIII Answer Grounding | Citations required | PASS | Vector search + citation extraction |
| XIX Multi-Source Citation | Max 5, link to source | PASS | Citation model with links |
| XX Context Stitching | Session continuity | PASS | Session/message persistence |
| XXIV-XXVII Safety | Guardrails for physical ops | PASS | Safety keyword detection + disclaimers |
| XXXIV Accessibility | WCAG 2.1 AA | PASS | Frontend widget requirements |

**Post-Design Re-Check**: All gates pass. No violations requiring justification.

---

## Project Structure

### Documentation (this feature)

```text
specs/008-rag-chatbot-assistant/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0: Technology research
├── data-model.md        # Phase 1: Entity definitions
├── quickstart.md        # Phase 1: Developer setup guide
├── contracts/
│   ├── openapi.yaml     # REST API contract
│   └── websocket.md     # WebSocket protocol
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── main.py                    # FastAPI application entry
├── api/
│   ├── routes/
│   │   ├── chat.py           # POST /chat, WebSocket /ws/chat
│   │   ├── sessions.py       # Session CRUD
│   │   └── health.py         # Health check endpoint
│   └── deps.py               # Dependency injection
├── models/
│   ├── schemas.py            # Pydantic request/response models
│   └── database.py           # SQLAlchemy ORM models
├── services/
│   ├── rag.py                # RAG pipeline orchestration
│   ├── agent.py              # OpenAI Agent configuration
│   ├── vector_store.py       # Qdrant client wrapper
│   ├── persona.py            # Persona prompt adaptation
│   └── safety.py             # Safety guardrail checks
├── core/
│   ├── config.py             # Pydantic settings
│   └── database.py           # Async session factory
└── alembic/                  # Database migrations

frontend/
└── components/
    └── ChatWidget.tsx        # React chat widget (Docusaurus integration)

tests/
├── unit/
│   ├── test_rag_pipeline.py
│   ├── test_persona_adapter.py
│   ├── test_safety_guardrails.py
│   └── test_citation_extractor.py
├── integration/
│   ├── test_chat_api.py
│   ├── test_websocket.py
│   └── test_vector_search.py
└── contract/
    └── test_openapi_schema.py

scripts/
├── setup_qdrant.py           # Qdrant collection setup
└── index_content.py          # Content indexing script
```

**Structure Decision**: Web application pattern with FastAPI backend and React frontend widget. Backend is API-only; frontend integrates with existing Docusaurus site.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Docusaurus Frontend                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Chat Widget │  │ Selection   │  │ Page Context Provider   │  │
│  │ (Floating)  │  │ Trigger     │  │ (Chapter/Persona)       │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
└─────────┼────────────────┼─────────────────────┼────────────────┘
          │ WebSocket/SSE  │                     │
          ▼                ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    API Layer                                 ││
│  │  /chat  /chat/stream  /ws/chat/{session_id}  /sessions      ││
│  └──────────────────────────┬──────────────────────────────────┘│
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────────┐│
│  │                   RAG Pipeline                               ││
│  │  ┌─────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ ││
│  │  │ Query   │─▶│ Vector      │─▶│ Context     │─▶│ Agent   │ ││
│  │  │ Parser  │  │ Search      │  │ Builder     │  │ Runner  │ ││
│  │  └─────────┘  └─────────────┘  └─────────────┘  └─────────┘ ││
│  │       │              │                │              │       ││
│  │       │              │                │              │       ││
│  │  ┌────▼────┐   ┌─────▼─────┐   ┌──────▼──────┐  ┌────▼────┐ ││
│  │  │ Persona │   │ Safety    │   │ Citation    │  │ Stream  │ ││
│  │  │ Adapter │   │ Filter    │   │ Extractor   │  │ Handler │ ││
│  │  └─────────┘   └───────────┘   └─────────────┘  └─────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
          │                             │
          ▼                             ▼
┌─────────────────┐          ┌─────────────────────┐
│  Qdrant Cloud   │          │  Neon PostgreSQL    │
│  (Vectors)      │          │  (Sessions/Meta)    │
│                 │          │                     │
│  textbook_chunks│          │  chat_sessions      │
│  - module_id    │          │  chat_messages      │
│  - chapter_id   │          │  citations          │
│  - persona      │          │  analytics_events   │
│  - text         │          │                     │
└─────────────────┘          └─────────────────────┘
          │
          ▼
┌─────────────────┐
│  OpenAI API     │
│  - Embeddings   │
│  - Chat         │
│  - Agents SDK   │
└─────────────────┘
```

---

## Implementation Phases

### Phase 1: Foundation (TDD)
1. Database models and migrations
2. Pydantic schemas for request/response
3. Basic FastAPI app structure
4. Health check endpoint

### Phase 2: RAG Pipeline (TDD)
1. Vector store client (Qdrant)
2. Embedding service
3. RAG retrieval logic
4. Citation extraction

### Phase 3: Agent Integration (TDD)
1. OpenAI Agent configuration
2. Tool definitions (search_book_content)
3. Persona prompt injection
4. Safety guardrail checks

### Phase 4: API Endpoints (TDD)
1. POST /chat endpoint
2. WebSocket /ws/chat endpoint
3. Session management endpoints
4. SSE streaming fallback

### Phase 5: Frontend Widget
1. React chat component
2. Selection trigger component
3. Docusaurus integration
4. Accessibility (WCAG 2.1 AA)

### Phase 6: Indexing & Operations
1. Content indexing script
2. Background purge job (24h retention)
3. Analytics event logging
4. Monitoring/observability

---

## Key Design Decisions

### 1. WebSocket vs SSE for Streaming
**Decision**: WebSocket primary, SSE fallback
**Rationale**: WebSocket enables bidirectional communication (user can cancel/interrupt). SSE fallback for restrictive environments.

### 2. Message-Based Retention
**Decision**: Per-message TTL (24h from creation)
**Rationale**: User requirement. More granular than session-based. Enables partial conversation recovery.

### 3. Persona via System Prompt
**Decision**: Inject persona instructions into agent system prompt
**Rationale**: Simpler than fine-tuning. Same RAG results, different explanation style. Easy to update personas.

### 4. Safety Keyword Detection
**Decision**: Keyword-based safety check with disclaimer injection
**Rationale**: Low latency, high recall. Can be enhanced with classifier later. Covers FR-021 through FR-024.

---

## Test Strategy (TDD)

### Unit Tests (RED first)
- `test_citation_extractor.py`: Verify citation parsing from vector results
- `test_persona_adapter.py`: Verify prompt injection per persona
- `test_safety_guardrails.py`: Verify safety keyword detection
- `test_message_retention.py`: Verify TTL calculation

### Integration Tests
- `test_chat_api.py`: End-to-end chat flow
- `test_websocket.py`: WebSocket connection and streaming
- `test_vector_search.py`: Qdrant query with filters

### Contract Tests
- `test_openapi_schema.py`: Validate responses against OpenAPI spec

### Acceptance Tests
- Per user story acceptance scenarios from spec.md

---

## Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Qdrant Cloud latency | Medium | High | Local caching, connection pooling |
| OpenAI rate limits | Medium | Medium | Request queuing, backoff |
| Hallucination despite RAG | Low | High | Strict grounding prompt, citation verification |
| Selection text too long | Low | Low | Frontend validation, clear error message |

---

## Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| fastapi | >=0.109.0 | Web framework |
| openai-agents-python | >=0.2.9 | Agent orchestration |
| qdrant-client | >=1.7.0 | Vector search |
| sqlalchemy | >=2.0.0 | ORM |
| asyncpg | >=0.29.0 | Async PostgreSQL driver |
| pydantic | >=2.5.0 | Validation |
| pydantic-settings | >=2.1.0 | Configuration |
| pytest | >=8.0.0 | Testing |
| pytest-asyncio | >=0.23.0 | Async test support |
| httpx | >=0.26.0 | Async HTTP client |
| alembic | >=1.13.0 | Migrations |

---

## Artifacts Generated

| Artifact | Path | Description |
|----------|------|-------------|
| Research | `research.md` | Technology decisions and rationale |
| Data Model | `data-model.md` | Entity definitions and schemas |
| OpenAPI Spec | `contracts/openapi.yaml` | REST API contract |
| WebSocket Spec | `contracts/websocket.md` | WebSocket protocol |
| Quickstart | `quickstart.md` | Developer setup guide |

---

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks from this plan
2. Begin TDD cycle: Write failing tests (RED) for Phase 1 foundation
3. Implement to make tests pass (GREEN)
4. Refactor while keeping tests green
5. Continue through phases 2-6
6. Create PR when feature complete

---

## Complexity Tracking

> No constitution violations requiring justification. All gates pass.

| Aspect | Decision | Justification |
|--------|----------|---------------|
| Project count | 2 (backend + frontend widget) | Standard web app pattern |
| Database | 2 (Postgres + Qdrant) | Constitution mandates both |
| External APIs | 1 (OpenAI) | Constitution specifies |
