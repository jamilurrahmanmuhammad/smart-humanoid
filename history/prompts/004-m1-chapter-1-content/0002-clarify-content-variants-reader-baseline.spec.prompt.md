---
id: "0002"
title: Clarify Content Variants Reader Baseline
stage: spec
date: 2025-12-02
surface: agent
model: claude-opus-4-5-20251101
feature: 004-m1-chapter-1-content
branch: 004-m1-chapter-1-content
user: jamil
command: /sp.clarify
labels: ["clarification", "personalization", "content-variants", "constitution-update"]
links:
  spec: specs/004-m1-chapter-1-content/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-m1-chapter-1-content/spec.md
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

/sp.clarify - Clarify content adaptation approach for learner profiles and update constitution with generalized rules.

User clarifications provided:
1. Content should adapt based on learner profiles (Explorer/Builder/Engineer)
2. Readers are basic generative AI users, not AI theorists
3. Three separate chapter variants with hackathon-aligned naming
4. Differentiation via both examples AND content depth

## Response snapshot

Conducted clarification session with 3 questions:

1. **Content Adaptation**: Three separate chapter variants (Explorer/Builder/Engineer) with hackathon-aligned naming convention
2. **Reader Background**: Basic generative AI users who may not know AI theory - content must explain from first principles
3. **Variant Differentiation**:
   - Same core narrative with different examples (software analogies vs hardware context)
   - Different content depth (high-level → moderate → technical)

**Constitution Updated (1.1.1 → 1.2.0):**
- Added Reader Baseline Assumption section
- Added Content Variant Strategy with naming convention
- Added Variant Differentiation Rules (examples + depth)
- Updated Section XIII. Adaptive Content significantly

**Spec Updated:**
- Added clarifications section with session log
- Updated FR-024 prerequisites
- Added FR-008a for first-principles AI explanation
- Updated edge cases and assumptions

## Outcome

- ✅ Impact: Both spec and constitution updated with content personalization strategy
- 🧪 Tests: N/A (clarification phase)
- 📁 Files: 2 files updated (spec.md, constitution.md)
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: User wanted generalized rules in constitution, not just chapter-specific requirements

## Evaluation notes (flywheel)

- Failure modes observed: Initially tried to add detailed variant requirements to spec only - user wanted constitution generalization
- Graders run and results (PASS/FAIL): All coverage categories now Clear
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase
