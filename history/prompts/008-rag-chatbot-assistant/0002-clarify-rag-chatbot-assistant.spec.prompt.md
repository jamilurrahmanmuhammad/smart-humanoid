---
id: "0002"
title: "Clarify RAG Chatbot Assistant Spec"
stage: spec
date: 2025-12-02
surface: agent
model: claude-opus-4-5-20251101
feature: 008-rag-chatbot-assistant
branch: 008-rag-chatbot-assistant
user: jamil
command: /sp.clarify
labels: ["rag", "chatbot", "clarification", "ui", "data-retention", "message-policy"]
links:
  spec: specs/008-rag-chatbot-assistant/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/008-rag-chatbot-assistant/spec.md
tests:
  - N/A (specification phase)
---

## Prompt

/sp.clarify

User responses:
- Q1 (UI placement): "A, with selection trigger"
- Q2 (Data retention): "for the time being, it should be only for the session and after the session only for 24 hours from the time that particular message was created. It should be message based policy rather than the conversation based policy."

## Response snapshot

Clarified RAG Chatbot Assistant specification with 2 key decisions:

**Clarification 1 - Chat Widget UI Placement:**
- Decision: Floating button (bottom-right) + selection trigger on text highlight
- Updated FR-001 with floating button placement
- Added FR-001a for selection trigger (tooltip/popover on text highlight)

**Clarification 2 - Data Retention Policy:**
- Decision: Message-based (not conversation-based) retention
- Policy: Messages persist during active session, then 24 hours from each message's creation timestamp
- Updated FR-025: Changed from session-based to message-based storage with message ID
- Updated FR-027: Specified 24-hour message-based retention policy
- Added FR-027a: Per-message expiration timer requirement
- Updated User Story 6 acceptance scenario 3 for message-based purge
- Updated Key Entities (Chat Session, Chat Message, Analytics Event) with retention details

## Outcome

- ✅ Impact: Specification refined with concrete UI placement and data retention policies
- 🧪 Tests: N/A (specification phase)
- 📁 Files: 1 file updated (spec.md)
- 🔁 Next prompts: /sp.plan for implementation planning
- 🧠 Reflection: Message-based retention is more granular than typical conversation-based approach, enabling per-message TTL management

## Evaluation notes (flywheel)

- Failure modes observed: None - clarifications integrated cleanly
- Graders run and results (PASS/FAIL): Specification consistency PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
