# Tasks: Hierarchical Documentation Structure

**Input**: Design documents from `/specs/003-docs-structure-user-story-3/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅

**Tests**: E2E tests will be updated (not TDD - tests already exist)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No setup needed - project already initialized with Docusaurus

**Status**: ✅ Complete (existing project)

---

## Phase 2: Foundational (Cleanup Old Structure)

**Purpose**: Remove old sibling structure to make way for hierarchical structure

**⚠️ CRITICAL**: Must complete before creating new module directories

- [ ] T001 Remove old `docs/modules/` directory (backup content first if needed)
- [ ] T002 Remove old `docs/chapters/` directory (backup content first if needed)
- [ ] T003 Run `npm run build` to verify docs still builds after removal

**Checkpoint**: Old structure removed, ready for new hierarchical structure

---

## Phase 3: User Story 3.1 - Hierarchical Content Structure (Priority: P1) 🎯 MVP

**Goal**: Create 4 module directories with proper hierarchy where chapters will be nested inside modules

**Independent Test**: Navigate to `/docs/intro` and verify sidebar shows 4 expandable module categories

### Implementation for User Story 3.1

- [ ] T004 [P] [US1] Create `docs/module-1-robotic-nervous-system/_category_.json` with label and position 2
- [ ] T005 [P] [US1] Create `docs/module-1-robotic-nervous-system/index.md` module landing page
- [ ] T006 [P] [US1] Create `docs/module-2-digital-twin/_category_.json` with label and position 3
- [ ] T007 [P] [US1] Create `docs/module-2-digital-twin/index.md` module landing page
- [ ] T008 [P] [US1] Create `docs/module-3-ai-robot-brain/_category_.json` with label and position 4
- [ ] T009 [P] [US1] Create `docs/module-3-ai-robot-brain/index.md` module landing page
- [ ] T010 [P] [US1] Create `docs/module-4-vision-language-action/_category_.json` with label and position 5
- [ ] T011 [P] [US1] Create `docs/module-4-vision-language-action/index.md` module landing page
- [ ] T012 [US1] Run `npm run build` to verify all modules render correctly
- [ ] T013 [US1] Verify sidebar displays 4 expandable module categories using browser

**Checkpoint**: 4 module directories created with proper _category_.json and index.md files

---

## Phase 4: User Story 3.2 - Sidebar Navigation Verification (Priority: P2)

**Goal**: Update E2E tests to verify sidebar displays modules as expandable categories with proper hierarchy

**Independent Test**: Run `npx playwright test tests/e2e/docs.spec.ts` - all tests pass

### Implementation for User Story 3.2

- [ ] T014 [US2] Update `tests/e2e/docs.spec.ts` test for "Modules" category to match new module names
- [ ] T015 [US2] Update `tests/e2e/docs.spec.ts` test for "Chapters" - remove or update (chapters now inside modules)
- [ ] T016 [US2] Run `npx playwright test tests/e2e/docs.spec.ts` to verify docs tests pass
- [ ] T017 [US2] Run `npx playwright test` to verify all 17 E2E tests pass

**Checkpoint**: All E2E tests pass with new hierarchical structure

---

## Phase 5: Polish & Validation

**Purpose**: Final verification and cleanup

- [ ] T018 Run `npm run build` and verify zero errors and zero warnings
- [ ] T019 Verify sidebar displays Module 1, Module 2, Module 3, Module 4 as expandable categories
- [ ] T020 Verify clicking module name navigates to module index page
- [ ] T021 Verify no `docs/modules/` or `docs/chapters/` directories exist
- [ ] T022 Run full test suite: `npx playwright test` - all 17 tests pass

**Checkpoint**: Feature complete, ready for commit

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 2)**: No dependencies - start immediately
- **User Story 3.1 (Phase 3)**: Depends on Foundational completion
- **User Story 3.2 (Phase 4)**: Depends on User Story 3.1 completion
- **Polish (Phase 5)**: Depends on all phases complete

### Task Dependencies Within Phases

**Phase 2 (Foundational)**:
- T001 → T002 → T003 (sequential - verify after each removal)

**Phase 3 (User Story 3.1)**:
- T004-T011 can run in parallel [P] (different directories)
- T012 depends on T004-T011 (build verification)
- T013 depends on T012 (visual verification)

**Phase 4 (User Story 3.2)**:
- T014-T015 can run in parallel [P] (same file but different tests)
- T016 depends on T014-T015 (test execution)
- T017 depends on T016 (full suite)

### Parallel Opportunities

```text
Phase 3 Parallel Group (after Phase 2 complete):
├── T004 + T005 (Module 1)
├── T006 + T007 (Module 2)
├── T008 + T009 (Module 3)
└── T010 + T011 (Module 4)
```

---

## Implementation Strategy

### MVP First (User Story 3.1 Only)

1. Complete Phase 2: Remove old structure
2. Complete Phase 3: Create 4 module directories
3. **STOP and VALIDATE**: Verify sidebar shows expandable modules
4. Build succeeds, sidebar renders correctly

### Full Implementation

1. Phase 2 → Phase 3 → Phase 4 → Phase 5
2. Total: 22 tasks
3. Estimated parallelization: 8 tasks can run in parallel (T004-T011)

---

## Summary

| Phase | Tasks | Parallel | Description |
|-------|-------|----------|-------------|
| Phase 2 | 3 | 0 | Cleanup old structure |
| Phase 3 (US1) | 10 | 8 | Create hierarchical modules |
| Phase 4 (US2) | 4 | 2 | Update E2E tests |
| Phase 5 | 5 | 0 | Final validation |
| **Total** | **22** | **10** | |

---

## Notes

- [P] tasks = different files, no dependencies
- [US1] = User Story 3.1 (Hierarchical Content Structure)
- [US2] = User Story 3.2 (Sidebar Navigation)
- Commit after each phase completion
- Stop at any checkpoint to validate independently
