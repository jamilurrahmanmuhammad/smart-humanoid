# Implementation Tasks: RAG Chatbot Assistant

**Feature**: 008-rag-chatbot-assistant | **Date**: 2025-12-02
**Methodology**: Test-Driven Development (RED → GREEN → REFACTOR)
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Legend

- `[P]` = Parallelizable with other `[P]` tasks in same phase
- `[B]` = Blocking; must complete before next phase
- `[US#]` = Maps to User Story number
- `[RED]` = Write failing test first
- `[GREEN]` = Implement to pass test
- `[REFACTOR]` = Clean up while green

---

## Phase 0: Project Setup [BLOCKING]

> Foundation tasks that must complete before any implementation.

- [ ] T001 [B] Initialize Python project structure with pyproject.toml
  - Files: `pyproject.toml`, `backend/__init__.py`
  - Acceptance: `pip install -e .` succeeds

- [ ] T002 [B] Create requirements.txt with pinned dependencies
  - Files: `requirements.txt`, `requirements-dev.txt`
  - Dependencies: fastapi>=0.109.0, openai-agents-python>=0.2.9, qdrant-client>=1.7.0, sqlalchemy>=2.0.0, asyncpg>=0.29.0, pydantic>=2.5.0, pydantic-settings>=2.1.0
  - Dev: pytest>=8.0.0, pytest-asyncio>=0.23.0, httpx>=0.26.0, pytest-cov

- [ ] T003 [B] Create .env.example with all required environment variables
  - Files: `.env.example`
  - Variables: OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, DATABASE_URL, APP_ENV, LOG_LEVEL, CORS_ORIGINS

- [ ] T004 [B] Set up pytest configuration with asyncio mode
  - Files: `pytest.ini`, `conftest.py`
  - Acceptance: `pytest --collect-only` shows test collection

- [ ] T005 [B] Create backend directory structure per plan.md
  - Files: `backend/api/__init__.py`, `backend/api/routes/__init__.py`, `backend/models/__init__.py`, `backend/services/__init__.py`, `backend/core/__init__.py`

---

## Phase 1: Configuration & Database Foundation [BLOCKING]

> Core configuration and database setup required by all features.

### 1.1 Configuration (Pydantic Settings)

- [ ] T006 [RED] [B] Write test for Settings model validation
  - File: `tests/unit/test_config.py`
  - Test: Settings loads from env, validates required fields, provides defaults
  - FR: N/A (infrastructure)

- [ ] T007 [GREEN] [B] Implement Settings with pydantic-settings
  - File: `backend/core/config.py`
  - Model: Settings with all env vars from T003
  - Acceptance: T006 passes

### 1.2 Database Models (SQLAlchemy 2.0)

- [ ] T008 [RED] [B] Write test for ChatSession ORM model
  - File: `tests/unit/test_database_models.py`
  - Test: Model fields match data-model.md, relationships defined
  - FR: FR-012 (session context)

- [ ] T009 [GREEN] [B] Implement ChatSession SQLAlchemy model
  - File: `backend/models/database.py`
  - Fields: id, persona, current_chapter, current_page, created_at, ended_at, is_active
  - Acceptance: T008 passes

- [ ] T010 [RED] [P] Write test for ChatMessage ORM model
  - File: `tests/unit/test_database_models.py`
  - Test: Model fields, session FK, expires_at calculation
  - FR: FR-027 (message retention)

- [ ] T011 [GREEN] [P] Implement ChatMessage SQLAlchemy model
  - File: `backend/models/database.py`
  - Fields: id, session_id, role, content, query_type, has_safety_disclaimer, created_at, expires_at
  - Acceptance: T010 passes

- [ ] T012 [RED] [P] Write test for Citation ORM model
  - File: `tests/unit/test_database_models.py`
  - Test: Model fields, message FK
  - FR: FR-004 (citations)

- [ ] T013 [GREEN] [P] Implement Citation SQLAlchemy model
  - File: `backend/models/database.py`
  - Fields: id, message_id, chapter, section, heading, quote, link, relevance_score
  - Acceptance: T012 passes

- [ ] T014 [RED] [P] Write test for AnalyticsEvent ORM model
  - File: `tests/unit/test_database_models.py`
  - Test: Model fields, JSON payload, no PII in payload schema
  - FR: FR-025, FR-026 (analytics storage, no PII)

- [ ] T015 [GREEN] [P] Implement AnalyticsEvent SQLAlchemy model
  - File: `backend/models/database.py`
  - Fields: id, event_type, session_id, payload, created_at
  - Acceptance: T014 passes

