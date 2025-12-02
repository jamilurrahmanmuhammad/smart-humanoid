---
id: "0006"
title: "Implement Chapter Navigation Order Fix"
stage: green
date: 2025-12-02
surface: agent
model: claude-opus-4-5-20251101
feature: 007-fix-chapter-nav-order
branch: 007-fix-chapter-nav-order
user: jamil
command: /sp.implement
labels: ["tdd", "navigation", "sidebar", "frontmatter", "e2e-testing"]
links:
  spec: specs/007-fix-chapter-nav-order/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - tests/e2e/sidebar-order.spec.ts (created)
  - docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-explorer.md (sidebar_position 3→5)
  - docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-builder.md (sidebar_position 4→6)
  - docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-engineer.md (sidebar_position 5→7)
  - docs/module-1-robotic-nervous-system/chapter-3-urdf-modeling-explorer.md (sidebar_position 6→8)
  - docs/module-1-robotic-nervous-system/chapter-3-urdf-modeling-builder.md (sidebar_position 7→9)
  - docs/module-1-robotic-nervous-system/chapter-3-urdf-modeling-engineer.md (sidebar_position 8→10)
  - specs/007-fix-chapter-nav-order/tasks.md (all tasks marked complete)
tests:
  - tests/e2e/sidebar-order.spec.ts (4 tests - all passing)
  - Full E2E suite (21 tests - all passing)
---

## Prompt

/sp.implement

Execute the TDD implementation plan for fixing chapter navigation ordering in Docusaurus sidebar.

## Response snapshot

Successfully implemented sidebar navigation fix using TDD methodology:

**Phase 1: RED (Test First)**
- Created `tests/e2e/sidebar-order.spec.ts` with 4 E2E tests
- Tests correctly detected the interleaving bug (Ch1 Engineer appearing after Ch2 Explorer)
- All 4 tests FAILED as expected (RED state confirmed)

**Phase 2: GREEN (Implementation)**
- Updated 6 chapter files with corrected `sidebar_position` values:
  - Chapter 2: 3→5, 4→6, 5→7
  - Chapter 3: 6→8, 7→9, 8→10
- All 4 sidebar-order tests now PASS (GREEN state achieved)

**Phase 3: REFACTOR (Validation)**
- Docusaurus build: SUCCESS
- Full E2E suite: 21/21 tests PASS
- Visual verification: Sidebar now displays Ch1 → Ch2 → Ch3 in correct order

**TDD Cycle Complete:**
- RED: 4 failing tests detected the bug
- GREEN: 6 file edits fixed the bug
- REFACTOR: Full validation confirmed the fix

## Outcome

- ✅ Impact: Sidebar navigation now displays chapters in correct sequential order
- 🧪 Tests: 4 new E2E tests + 21 total suite (all passing)
- 📁 Files: 7 modified (6 chapters + 1 test file)
- 🔁 Next prompts: /sp.git.commit_pr to commit and create PR
- 🧠 Reflection: TDD approach caught the exact bug (interleaving) with automated tests for regression protection

## Evaluation notes (flywheel)

- Failure modes observed: Initial test selectors needed adjustment for Docusaurus sidebar structure
- Graders run and results (PASS/FAIL): Build PASS, E2E suite PASS (21/21)
- Prompt variant (if applicable): TDD approach with Playwright E2E tests
- Next experiment (smallest change to try): N/A - fix complete
