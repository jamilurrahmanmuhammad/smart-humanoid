# Feature Specification: RAG Chatbot Assistant

**Feature Branch**: `008-rag-chatbot-assistant`
**Created**: 2025-12-02
**Status**: Draft
**Input**: User description: "RAG chatbot for conversational learning with persona-aware, citation-grounded answers aligned with constitution"

## Clarifications

### Session 2025-12-02

- Q: Chat widget UI placement? → A: Floating button (bottom-right) expanding to chat panel, plus selection trigger on text highlight
- Q: Conversation/message retention policy? → A: Message-based (not conversation-based): messages persist during session, then retained for 24 hours from each message's creation timestamp before automatic purge

---

## Overview

Transform the textbook from static content into a conversational learning environment. Learners can ask questions about book content and receive grounded, citation-aware answers that respect their learning persona (Explorer, Builder, Engineer) and include appropriate safety guidance for physical robotics topics.

**Constitution Alignment**: This feature implements Constitution Sections X-XI (Technology Platform), XVIII-XX (RAG Assistant Governance), and XXIV-XXVII (Embodied Intelligence Safety).

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask General Questions About the Book (Priority: P1)

As a learner, I want to ask open-ended questions about the book (e.g., "What is embodied intelligence?") so that I can clarify concepts without manually searching through chapters.

**Why this priority**: Core value proposition - enables conversational learning. Without this, the chatbot has no purpose.

**Independent Test**: Can be fully tested by asking a question about book content and verifying the response includes relevant citations and accurate information grounded in the textbook.

**Acceptance Scenarios**:

1. **Given** a learner on any book page, **When** they ask "What is embodied intelligence?", **Then** the chatbot responds with an answer sourced from Chapter 1 content with at least one citation reference.
2. **Given** a learner asks about content not covered in the book, **When** the system cannot find relevant content, **Then** it clearly states "I don't have information about this in the book" rather than hallucinating.
3. **Given** a learner asks a question, **When** the response requires multiple sources, **Then** all contributing chapters/sections are cited (max 5 citations per Constitution Section XIX).

---

### User Story 2 - Persona-Aware Responses (Priority: P1)

As a learner with a specific background (Explorer/Builder/Engineer), I want the chatbot's answers to match my experience level so that explanations are accessible and relevant to my context.

**Why this priority**: Core to personalization promise. The three-variant strategy (Constitution Section XIII) must extend to chatbot responses.

**Independent Test**: Can be tested by asking the same question with different persona settings and verifying response complexity, examples, and language adapt appropriately.

**Acceptance Scenarios**:

1. **Given** an Explorer persona (software background, simulation-focused), **When** they ask about torque, **Then** the response uses software analogies and avoids hardware-specific jargon.
2. **Given** a Builder persona (Arduino/Raspberry Pi experience), **When** they ask about torque, **Then** the response includes maker-friendly examples with moderate technical detail.
3. **Given** an Engineer persona (industrial robotics context), **When** they ask about torque, **Then** the response provides full technical depth with real-world hardware considerations.
4. **Given** no persona is selected, **When** a learner asks a question, **Then** a balanced default style is used that doesn't assume specialized background.

---

### User Story 3 - Ask Questions About Current Page (Priority: P2)

As a learner reading a specific chapter, I want to ask questions that prioritize content from my current location so that I get context-aware explanations without unrelated information.

**Why this priority**: Enhances learning flow by respecting reader's current context. Important but not essential for MVP.

**Independent Test**: Can be tested by navigating to a specific chapter, asking a question, and verifying the response prioritizes citations from that chapter before referencing other sections.

**Acceptance Scenarios**:

1. **Given** a learner on Chapter 2 (ROS 2 Architecture), **When** they ask "What are nodes?", **Then** the response primarily cites Chapter 2 content before referencing other chapters.
2. **Given** page-scoped mode is enabled, **When** the current chapter doesn't cover the topic, **Then** the system indicates this and offers to search the full book.

---

### User Story 4 - Ask Questions About Selected Text (Priority: P2)

As a learner, I want to highlight a specific paragraph and ask a question that is answered only from that selection so that I can deeply understand that specific content without noise from other sections.

**Why this priority**: Enables deep, focused learning on specific passages. Valuable for complex topics.

**Independent Test**: Can be tested by selecting a paragraph, asking a question, and verifying the response uses only the selected text as context.

**Acceptance Scenarios**:

1. **Given** a learner selects a paragraph about URDF joints, **When** they ask "Explain this in simpler terms", **Then** the response is based only on the selected text.
2. **Given** selection-scoped mode is active, **When** the selected text doesn't contain enough information to answer, **Then** the chatbot clearly states "This selection doesn't contain enough information to answer your question" rather than pulling from other content.
3. **Given** selection-scoped mode, **When** the learner receives an answer, **Then** the UI clearly indicates the answer is based on the selected text only.