### 1.3 Database Connection

- [ ] T016 [RED] [B] Write test for async database session factory
  - File: `tests/unit/test_database.py`
  - Test: Creates async session, handles connection errors
  - FR: N/A (infrastructure)

- [ ] T017 [GREEN] [B] Implement async session factory
  - File: `backend/core/database.py`
  - Pattern: AsyncSession with asyncpg driver
  - Acceptance: T016 passes

### 1.4 Alembic Migrations

- [ ] T018 [B] Initialize Alembic with async support
  - Files: `alembic.ini`, `backend/alembic/env.py`
  - Config: async_fallback=True, target_metadata from models

- [ ] T019 [B] Create initial migration for all models
  - File: `backend/alembic/versions/001_initial_schema.py`
  - Tables: chat_sessions, chat_messages, citations, analytics_events
  - Acceptance: `alembic upgrade head` succeeds on test DB

---

## Phase 2: Pydantic Schemas [BLOCKING]

> Request/Response models required by API layer.

- [ ] T020 [RED] [P] Write test for ChatRequest schema validation
  - File: `tests/unit/test_schemas.py`
  - Test: Validates message length, persona enum, query_type enum, selected_text limit
  - FR: FR-003, FR-018

- [ ] T021 [GREEN] [P] Implement ChatRequest Pydantic model
  - File: `backend/models/schemas.py`
  - Fields per contracts/openapi.yaml ChatRequest
  - Acceptance: T020 passes

- [ ] T022 [RED] [P] Write test for ChatResponse schema
  - File: `tests/unit/test_schemas.py`
  - Test: Required fields, citation array max 5
  - FR: FR-009

- [ ] T023 [GREEN] [P] Implement ChatResponse Pydantic model
  - File: `backend/models/schemas.py`
  - Fields per contracts/openapi.yaml ChatResponse
  - Acceptance: T022 passes

- [ ] T024 [RED] [P] Write test for Citation schema
  - File: `tests/unit/test_schemas.py`
  - Test: All required fields present, link format
  - FR: FR-004, FR-010

- [ ] T025 [GREEN] [P] Implement Citation Pydantic model
  - File: `backend/models/schemas.py`
  - Fields per contracts/openapi.yaml Citation
  - Acceptance: T024 passes

- [ ] T026 [RED] [P] Write test for StreamChunk schema
  - File: `tests/unit/test_schemas.py`
  - Test: Chunk types (content, citation, done, error)
  - FR: NFR-001

- [ ] T027 [GREEN] [P] Implement StreamChunk Pydantic model
  - File: `backend/models/schemas.py`
  - Fields per contracts/websocket.md message types
  - Acceptance: T026 passes

- [ ] T028 [RED] [P] Write test for Session schemas
  - File: `tests/unit/test_schemas.py`
  - Test: CreateSessionRequest, SessionResponse, SessionDetailResponse
  - FR: FR-012

- [ ] T029 [GREEN] [P] Implement Session Pydantic models
  - File: `backend/models/schemas.py`
  - Models: CreateSessionRequest, SessionResponse, SessionDetailResponse
  - Acceptance: T028 passes

- [ ] T030 [RED] [P] Write test for ErrorResponse schema
  - File: `tests/unit/test_schemas.py`
  - Test: Error codes match openapi.yaml
  - FR: FR-028

- [ ] T031 [GREEN] [P] Implement ErrorResponse Pydantic model
  - File: `backend/models/schemas.py`
  - Fields: error, message, code, details
  - Acceptance: T030 passes

---

## Phase 3: US1 - Ask General Questions (P1) [CORE RAG]

> Core RAG functionality with citation-grounded responses.
> Dependencies: Phase 0, 1, 2

### 3.1 Vector Store Client

- [ ] T032 [RED] [B] [US1] Write test for Qdrant client initialization
  - File: `tests/unit/test_vector_store.py`
  - Test: Client connects, handles connection errors gracefully
  - FR: N/A (infrastructure)

- [ ] T033 [GREEN] [B] [US1] Implement VectorStoreClient class
  - File: `backend/services/vector_store.py`
  - Methods: __init__, health_check
  - Acceptance: T032 passes

- [ ] T034 [RED] [B] [US1] Write test for vector search with filters
  - File: `tests/unit/test_vector_store.py`
  - Test: Search returns ContentChunk objects, respects limit, applies filters
  - FR: FR-003

- [ ] T035 [GREEN] [B] [US1] Implement search method
  - File: `backend/services/vector_store.py`
  - Method: search(query_vector, filters, limit) -> List[ContentChunk]
  - Acceptance: T034 passes

