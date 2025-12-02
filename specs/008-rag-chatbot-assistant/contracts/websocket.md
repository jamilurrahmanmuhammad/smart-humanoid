# WebSocket Contract: RAG Chatbot Assistant

**Endpoint**: `ws://[host]/api/v1/ws/chat/{session_id}`

---

## Overview

WebSocket endpoint for real-time bidirectional chat communication. Provides streaming responses with lower latency than SSE.

**FR References**: FR-003, FR-004, FR-012, NFR-001

---

## Connection

### URL Pattern
```
ws://localhost:8000/api/v1/ws/chat/{session_id}
wss://api.example.com/api/v1/ws/chat/{session_id}
```

### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| session_id | UUID | Chat session identifier |

### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| token | string | Yes | JWT authentication token |

### Connection Example
```javascript
const ws = new WebSocket(
  `wss://api.example.com/api/v1/ws/chat/${sessionId}?token=${authToken}`
);
```

---

## Message Protocol

All messages are JSON-encoded.

### Client -> Server Messages

#### 1. Chat Message
Send a user question to the chatbot.

```json
{
  "type": "message",
  "data": {
    "content": "What is embodied intelligence?",
    "query_type": "global",
    "current_chapter": null,
    "selected_text": null
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | Yes | Must be "message" |
| data.content | string | Yes | User's question (1-2000 chars) |
| data.query_type | enum | No | "global" (default), "page", "selection" |
| data.current_chapter | int | No | Chapter for page-scoped queries |
| data.selected_text | string | No | Text for selection-scoped queries (max 2000) |

#### 2. Ping (Keep-Alive)
```json
{
  "type": "ping"
}
```

#### 3. Update Context
Update session context without sending a message.

```json
{
  "type": "context",
  "data": {
    "current_chapter": 3,
    "current_page": "/docs/module-1/chapter-3-urdf-modeling-explorer"
  }
}
```

---

### Server -> Client Messages

#### 1. Welcome (on connection)
```json
{
  "type": "welcome",
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "persona": "Explorer",
    "connected_at": "2025-12-02T10:30:00Z"
  }
}
```

#### 2. Content Chunk (streaming response)
```json
{
  "type": "content",
  "data": {
    "chunk": "Embodied intelligence refers to ",
    "message_id": "msg-uuid-here"
  }
}
```

#### 3. Citation
```json
{
  "type": "citation",
  "data": {
    "chapter": 1,
    "section": "1.2",
    "heading": "Understanding Embodied Intelligence",
    "quote": "Embodied intelligence is the capacity of an agent...",
    "link": "/docs/module-1/chapter-1-foundations-explorer#embodied-intelligence",
    "relevance_score": 0.92
  }
}
```

#### 4. Safety Warning
```json
{
  "type": "safety",
  "data": {
    "message": "This involves physical hardware operations. Always consult official equipment manuals."
  }
}
```

#### 5. Done (response complete)
```json
{
  "type": "done",
  "data": {
    "message_id": "msg-uuid-here",
    "citation_count": 2,
    "has_safety_disclaimer": false,
    "latency_ms": 1234
  }
}
```

#### 6. Error
```json
{
  "type": "error",
  "data": {
    "code": "INDEX_UNAVAILABLE",
    "message": "The content index is temporarily unavailable.",
    "recoverable": true
  }
}
```

| Error Code | Recoverable | Description |
|------------|-------------|-------------|
| VALIDATION_ERROR | Yes | Invalid message format |
| INDEX_UNAVAILABLE | Yes | Vector store temporarily down (FR-028) |
| LLM_ERROR | Yes | LLM service error |
| RATE_LIMITED | Yes | Too many requests |
| SESSION_EXPIRED | No | Session no longer active |
| AUTH_ERROR | No | Authentication failed |

#### 7. Pong (response to ping)
```json
{
  "type": "pong",
  "data": {
    "timestamp": "2025-12-02T10:30:05Z"
  }
}
```

---

## Sequence Diagram

```
Client                                Server
  |                                     |
  |------ Connect with token ---------->|
  |                                     |
  |<-------- Welcome message -----------|
  |                                     |
  |------ Chat message ---------------->|
  |                                     |
  |<-------- Content chunk 1 -----------|
  |<-------- Content chunk 2 -----------|
  |<-------- Content chunk N -----------|
  |<-------- Citation 1 ----------------|
  |<-------- Citation 2 ----------------|
  |<-------- Done message --------------|
  |                                     |
  |------ Ping ------------------------>|
  |<-------- Pong ----------------------|
  |                                     |
  |------ Close connection ------------>|
```

---

## Error Handling

### Connection Errors
| Code | Reason | Action |
|------|--------|--------|
| 1008 | Policy Violation | Invalid/expired token |
| 1011 | Internal Error | Server error, retry with backoff |
| 1013 | Try Again Later | Rate limited |

### Reconnection Strategy
```javascript
const reconnect = (attempt = 1) => {
  const delay = Math.min(1000 * Math.pow(2, attempt), 30000);
  setTimeout(() => {
    try {
      connect();
    } catch (e) {
      reconnect(attempt + 1);
    }
  }, delay);
};
```

---

## Client Implementation Example

```typescript
interface ChatMessage {
  type: 'message';
  data: {
    content: string;
    query_type?: 'global' | 'page' | 'selection';
    current_chapter?: number;
    selected_text?: string;
  };
}

interface ServerMessage {
  type: 'welcome' | 'content' | 'citation' | 'safety' | 'done' | 'error' | 'pong';
  data: Record<string, unknown>;
}

class ChatWebSocket {
  private ws: WebSocket;
  private messageBuffer: string = '';

  constructor(sessionId: string, token: string) {
    this.ws = new WebSocket(
      `wss://api.example.com/api/v1/ws/chat/${sessionId}?token=${token}`
    );

    this.ws.onmessage = (event) => {
      const msg: ServerMessage = JSON.parse(event.data);

      switch (msg.type) {
        case 'content':
          this.messageBuffer += msg.data.chunk;
          this.onContentChunk(msg.data.chunk as string);
          break;
        case 'citation':
          this.onCitation(msg.data);
          break;
        case 'done':
          this.onComplete(this.messageBuffer, msg.data);
          this.messageBuffer = '';
          break;
        case 'error':
          this.onError(msg.data);
          break;
      }
    };
  }

  send(message: string, options?: Partial<ChatMessage['data']>) {
    this.ws.send(JSON.stringify({
      type: 'message',
      data: {
        content: message,
        query_type: 'global',
        ...options
      }
    }));
  }

  // Override these handlers
  onContentChunk(chunk: string) {}
  onCitation(citation: unknown) {}
  onComplete(fullMessage: string, metadata: unknown) {}
  onError(error: unknown) {}
}
```

---

## Rate Limiting

| Limit | Value | Per |
|-------|-------|-----|
| Messages | 10 | minute |
| Connections | 3 | user |
| Message size | 10KB | message |

Exceeding limits returns error code `RATE_LIMITED`.

---

## FR Traceability

| Requirement | Implementation |
|-------------|----------------|
| FR-003 | query_type in message data |
| FR-004 | Citation messages with grounding |
| FR-012 | Session context maintained |
| FR-019 | is_selection_scoped in done message |
| FR-021 | Safety warning message type |
| FR-028 | INDEX_UNAVAILABLE error code |
| NFR-001 | latency_ms in done message |
