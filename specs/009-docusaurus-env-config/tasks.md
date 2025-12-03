# Tasks: Docusaurus Environment Configuration

**Input**: Design documents from `/specs/009-docusaurus-env-config/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md

**Approach**: TDD (Test-Driven Development) - Tests written FIRST, implementation follows

**Organization**: Tasks grouped by TDD phase, then by user story

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Config file**: `docusaurus.config.ts` (repository root)
- **Test files**: `tests/config/` (new directory)
- **Documentation**: `.env.example` (repository root)

---

## Phase 1: Setup (Test Infrastructure)

**Purpose**: Configure Jest for testing Docusaurus config

- [x] T001 Create test directory structure at `tests/config/`
- [x] T002 Configure Jest for TypeScript config testing in `jest.config.js`
- [x] T003 Add Jest and ts-jest as devDependencies in `package.json`

---

## Phase 2: RED - Write Failing Tests (TDD)

**Purpose**: Write all tests FIRST - they MUST FAIL before implementation

**⚠️ CRITICAL**: Run tests after each task to confirm they FAIL

### Tests for Core Configuration (US1 + US2 combined)

- [x] T004 [P] [US1] Write test: default SITE_URL is `http://localhost:3000` when env var not set in `tests/config/env-config.test.ts`
- [x] T005 [P] [US2] Write test: default BASE_URL is `/` when env var not set in `tests/config/env-config.test.ts`
- [x] T006 [P] [US1] Write test: SITE_URL env var overrides default in `tests/config/env-config.test.ts`
- [x] T007 [P] [US2] Write test: BASE_URL env var overrides default in `tests/config/env-config.test.ts`

### Tests for Validation (Edge Cases)

- [x] T008 [P] [US1] Write test: SITE_URL without protocol throws error in `tests/config/env-config.test.ts`
- [x] T009 [P] [US2] Write test: BASE_URL without leading slash throws error in `tests/config/env-config.test.ts`
- [x] T010 [P] [US2] Write test: BASE_URL gets trailing slash normalized in `tests/config/env-config.test.ts`

### Tests for Local Development (US4)

- [x] T011 [P] [US4] Write test: config loads without any env vars set in `tests/config/env-config.test.ts`
- [x] T012 [P] [US4] Write test: npm start works with default config (integration) in `tests/config/env-config.test.ts`

**Checkpoint**: All tests written and FAILING (RED phase complete)

---

## Phase 3: GREEN - Make Tests Pass (Implementation)

**Purpose**: Implement minimum code to make all tests pass

### Core Implementation

- [x] T013 Create validation helper functions (validateUrl, validateBaseUrl) in `config-helpers.ts`
- [x] T014 [US1] Replace hardcoded `url` with `process.env.SITE_URL || 'http://localhost:3000'` in `docusaurus.config.ts`
- [x] T015 [US2] Replace hardcoded `baseUrl` with `process.env.BASE_URL || '/'` in `docusaurus.config.ts`
- [x] T016 Add validation calls for SITE_URL and BASE_URL in `docusaurus.config.ts`
- [x] T017 Run all tests - verify they PASS

**Checkpoint**: All tests passing (GREEN phase complete)

---

## Phase 4: REFACTOR - Clean Up & Documentation

**Purpose**: Improve code quality without changing behavior

- [x] T018 [P] Extract config helpers to separate file if needed (optional refactor) - created config-helpers.ts
- [x] T019 [P] Create `.env.example` with documented environment variables - updated existing file
- [x] T020 [P] Update quickstart.md with final implementation details in `specs/009-docusaurus-env-config/quickstart.md`

---

## Phase 5: Validation & Multi-Environment Testing (US3)

**Purpose**: Verify the implementation works across different environments

**Goal**: Confirm same build process works with different env configs

**Independent Test**: Run builds with staging vs production configs

- [x] T021 [US3] Test build with staging config: `SITE_URL=https://staging.example.com BASE_URL=/` (CLI)
- [x] T022 [US3] Test build with production config: `SITE_URL=https://docs.example.com BASE_URL=/smart-humanoid/` (CLI)
- [x] T023 [US3] Verify generated HTML contains correct URLs for each build
- [x] T024 [US4] Verify `npm start` works without any env vars set (local dev) - defaults work
- [x] T025 [US4] Verify `npm run build` works without any env vars set (default build)

**Checkpoint**: All user stories validated

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final documentation and cleanup

- [x] T026 [P] Add test script to `package.json` for config tests
- [x] T027 [P] Update CLAUDE.md if new active technologies (optional) - N/A, no new active tech
- [x] T028 Run full test suite and verify no regressions - 15/15 tests pass
- [x] T029 Run `npm run build` final validation - builds with defaults work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (RED)**: Depends on Phase 1 - tests need Jest configured
- **Phase 3 (GREEN)**: Depends on Phase 2 - tests must exist and FAIL first
- **Phase 4 (REFACTOR)**: Depends on Phase 3 - tests must PASS first
- **Phase 5 (Validation)**: Depends on Phase 3 - implementation must be complete
- **Phase 6 (Polish)**: Depends on Phase 5 - all validation complete

### TDD Flow

```
Phase 1 (Setup) → Phase 2 (RED: tests fail) → Phase 3 (GREEN: tests pass) → Phase 4 (REFACTOR)
                                                                              ↓
                                                        Phase 5 (Validation) → Phase 6 (Polish)
```

### Parallel Opportunities

**Phase 2 (RED)**: All test tasks T004-T012 can run in parallel (different test cases, same file)

**Phase 4 (REFACTOR)**: T018, T019, T020 can run in parallel (different files)

**Phase 6 (Polish)**: T026, T027 can run in parallel (different files)

---

## Parallel Example: Phase 2 Tests

```bash
# All these tests can be written in parallel (same file, different test cases):
Task T004: "Write test: default SITE_URL..."
Task T005: "Write test: default BASE_URL..."
Task T006: "Write test: SITE_URL env var overrides..."
Task T007: "Write test: BASE_URL env var overrides..."
Task T008: "Write test: SITE_URL without protocol throws..."
Task T009: "Write test: BASE_URL without leading slash throws..."
```

---

## Implementation Strategy

### MVP First (Core Config - US1 + US2)

1. Complete Phase 1: Setup (Jest configuration)
2. Complete Phase 2: RED (write failing tests for T004-T010)
3. Complete Phase 3: GREEN (implement T013-T017)
4. **STOP and VALIDATE**: Run tests, verify all pass
5. Deploy/demo if ready - core functionality complete

### Full Feature

1. Complete MVP above
2. Add Phase 4: REFACTOR (documentation, cleanup)
3. Add Phase 5: Validation (multi-environment testing)
4. Add Phase 6: Polish (final touches)

---

## User Story Mapping

| Task Range | User Story | Description |
|------------|------------|-------------|
| T004, T006, T008 | US1 | Deploy to Custom Domain (SITE_URL) |
| T005, T007, T009, T010 | US2 | Deploy to Subdirectory (BASE_URL) |
| T021-T023 | US3 | Multi-Environment Deployment |
| T011, T012, T024, T025 | US4 | Local Development |

---

## Notes

- TDD approach: Write tests FIRST, see them FAIL, then implement
- [P] tasks = can run in parallel
- US1 and US2 are tightly coupled (same config file) - implemented together
- US3 and US4 are validation of core functionality
- All validation in Phase 5 uses CLI commands per user request
- Commit after each phase completes