### 3.2 Embedding Service

- [ ] T036 [RED] [B] [US1] Write test for embedding generation
  - File: `tests/unit/test_embedding.py`
  - Test: Generates 1536-dim vector, handles empty input
  - FR: N/A (infrastructure)

- [ ] T037 [GREEN] [B] [US1] Implement EmbeddingService
  - File: `backend/services/embedding.py`
  - Method: embed(text) -> List[float]
  - Model: text-embedding-3-small
  - Acceptance: T036 passes

### 3.3 Citation Extractor

- [ ] T038 [RED] [B] [US1] Write test for citation extraction from chunks
  - File: `tests/unit/test_citation_extractor.py`
  - Test: Extracts Citation from ContentChunk, limits to 5
  - FR: FR-004, FR-009

- [ ] T039 [GREEN] [B] [US1] Implement CitationExtractor
  - File: `backend/services/citation.py`
  - Method: extract(chunks, limit=5) -> List[Citation]
  - Acceptance: T038 passes

- [ ] T040 [RED] [P] [US1] Write test for citation deduplication
  - File: `tests/unit/test_citation_extractor.py`
  - Test: Removes duplicate citations by chapter+section
  - FR: FR-009

- [ ] T041 [GREEN] [P] [US1] Implement citation deduplication
  - File: `backend/services/citation.py`
  - Method: deduplicate(citations) -> List[Citation]
  - Acceptance: T040 passes

- [ ] T041a [RED] [P] [US1] Write test for conflicting source detection
  - File: `tests/unit/test_citation_extractor.py`
  - Test: Detects when citations contain contradictory information, flags to user
  - FR: FR-011

- [ ] T041b [GREEN] [P] [US1] Implement conflict detection in citations
  - File: `backend/services/citation.py`
  - Method: detect_conflicts(citations) -> List[ConflictWarning]
  - Behavior: Semantic comparison of citation content for contradictions
  - Acceptance: T041a passes

### 3.4 RAG Pipeline

- [ ] T042 [RED] [B] [US1] Write test for RAG pipeline query flow
  - File: `tests/unit/test_rag_pipeline.py`
  - Test: Query → embed → search → context build → response with citations
  - FR: FR-001, FR-004

- [ ] T043 [GREEN] [B] [US1] Implement RAGPipeline class
  - File: `backend/services/rag.py`
  - Method: query(message, session_context) -> RAGResult
  - Acceptance: T042 passes

- [ ] T044 [RED] [P] [US1] Write test for context window building
  - File: `tests/unit/test_rag_pipeline.py`
  - Test: Builds context from chunks within token limit
  - FR: N/A (infrastructure)

- [ ] T045 [GREEN] [P] [US1] Implement context builder
  - File: `backend/services/rag.py`
  - Method: build_context(chunks, max_tokens) -> str
  - Acceptance: T044 passes

- [ ] T045a [RED] [B] [US1] Write test for out-of-scope query detection
  - File: `tests/unit/test_rag_pipeline.py`
  - Test: Query about content not in book returns "I don't have information about this" response
  - FR: FR-006, FR-007

- [ ] T045b [GREEN] [B] [US1] Implement out-of-scope query handling
  - File: `backend/services/rag.py`
  - Method: detect_out_of_scope(query, search_results) -> bool
  - Behavior: Returns explicit message when no relevant content found (relevance threshold)
  - Acceptance: T045a passes

- [ ] T045c [RED] [B] [US1] Write test for context window summarization
  - File: `tests/unit/test_rag_pipeline.py`
  - Test: When context exceeds limit, earlier turns are summarized (not truncated)
  - FR: FR-013

- [ ] T045d [GREEN] [B] [US1] Implement context summarization
  - File: `backend/services/rag.py`
  - Method: summarize_context(history, max_tokens) -> str
  - Behavior: Summarizes older messages while preserving recent context
  - Acceptance: T045c passes

- [ ] T045e [RED] [P] [US1] Write test for cross-chapter context stitching
  - File: `tests/unit/test_rag_pipeline.py`
  - Test: Query spanning multiple chapters produces coherent combined context
  - FR: FR-014

- [ ] T045f [GREEN] [P] [US1] Implement cross-chapter stitching
  - File: `backend/services/rag.py`
  - Method: stitch_cross_chapter_context(chunks) -> str
  - Behavior: Combines chunks from different chapters with transition markers
  - Acceptance: T045e passes

### 3.5 OpenAI Agent Integration

