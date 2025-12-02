# Tasks: Fix Chapter Navigation Order (TDD Approach)

**Input**: Design documents from `/specs/007-fix-chapter-nav-order/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)
**Methodology**: Test-Driven Development (RED → GREEN → REFACTOR)

**Organization**: Single user story (P1) - all tasks fix the navigation ordering issue.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1)
- Include exact file paths in descriptions

## Path Conventions

- **Content**: `docs/module-1-robotic-nervous-system/`
- **Tests**: `tests/e2e/`

---

## Phase 1: RED - Write Failing Tests First

**Goal**: Create E2E test that validates correct sidebar navigation order. Test should FAIL with current state.

**CLI Command**: `npx playwright test tests/e2e/sidebar-order.spec.ts --reporter=list`

### Test Creation

- [X] T001 [US1] Create `tests/e2e/sidebar-order.spec.ts` with E2E test that verifies Module 1 sidebar displays chapters in correct order: Ch1 variants → Ch2 variants → Ch3 variants (FR-011, SC-002)

**Test Specification**:
```typescript
// Expected order in sidebar (by text content):
// 1. Module 1 index
// 2. Chapter 1 Explorer
// 3. Chapter 1 Builder
// 4. Chapter 1 Engineer
// 5. Chapter 2 Explorer
// 6. Chapter 2 Builder
// 7. Chapter 2 Engineer
// 8. Chapter 3 Explorer
// 9. Chapter 3 Builder
// 10. Chapter 3 Engineer
```

**Checkpoint**: Test written and FAILS (red state confirmed)

**CLI Validation**: `npm run build && npx playwright test sidebar-order --reporter=list` → should FAIL

---

## Phase 2: GREEN - Implement the Fix

**Goal**: Update sidebar_position frontmatter values to make the test pass

**Independent Test**: After all fixes, run `npx playwright test sidebar-order --reporter=list` → should PASS

### Chapter 2 Fixes

- [X] T002 [P] [US1] Update sidebar_position from 3 to 5 in docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-explorer.md (FR-005)
- [X] T003 [P] [US1] Update sidebar_position from 4 to 6 in docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-builder.md (FR-006)
- [X] T004 [P] [US1] Update sidebar_position from 5 to 7 in docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-engineer.md (FR-007)

### Chapter 3 Fixes

- [X] T005 [P] [US1] Update sidebar_position from 6 to 8 in docs/module-1-robotic-nervous-system/chapter-3-urdf-modeling-explorer.md (FR-008)
- [X] T006 [P] [US1] Update sidebar_position from 7 to 9 in docs/module-1-robotic-nervous-system/chapter-3-urdf-modeling-builder.md (FR-009)
- [X] T007 [P] [US1] Update sidebar_position from 8 to 10 in docs/module-1-robotic-nervous-system/chapter-3-urdf-modeling-engineer.md (FR-010)

**Checkpoint**: All frontmatter updates complete

**CLI Validation**: `npx playwright test sidebar-order --reporter=list` → should PASS (green state)

---

## Phase 3: REFACTOR - Validation & Cleanup

**Goal**: Comprehensive validation using CLI automation

### Automated Validation

- [X] T008 [US1] Run Docusaurus build to verify no errors: `npm run build` (SC-003)
- [X] T009 [US1] Run full E2E test suite to ensure no regressions: `npx playwright test --reporter=list` (SC-004)
- [X] T010 [US1] Visual verification of sidebar navigation order using Playwright screenshot (SC-002)

**CLI Commands**:
```bash
# Build validation
npm run build

# Full E2E suite
npx playwright test --reporter=list

# Screenshot for visual validation (optional)
npx playwright test sidebar-order --update-snapshots
```

**Checkpoint**: Fix validated, all tests pass, ready for commit

---

## Dependencies & Execution Order

### Phase Dependencies (TDD Cycle)

```text
Phase 1 (RED)     → T001 must complete first (test written, fails)
Phase 2 (GREEN)   → T002-T007 can run in parallel (make test pass)
Phase 3 (REFACTOR) → T008-T010 run after Phase 2 (validation)
```

### Parallel Opportunities

All 6 fix tasks (T002-T007) can run in parallel as they modify different files with no dependencies.

```text
# Launch all fix tasks together:
Task T002: Update chapter-2-ros2-architecture-explorer.md (3→5)
Task T003: Update chapter-2-ros2-architecture-builder.md (4→6)
Task T004: Update chapter-2-ros2-architecture-engineer.md (5→7)
Task T005: Update chapter-3-urdf-modeling-explorer.md (6→8)
Task T006: Update chapter-3-urdf-modeling-builder.md (7→9)
Task T007: Update chapter-3-urdf-modeling-engineer.md (8→10)
```

---

## Implementation Strategy

### TDD Cycle

1. **RED**: Write test T001 → verify it FAILS
2. **GREEN**: Execute T002-T007 in parallel → verify test PASSES
3. **REFACTOR**: Run T008-T010 → ensure quality

### CLI Automation Summary

| Step | Command | Expected Result |
|------|---------|-----------------|
| Build | `npm run build` | Exit 0, no errors |
| Run specific test | `npx playwright test sidebar-order` | FAIL (RED), then PASS (GREEN) |
| Run all tests | `npx playwright test` | All pass |
| Serve for manual check | `npm run serve` | http://localhost:3000 |

### Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 10 |
| RED Phase | 1 |
| GREEN Phase (Parallelizable) | 6 (60%) |
| REFACTOR Phase | 3 |
| User Stories | 1 |
| Files Modified | 7 (6 chapters + 1 test) |

---

## Notes

- TDD approach ensures we have automated regression protection
- Playwright E2E test will catch future sidebar ordering issues
- All CLI commands can be automated in CI/CD pipeline
- Build verification ensures no breaking changes
- Visual check confirms navigation order is correct