---

### User Story 5 - Safe Responses for Physical Robotics Topics (Priority: P1)

As a learner working with physical robots, I want the chatbot to include safety warnings and avoid unsafe advice so that I don't accidentally damage equipment or injure myself.

**Why this priority**: Safety is non-negotiable per Constitution Sections XXIV-XXVII. Critical for any physical robotics content.

**Independent Test**: Can be tested by asking questions about hardware manipulation, motor control, or physical experiments and verifying safety disclaimers are included.

**Acceptance Scenarios**:

1. **Given** a learner asks "How do I rewire my robot's motor?", **When** the question involves physical risk, **Then** the response includes safety disclaimers and recommends consulting official manuals or instructors.
2. **Given** a learner asks about bypassing safety interlocks, **When** the request could lead to dangerous outcomes, **Then** the chatbot refuses to provide step-by-step instructions.
3. **Given** a question about hardware experimentation, **When** safety considerations apply, **Then** the response distinguishes between "conceptual understanding" and "ready to try on real hardware."
4. **Given** any response about physical operations, **When** multiple safety layers exist (Constitution Section XXIV), **Then** the chatbot encourages learners to cross-check procedures before attempting.

---

### User Story 6 - Instructor Analytics Access (Priority: P3)

As an instructor or author, I want visibility into how learners use the chatbot so that I can identify common questions and improve book content.

**Why this priority**: Valuable for content improvement but not essential for learner experience. Can be added after core functionality.

**Independent Test**: Can be tested by verifying chat interaction metadata is stored (without personal identifiers) and can be queried for analytics.

**Acceptance Scenarios**:

1. **Given** a learner asks questions, **When** the interaction completes, **Then** anonymized metadata is stored including: message ID, creation timestamp, persona type, chapter/page, query type (global/page/selection).
2. **Given** stored analytics data, **When** an instructor reviews it, **Then** no personally identifiable information is exposed.
3. **Given** the message-based retention policy, **When** 24 hours have elapsed from a message's creation timestamp (post-session), **Then** that specific message is automatically purged.

---

### Edge Cases

- What happens when the book content index is temporarily unavailable? → System must degrade gracefully with user-friendly error, no fallback to ungrounded responses.
- How does system handle questions in languages other than English? → For this release, English only; non-English queries receive a clear message about language support.
- What happens when a learner asks the same question repeatedly? → Responses may vary slightly but citations must remain consistent with source content.
- How does system handle extremely long selected text? → Selection is limited to a reasonable size (e.g., 2000 characters) with clear feedback if exceeded.
- What happens during high concurrent usage? → System must maintain response quality; latency may increase but functionality preserved.

---

## Requirements *(mandatory)*

### Functional Requirements

**Chat Interface**

- **FR-001**: System MUST display a chat interface as a floating button (bottom-right corner) that expands to a chat panel, accessible from all book content pages.
- **FR-001a**: System MUST display a selection trigger (e.g., tooltip/popover) when users highlight text, enabling "Ask about this" functionality.
- **FR-002**: Chat interface MUST be accessible via keyboard and include ARIA labels for screen readers (Constitution Section XXXIV).
- **FR-003**: System MUST support free-form questions, page-scoped questions, and selection-scoped questions.

**Answer Grounding (Constitution Section XVIII)**

- **FR-004**: Every response MUST be grounded in indexed book content with traceable citations.
- **FR-005**: Responses MUST cite specific sections, chapters, or passages in the format: "Chapter X, Section Y: 'relevant quote'".
- **FR-006**: Out-of-scope questions MUST receive explicit "I don't have information about this in the book" responses.
- **FR-007**: System MUST NOT hallucinate content that doesn't exist in the book.

**Multi-Source Citation (Constitution Section XIX)**

- **FR-008**: Responses synthesizing multiple sources MUST cite all contributing passages.
- **FR-009**: Maximum 5 citations per response to maintain readability.
- **FR-010**: Citations MUST link to the exact location in the book.
- **FR-011**: Conflicting information across sources MUST be flagged to the user.

**Context Management (Constitution Section XX)**

- **FR-012**: Conversation history MUST be preserved within a user session.
- **FR-013**: When context window limits are reached, earlier turns MUST be summarized rather than truncated.
- **FR-014**: Cross-chapter queries MUST stitch relevant content coherently.

**Persona Adaptation (Constitution Section XIII)**

- **FR-015**: System MUST accept persona input (Explorer, Builder, Engineer) from the user interface.
- **FR-016**: Persona MUST influence: level of technical depth, choice of analogies, explanation style.
- **FR-017**: If no persona is provided, a default balanced style MUST be used.

**Selection-Scoped Mode**

- **FR-018**: When selection-scoped mode is active, answers MUST be based only on the selected text.
- **FR-019**: Selection-scoped responses MUST clearly indicate they are based on the selection only.
- **FR-020**: If the selection doesn't contain enough information, system MUST state this explicitly.