- [ ] T046 [RED] [B] [US1] Write test for Agent tool definition
  - File: `tests/unit/test_agent.py`
  - Test: search_book_content tool defined with correct schema
  - FR: N/A (infrastructure)

- [ ] T047 [GREEN] [B] [US1] Implement search_book_content tool
  - File: `backend/services/agent.py`
  - Tool: search_book_content(query, filters) using RAGPipeline
  - Acceptance: T046 passes

- [ ] T048 [RED] [B] [US1] Write test for Agent runner with streaming
  - File: `tests/unit/test_agent.py`
  - Test: Agent streams response chunks
  - FR: NFR-001

- [ ] T049 [GREEN] [B] [US1] Implement AgentRunner with streaming
  - File: `backend/services/agent.py`
  - Method: run_stream(message, context) -> AsyncIterator[StreamChunk]
  - Acceptance: T048 passes

### 3.6 Health Check Endpoint

- [ ] T050 [RED] [P] [US1] Write test for health check endpoint
  - File: `tests/integration/test_health.py`
  - Test: Returns healthy/degraded/unhealthy, checks all dependencies
  - FR: N/A (operations)

- [ ] T051 [GREEN] [P] [US1] Implement GET /health endpoint
  - File: `backend/api/routes/health.py`
  - Response: HealthResponse with dependency statuses
  - Acceptance: T050 passes

### 3.7 Chat Endpoint (Non-streaming)

- [ ] T052 [RED] [B] [US1] Write test for POST /chat endpoint
  - File: `tests/integration/test_chat_api.py`
  - Test: Returns ChatResponse with citations, creates session if needed
  - FR: FR-001, FR-004, FR-012

- [ ] T053 [GREEN] [B] [US1] Implement POST /chat endpoint
  - File: `backend/api/routes/chat.py`
  - Endpoint: POST /chat with ChatRequest → ChatResponse
  - Acceptance: T052 passes

### 3.8 Streaming Chat Endpoint (SSE)

- [ ] T054 [RED] [B] [US1] Write test for POST /chat/stream endpoint
  - File: `tests/integration/test_chat_api.py`
  - Test: Returns SSE stream with content/citation/done events
  - FR: NFR-001

- [ ] T055 [GREEN] [B] [US1] Implement POST /chat/stream endpoint
  - File: `backend/api/routes/chat.py`
  - Endpoint: POST /chat/stream → StreamingResponse
  - Acceptance: T054 passes

### 3.9 WebSocket Chat Endpoint

- [ ] T056 [RED] [B] [US1] Write test for WebSocket connection lifecycle
  - File: `tests/integration/test_websocket.py`
  - Test: Connect, receive welcome, send message, receive stream, disconnect
  - FR: FR-003

- [ ] T057 [GREEN] [B] [US1] Implement WebSocket /ws/chat/{session_id}
  - File: `backend/api/routes/chat.py`
  - Protocol per contracts/websocket.md
  - Acceptance: T056 passes

- [ ] T058 [RED] [P] [US1] Write test for WebSocket error handling
  - File: `tests/integration/test_websocket.py`
  - Test: Invalid message format, rate limiting, reconnection
  - FR: FR-028

- [ ] T059 [GREEN] [P] [US1] Implement WebSocket error handling
  - File: `backend/api/routes/chat.py`
  - Error codes per contracts/websocket.md
  - Acceptance: T058 passes

### 3.10 FastAPI Application

- [ ] T060 [B] [US1] Create FastAPI application entry point
  - File: `backend/main.py`
  - Routers: chat, sessions, health
  - Middleware: CORS
  - Acceptance: `uvicorn backend.main:app` starts

### 3.11 Contract Tests

- [ ] T061 [RED] [P] [US1] Write contract test for OpenAPI schema compliance
  - File: `tests/contract/test_openapi_schema.py`
  - Test: Responses match contracts/openapi.yaml schemas
  - FR: N/A (contract validation)

- [ ] T062 [GREEN] [P] [US1] Fix any contract violations
  - Files: Various based on test failures
  - Acceptance: T061 passes

---

## Phase 4: US2 - Persona-Aware Responses (P1)

> Adapt response style based on learner persona.
> Dependencies: Phase 3 (core RAG)

### 4.1 Persona Adapter

- [ ] T063 [RED] [B] [US2] Write test for persona system prompt injection
  - File: `tests/unit/test_persona_adapter.py`
  - Test: Explorer/Builder/Engineer/Default produce different system prompts
  - FR: FR-015, FR-016, FR-017

