---
id: "0002"
title: "Plan Chapter Navigation Order Fix"
stage: plan
date: 2025-12-02
surface: agent
model: claude-opus-4-5-20251101
feature: 007-fix-chapter-nav-order
branch: 007-fix-chapter-nav-order
user: jamil
command: /sp.plan
labels: ["navigation", "sidebar", "frontmatter", "fix"]
links:
  spec: specs/007-fix-chapter-nav-order/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/007-fix-chapter-nav-order/plan.md
tests:
  - N/A (planning phase)
---

## Prompt

/sp.plan for feature 1

User wants to plan the fix for feature 1 (docusaurus setup) navigation ordering issue, created as a new branch 007-fix-chapter-nav-order.

## Response snapshot

Created implementation plan for fixing chapter navigation ordering.

**Root Cause**: Overlapping `sidebar_position` frontmatter values between chapters:
- Chapter 1: positions 2, 3, 4
- Chapter 2: positions 3, 4, 5 (overlaps with Chapter 1!)
- Chapter 3: positions 6, 7, 8

**Solution**: Update to non-overlapping sequential positions using formula:
`position = (chapter_number - 1) * 3 + variant_offset + 1`

**Files to modify**: 6 chapter files (Chapter 2 and Chapter 3 variants)
- chapter-2-ros2-architecture-explorer.md: 3→5
- chapter-2-ros2-architecture-builder.md: 4→6
- chapter-2-ros2-architecture-engineer.md: 5→7
- chapter-3-urdf-modeling-explorer.md: 6→8
- chapter-3-urdf-modeling-builder.md: 7→9
- chapter-3-urdf-modeling-engineer.md: 8→10

**Skipped Artifacts**: research.md, data-model.md, contracts/, quickstart.md (not needed for simple frontmatter fix)

## Outcome

- ✅ Impact: Clear implementation plan with exact file changes documented
- 🧪 Tests: Build verification + visual inspection planned
- 📁 Files: 1 file created (plan.md)
- 🔁 Next prompts: /sp.tasks then /sp.implement
- 🧠 Reflection: Simple fix recognized - skipped unnecessary Phase 0/1 artifacts to avoid overhead

## Evaluation notes (flywheel)

- Failure modes observed: None - straightforward fix
- Graders run and results (PASS/FAIL): Constitution Check PASS (all gates)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