**Safety Guardrails (Constitution Sections XXIV-XXVII)**

- **FR-021**: System MUST include safety disclaimers for questions involving physical robotics operations.
- **FR-022**: System MUST refuse or heavily qualify advice that involves physical risks (rewiring, bypassing safety).
- **FR-023**: System MUST distinguish between conceptual explanation and readiness for real hardware.
- **FR-024**: System MUST encourage cross-checking complex physical procedures with official sources.

**Session & Metadata Storage**

- **FR-025**: Chat messages MUST be stored individually with: message ID, session ID, creation timestamp, persona type, chapter/page context, query type.
- **FR-026**: Storage MUST avoid personally identifiable information.
- **FR-027**: Data retention MUST follow message-based policy: messages persist during active session, then are retained for 24 hours from each message's creation timestamp before automatic purge.
- **FR-027a**: Retention policy MUST be applied per-message (not per-conversation), with each message having its own 24-hour expiration timer.

**Error Handling**

- **FR-028**: If content index is unavailable, system MUST show user-friendly error without attempting ungrounded responses.
- **FR-029**: API errors MUST NOT expose sensitive system information to users.
- **FR-030**: System MUST maintain graceful degradation under high load.

### Non-Functional Requirements

- **NFR-001**: First response token MUST begin within 5 seconds under normal conditions.
- **NFR-002**: Chat interface MUST meet WCAG 2.1 AA accessibility standards.
- **NFR-003**: API credentials MUST never be exposed to the client-side.
- **NFR-004**: System MUST log request timestamps, failure modes, and sanitized error messages.

### Key Entities

- **Chat Session**: Represents a conversation between a learner and the chatbot. Contains session ID, start time, persona, and associated messages. Session is ephemeral (no persistence beyond active use).
- **Chat Message**: Individual message within a session. Contains message ID, role (user/assistant), content, creation timestamp, citations, query type, and expiration timestamp (24 hours post-session). Each message is independently tracked for retention.
- **Content Chunk**: Indexed portion of book content. Contains text, source location (module/chapter/section), persona variant, and embedding reference.
- **Citation**: Reference to source content. Contains chapter, section, quote extract, and link to source.
- **Analytics Event**: Anonymized interaction metadata for instructor insights. Contains message ID, creation timestamp, persona, chapter, query type (no PII). Subject to message-based 24-hour retention.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of responses include at least one accurate citation to book content.
- **SC-002**: First response token appears within 5 seconds for 90% of queries under normal load.
- **SC-003**: Users report understanding improvement in 80% of chat interactions (measured via optional feedback).
- **SC-004**: 100% of questions about physical robotics operations include safety disclaimers.
- **SC-005**: Chat interface passes WCAG 2.1 AA accessibility audit.
- **SC-006**: Zero instances of hallucinated content (content not in the book) in production responses.
- **SC-007**: Persona-adapted responses demonstrate measurable difference in complexity/vocabulary across the three variants.
- **SC-008**: Selection-scoped responses correctly use only the selected text as context in 100% of cases.
- **SC-009**: System maintains functionality when content index is temporarily unavailable (graceful degradation).
- **SC-010**: Instructor analytics capture 100% of interactions without exposing personal identifiers.

---

## Assumptions

- Book content is available for indexing and chunking.
- Users have completed onboarding that captures their persona (or can select it ad-hoc).
- The platform has user session management in place.
- Content is primarily in English for this release.
- The three-variant chapter structure (Explorer/Builder/Engineer) is in place for indexed content.

---

## Out of Scope

- Multi-tenant authentication/SSO (handled by separate feature)
- Payment/billing integration
- Mobile app integration
- Non-English language support (beyond English)
- Fine-tuned models or custom training pipelines
- Full instructor analytics dashboard (only data persistence in this feature)

---

## Dependencies

- User onboarding/personalization system (for persona detection)
- Book content published and structured per Constitution standards
- Session management infrastructure

---

## Constitution Compliance Checklist

| Constitution Section | Requirement | Addressed By |
|----------------------|-------------|--------------|
| X-XI Technology Platform | Platform stack | Infrastructure (implementation detail) |
| XIII Adaptive Content | Three personas | FR-015, FR-016, FR-017 |
| XVIII Answer Grounding | Citation requirements | FR-004, FR-005, FR-006, FR-007 |
| XIX Multi-Source Citation | Multiple source handling | FR-008, FR-009, FR-010, FR-011 |
| XX Context Stitching | Conversation continuity | FR-012, FR-013, FR-014 |
| XXIV LLM-to-Robot Safety | Safety guardrails | FR-021, FR-022, FR-023, FR-024 |
| XXXIV Accessibility | WCAG 2.1 AA | FR-002, NFR-002, SC-005 |