- [ ] T064 [GREEN] [B] [US2] Implement PersonaAdapter
  - File: `backend/services/persona.py`
  - Method: get_system_prompt(persona) -> str
  - Acceptance: T063 passes

- [ ] T065 [RED] [P] [US2] Write test for persona prompt content
  - File: `tests/unit/test_persona_adapter.py`
  - Test: Explorer mentions simulation, Builder mentions maker, Engineer uses technical depth
  - FR: FR-015, FR-016, FR-017

- [ ] T066 [GREEN] [P] [US2] Implement persona-specific prompts
  - File: `backend/services/persona.py`
  - Prompts: Per Constitution Section XIII
  - Acceptance: T065 passes

### 4.2 Agent Integration

- [ ] T067 [RED] [B] [US2] Write test for Agent with persona context
  - File: `tests/unit/test_agent.py`
  - Test: Agent uses persona system prompt
  - FR: FR-015

- [ ] T068 [GREEN] [B] [US2] Integrate PersonaAdapter into AgentRunner
  - File: `backend/services/agent.py`
  - Modification: Include persona in agent configuration
  - Acceptance: T067 passes

### 4.3 Session Persona Persistence

- [ ] T069 [RED] [P] [US2] Write test for session persona storage
  - File: `tests/integration/test_sessions.py`
  - Test: Session stores persona, subsequent messages use same persona
  - FR: FR-012

- [ ] T070 [GREEN] [P] [US2] Implement session persona persistence
  - File: `backend/api/routes/sessions.py`
  - Modification: Store/retrieve persona from ChatSession
  - Acceptance: T069 passes

---

## Phase 5: US5 - Safe Responses (P1)

> Safety guardrails for physical robotics content.
> Dependencies: Phase 3 (core RAG)

### 5.1 Safety Keyword Detection

- [ ] T071 [RED] [B] [US5] Write test for safety keyword detection
  - File: `tests/unit/test_safety_guardrails.py`
  - Test: Detects motor, gripper, actuator, power, voltage keywords
  - FR: FR-021

- [ ] T072 [GREEN] [B] [US5] Implement SafetyChecker keyword detection
  - File: `backend/services/safety.py`
  - Method: check_keywords(text) -> bool
  - Acceptance: T071 passes

### 5.2 Safety Disclaimer Injection

- [ ] T073 [RED] [B] [US5] Write test for disclaimer injection
  - File: `tests/unit/test_safety_guardrails.py`
  - Test: Disclaimer text prepended when safety keywords detected
  - FR: FR-022, FR-023

- [ ] T074 [GREEN] [B] [US5] Implement disclaimer injection
  - File: `backend/services/safety.py`
  - Method: inject_disclaimer(response, detected) -> str
  - Acceptance: T073 passes

### 5.3 Safety Categories

- [ ] T075 [RED] [P] [US5] Write test for safety category classification
  - File: `tests/unit/test_safety_guardrails.py`
  - Test: Classifies into motor_control, power_systems, physical_assembly
  - FR: FR-024

- [ ] T076 [GREEN] [P] [US5] Implement safety category classification
  - File: `backend/services/safety.py`
  - Method: classify_category(text) -> SafetyCategory
  - Acceptance: T075 passes

### 5.4 RAG Integration

- [ ] T077 [RED] [B] [US5] Write test for safety check in RAG pipeline
  - File: `tests/unit/test_rag_pipeline.py`
  - Test: RAG response includes has_safety_disclaimer flag
  - FR: FR-021

- [ ] T078 [GREEN] [B] [US5] Integrate SafetyChecker into RAGPipeline
  - File: `backend/services/rag.py`
  - Modification: Check query + response for safety keywords
  - Acceptance: T077 passes

---

## Phase 6: US3 - Page-Scoped Questions (P2)

> Context-aware queries prioritizing current chapter.
> Dependencies: Phase 3 (core RAG)

### 6.1 Chapter Filter

- [ ] T079 [RED] [B] [US3] Write test for chapter-filtered vector search
  - File: `tests/unit/test_vector_store.py`
  - Test: Search with chapter_id filter returns only matching chunks
  - FR: FR-003

- [ ] T080 [GREEN] [B] [US3] Implement chapter filter in VectorStoreClient
  - File: `backend/services/vector_store.py`
  - Modification: Add chapter_id to search filters
  - Acceptance: T079 passes

### 6.2 Query Type Handling

- [ ] T081 [RED] [B] [US3] Write test for page query type routing
  - File: `tests/unit/test_rag_pipeline.py`
  - Test: query_type=page applies chapter filter
  - FR: FR-003

- [ ] T082 [GREEN] [B] [US3] Implement page query type in RAGPipeline
  - File: `backend/services/rag.py`
  - Modification: Route page queries through chapter filter
  - Acceptance: T081 passes

### 6.3 Context Update

- [ ] T083 [RED] [P] [US3] Write test for WebSocket context update
  - File: `tests/integration/test_websocket.py`
  - Test: Context message updates current_chapter
  - FR: FR-012

- [ ] T084 [GREEN] [P] [US3] Implement context update handler
  - File: `backend/api/routes/chat.py`
  - Modification: Handle "context" message type
  - Acceptance: T083 passes

---

## Phase 7: US4 - Selection-Scoped Questions (P2)

> Queries based on user-selected text.
> Dependencies: Phase 3 (core RAG)

### 7.1 Selection Validation

- [ ] T085 [RED] [B] [US4] Write test for selection text validation
  - File: `tests/unit/test_schemas.py`
  - Test: Rejects selection > 2000 chars, accepts valid selection
  - FR: FR-018

- [ ] T086 [GREEN] [B] [US4] Implement selection validation in ChatRequest
  - File: `backend/models/schemas.py`
  - Modification: Add validator for selected_text
  - Acceptance: T085 passes

### 7.2 Selection Query Handling

- [ ] T087 [RED] [B] [US4] Write test for selection-only context
  - File: `tests/unit/test_rag_pipeline.py`
  - Test: query_type=selection uses only selected_text as context
  - FR: FR-018, FR-019

- [ ] T088 [GREEN] [B] [US4] Implement selection query in RAGPipeline
  - File: `backend/services/rag.py`
  - Modification: Skip vector search for selection queries
  - Acceptance: T087 passes

- [ ] T088a [RED] [P] [US4] Write test for insufficient selection response
  - File: `tests/unit/test_rag_pipeline.py`
  - Test: Selection-scoped query with insufficient context returns explicit message
  - FR: FR-020

- [ ] T088b [GREEN] [P] [US4] Implement insufficient selection handling
  - File: `backend/services/rag.py`
  - Method: check_selection_sufficiency(selected_text, query) -> bool
  - Behavior: Returns "This selection doesn't contain enough information" when appropriate
  - Acceptance: T088a passes

### 7.3 Selection Response Flag

- [ ] T089 [RED] [P] [US4] Write test for is_selection_scoped flag
  - File: `tests/integration/test_chat_api.py`
  - Test: Response includes is_selection_scoped=true for selection queries
  - FR: FR-019

- [ ] T090 [GREEN] [P] [US4] Implement is_selection_scoped in response
  - File: `backend/api/routes/chat.py`
  - Modification: Set flag based on query_type
  - Acceptance: T089 passes

---

## Phase 8: US6 - Instructor Analytics (P3)

> Analytics event logging for instructor insights.
> Dependencies: Phase 3 (core RAG)

### 8.1 Analytics Event Logging

- [ ] T091 [RED] [B] [US6] Write test for analytics event creation
  - File: `tests/unit/test_analytics.py`
  - Test: Creates AnalyticsEvent with correct payload, validates no PII included
  - FR: FR-025, FR-026

- [ ] T092 [GREEN] [B] [US6] Implement AnalyticsService
  - File: `backend/services/analytics.py`
  - Method: log_event(event_type, session_id, payload)
  - Acceptance: T091 passes

### 8.2 Chat Event Logging

- [ ] T093 [RED] [P] [US6] Write test for chat message analytics
  - File: `tests/integration/test_analytics.py`
  - Test: Chat request logs query_received, response_sent events
  - FR: FR-029

- [ ] T094 [GREEN] [P] [US6] Integrate analytics into chat endpoints
  - File: `backend/api/routes/chat.py`
  - Modification: Log analytics events on request/response
  - Acceptance: T093 passes

### 8.3 Latency Tracking

- [ ] T095 [RED] [P] [US6] Write test for latency tracking
  - File: `tests/unit/test_analytics.py`
  - Test: Tracks first_token_ms, total_ms in analytics
  - FR: NFR-001

- [ ] T096 [GREEN] [P] [US6] Implement latency tracking
  - File: `backend/services/analytics.py`
  - Modification: Calculate and log latency metrics
  - Acceptance: T095 passes

---

## Phase 9: Session Management

> Session CRUD and message retention.
> Dependencies: Phase 1 (database)

### 9.1 Session CRUD

- [ ] T097 [RED] [B] Write test for POST /sessions
  - File: `tests/integration/test_sessions.py`
  - Test: Creates session with persona, returns SessionResponse
  - FR: FR-012

- [ ] T098 [GREEN] [B] Implement POST /sessions endpoint
  - File: `backend/api/routes/sessions.py`
  - Endpoint: POST /sessions → SessionResponse
  - Acceptance: T097 passes

- [ ] T099 [RED] [P] Write test for GET /sessions/{id}
  - File: `tests/integration/test_sessions.py`
  - Test: Returns session details, 404 if not found
  - FR: FR-012

- [ ] T100 [GREEN] [P] Implement GET /sessions/{id} endpoint
  - File: `backend/api/routes/sessions.py`
  - Endpoint: GET /sessions/{id} → SessionDetailResponse
  - Acceptance: T099 passes

- [ ] T101 [RED] [P] Write test for DELETE /sessions/{id}
  - File: `tests/integration/test_sessions.py`
  - Test: Marks session inactive, returns 204
  - FR: FR-012

- [ ] T102 [GREEN] [P] Implement DELETE /sessions/{id} endpoint
  - File: `backend/api/routes/sessions.py`
  - Endpoint: DELETE /sessions/{id} → 204
  - Acceptance: T101 passes

### 9.2 Message Retrieval

- [ ] T103 [RED] [B] Write test for GET /sessions/{id}/messages
  - File: `tests/integration/test_sessions.py`
  - Test: Returns messages with pagination, excludes expired
  - FR: FR-027

- [ ] T104 [GREEN] [B] Implement GET /sessions/{id}/messages endpoint
  - File: `backend/api/routes/sessions.py`
  - Endpoint: GET /sessions/{id}/messages → MessageListResponse
  - Acceptance: T103 passes

### 9.3 Message Retention

- [ ] T105 [RED] [B] Write test for message TTL calculation
  - File: `tests/unit/test_database_models.py`
  - Test: expires_at = created_at + 24h
  - FR: FR-027

- [ ] T106 [GREEN] [B] Implement message TTL in ChatMessage model
  - File: `backend/models/database.py`
  - Modification: Set expires_at on creation
  - Acceptance: T105 passes

- [ ] T107 [RED] [P] Write test for expired message filtering
  - File: `tests/unit/test_database.py`
  - Test: Query excludes messages where expires_at < now
  - FR: FR-027

- [ ] T108 [GREEN] [P] Implement expired message filter
  - File: `backend/core/database.py`
  - Method: get_valid_messages(session_id) excludes expired
  - Acceptance: T107 passes

---

## Phase 10: Content Indexing Scripts

> Scripts for Qdrant setup and content indexing.
> Dependencies: Phase 1 (database), Phase 3.1 (vector store)

- [ ] T109 [B] Create Qdrant collection setup script
  - File: `scripts/setup_qdrant.py`
  - Creates collection with 1536-dim vectors, payload indexes
  - Acceptance: Script runs without error on fresh Qdrant

- [ ] T110 [B] Create content indexing script
  - File: `scripts/index_content.py`
  - Indexes docs/**/*.md with frontmatter metadata
  - Acceptance: Script indexes sample chapter

- [ ] T111 [P] Add chunking logic with overlap
  - File: `scripts/index_content.py`
  - Method: chunk_text(text, size=512, overlap=64)
  - Acceptance: Chunks maintain context at boundaries

---

## Phase 11: Frontend Widget (Future)

> React chat widget for Docusaurus integration.
> Dependencies: All backend phases

- [ ] T112 [P] Create ChatWidget React component
  - File: `frontend/components/ChatWidget.tsx`
  - Features: Message list, input, WebSocket connection
  - FR: N/A (frontend)

- [ ] T113 [P] Create SelectionTrigger component
  - File: `frontend/components/SelectionTrigger.tsx`
  - Features: Text selection detection, context menu
  - FR: FR-018

- [ ] T114 [P] Implement accessibility (WCAG 2.1 AA)
  - Files: `frontend/components/*.tsx`
  - Features: Keyboard nav, screen reader, focus management
  - FR: XXXIV (Constitution)

---

## Phase 12: Operations & Polish

> Observability, background jobs, final cleanup.
> Dependencies: All feature phases

### 12.1 Message Purge Job

- [ ] T115 [RED] [B] Write test for message purge job
  - File: `tests/unit/test_purge.py`
  - Test: Deletes messages where expires_at < now
  - FR: FR-027

- [ ] T116 [GREEN] [B] Implement message purge background task
  - File: `backend/services/purge.py`
  - Method: purge_expired_messages()
  - Acceptance: T115 passes

### 12.2 Error Handling

- [ ] T117 [RED] [P] Write test for graceful degradation
  - File: `tests/integration/test_error_handling.py`
  - Test: Returns INDEX_UNAVAILABLE when Qdrant down
  - FR: FR-028

- [ ] T118 [GREEN] [P] Implement graceful degradation
  - File: `backend/api/routes/chat.py`
  - Modification: Catch vector store errors, return 503
  - Acceptance: T117 passes

- [ ] T118a [RED] [P] Write test for sensitive error filtering
  - File: `tests/integration/test_error_handling.py`
  - Test: API errors do not expose internal paths, stack traces, or credentials
  - FR: FR-029

- [ ] T118b [GREEN] [P] Implement error sanitization
  - File: `backend/api/middleware.py`
  - Method: sanitize_error_response(error) -> ErrorResponse
  - Behavior: Strips sensitive information from error responses
  - Acceptance: T118a passes

### 12.3 Logging & Observability

- [ ] T119 [P] Add structured logging throughout
  - Files: Various backend files
  - Format: JSON with request_id, session_id, latency
  - FR: N/A (operations)

- [ ] T120 [P] Add request timing middleware
  - File: `backend/api/middleware.py`
  - Feature: Log request duration, add X-Request-ID header
  - FR: NFR-001

---

## Dependency Graph

```
Phase 0 (Setup)
    │
    ▼
Phase 1 (Config & DB)
    │
    ▼
Phase 2 (Schemas)
    │
    ▼
Phase 3 (US1: Core RAG) ◄─────────────────────────────┐
    │                                                  │
    ├──────────────┬──────────────┬──────────────┬────┤
    ▼              ▼              ▼              ▼    │
Phase 4        Phase 5        Phase 6        Phase 7  │
(US2:Persona)  (US5:Safety)   (US3:Page)    (US4:Sel) │
    │              │              │              │    │
    └──────────────┴──────────────┴──────────────┘    │
                        │                              │
                        ▼                              │
                   Phase 8 (US6: Analytics)            │
                        │                              │
                        ▼                              │
                   Phase 9 (Sessions) ─────────────────┘
                        │
                        ▼
                   Phase 10 (Indexing Scripts)
                        │
                        ▼
                   Phase 11 (Frontend) [Optional]
                        │
                        ▼
                   Phase 12 (Operations)
```

---

## Parallel Execution Guide

### Within Phase 1 (after T007):
```bash
# Run in parallel:
pytest tests/unit/test_database_models.py::test_chat_message &
pytest tests/unit/test_database_models.py::test_citation &
pytest tests/unit/test_database_models.py::test_analytics_event &
wait
```

### Within Phase 2:
```bash
# All schema tests can run in parallel:
pytest tests/unit/test_schemas.py -n auto
```

### After Phase 3 completes:
```bash
# Phases 4, 5, 6, 7 can run in parallel:
pytest tests/unit/test_persona_adapter.py &
pytest tests/unit/test_safety_guardrails.py &
pytest tests/unit/test_vector_store.py::test_chapter_filter &
pytest tests/unit/test_rag_pipeline.py::test_selection_query &
wait
```

---

## Summary

| Phase | Tasks | Priority | Story Coverage |
|-------|-------|----------|----------------|
| 0 | T001-T005 | P0 | Setup |
| 1 | T006-T019 | P0 | Foundation |
| 2 | T020-T031 | P0 | Schemas |
| 3 | T032-T062 (+T041a-b, T045a-f) | P1 | US1 (Core RAG) |
| 4 | T063-T070 | P1 | US2 (Personas) |
| 5 | T071-T078 | P1 | US5 (Safety) |
| 6 | T079-T084 | P2 | US3 (Page-scoped) |
| 7 | T085-T090 (+T088a-b) | P2 | US4 (Selection) |
| 8 | T091-T096 | P3 | US6 (Analytics) |
| 9 | T097-T108 | P1 | Sessions |
| 10 | T109-T111 | P2 | Indexing |
| 11 | T112-T114 | P3 | Frontend |
| 12 | T115-T120 (+T118a-b) | P2 | Operations |

**Total Tasks**: 132
**TDD Tasks (RED+GREEN pairs)**: 106 (53 test pairs)
**Blocking Tasks**: 64
**Parallelizable Tasks**: 68

---

## Next Steps

1. Begin Phase 0: `T001` - Initialize project structure
2. Run tests in RED phase before implementing
3. Mark tasks complete as you progress
4. Create PR when Phase 3 (US1) is complete for early review
