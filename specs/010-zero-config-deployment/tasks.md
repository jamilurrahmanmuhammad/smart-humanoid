# Tasks: Zero-Config Platform Deployment

**Input**: Design documents from `/specs/010-zero-config-deployment/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md

**Approach**: TDD (Test-Driven Development) - Tests written FIRST, implementation follows

**Organization**: Tasks grouped by TDD phase (RED → GREEN → REFACTOR), then by user story

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Config file**: `config-helpers.ts` (repository root)
- **Test files**: `tests/config/` (existing from feature 009)
- **Package config**: `package.json` (repository root)
- **Documentation**: `.env.example`, `specs/010-zero-config-deployment/quickstart.md`

---

## Phase 1: Setup (TDD Infrastructure)

**Purpose**: Ensure test infrastructure is ready (already exists from feature 009)

- [x] T001 Verify Jest configuration exists and works in `jest.config.js`
- [x] T002 Verify existing tests pass with `npm test` (CLI command)

---

## Phase 2: RED - Write Failing Tests (TDD)

**Purpose**: Write all tests FIRST - they MUST FAIL before implementation

**⚠️ CRITICAL**: Run tests after each task to confirm they FAIL

### Tests for CI Detection (US2: Environment Auto-Detection)

- [x] T003 [P] [US2] Write test: `isCI()` returns true when CI=true in `tests/config/ci-detection.test.ts`
- [x] T004 [P] [US2] Write test: `isCI()` returns false when CI not set in `tests/config/ci-detection.test.ts`
- [x] T005 [P] [US2] Write test: `isCI()` returns false when CI=false in `tests/config/ci-detection.test.ts`

### Tests for package.json Standards (US4: Framework Configuration Discovery)

- [x] T006 [P] [US4] Write test: package.json has `engines.node` >= 20 in `tests/config/package-standards.test.ts`
- [x] T007 [P] [US4] Write test: package.json has `scripts.build` = "docusaurus build" in `tests/config/package-standards.test.ts`
- [x] T008 [P] [US4] Write test: package.json has `scripts.start` = "docusaurus start" in `tests/config/package-standards.test.ts`

### Tests for Local Development (US3: Local Development Parity)

- [x] T009 [P] [US3] Write test: `getConfig()` returns localhost defaults when no env vars in `tests/config/env-config.test.ts` (may already exist)
- [x] T010 [P] [US3] Write test: config works with no CI var set (local mode) in `tests/config/ci-detection.test.ts`

### Tests for Build Validation (US1: One-Click Repository Import)

- [x] T011 [P] [US1] Write test: build output directory is `build/` (Docusaurus default) in `tests/config/build-config.test.ts`
- [x] T012 [US1] Run tests - verify all new tests FAIL (RED phase validation via CLI)

**Checkpoint**: All tests written and FAILING (RED phase complete)

---

## Phase 3: GREEN - Make Tests Pass (Implementation)

**Purpose**: Implement minimum code to make all tests pass

### Core CI Detection Implementation (US2)

- [x] T013 [US2] Add `isCI()` function to `config-helpers.ts`
- [x] T014 [US2] Export `isCI()` from `config-helpers.ts`
- [x] T015 [US2] Run CI detection tests - verify they PASS (CLI: `npm test -- --testPathPattern=ci-detection`)

### Package.json Verification/Update (US4)

- [x] T016 [US4] Verify `engines.node` field exists and is `>=20.0` in `package.json`
- [x] T017 [US4] Verify `scripts.build` is `docusaurus build` in `package.json`
- [x] T018 [US4] Verify `scripts.start` is `docusaurus start` in `package.json`
- [x] T019 [US4] Run package standards tests - verify they PASS (CLI: `npm test -- --testPathPattern=package-standards`)

### Local Development Verification (US3)

- [x] T020 [US3] Verify `getConfig()` uses localhost defaults when no env vars in `config-helpers.ts`
- [x] T021 [US3] Run local development tests - verify they PASS

### Build Validation (US1)

- [x] T022 [US1] Verify Docusaurus build outputs to `build/` directory (CLI: `npm run build && ls -la build/`)
- [x] T023 [US1] Run all tests - verify they PASS (CLI: `npm test`)

**Checkpoint**: All tests passing (GREEN phase complete)

---

## Phase 4: REFACTOR - Clean Up & Documentation

**Purpose**: Improve code quality and documentation without changing behavior

- [x] T024 [P] Update `.env.example` with CI detection documentation
- [x] T025 [P] Verify `specs/010-zero-config-deployment/quickstart.md` is complete and accurate
- [x] T026 [P] Add JSDoc comments to `isCI()` function in `config-helpers.ts`
- [x] T027 Run all tests again - verify still PASS after refactoring (CLI: `npm test`)

---

## Phase 5: Validation - Multi-Environment Testing

**Purpose**: Validate the implementation works across different environments

### Local Development Validation (US3)

- [x] T028 [US3] Verify `npm start` works without any env vars (CLI command)
- [x] T029 [US3] Verify `npm run build` works without any env vars (CLI command)

### CI Environment Simulation (US2)

- [x] T030 [US2] Test build with CI=true: `CI=true npm run build` (CLI command)
- [x] T031 [US2] Verify build succeeds in simulated CI mode

### Custom URL Configuration (US1 + US2)

- [x] T032 [US1] Test with custom SITE_URL: `SITE_URL=https://example.com npm run build` (CLI command)
- [x] T033 [US1] Test with custom BASE_URL: `BASE_URL=/docs/ npm run build` (CLI command)
- [x] T034 [US1] Verify generated HTML contains correct URLs (CLI: `grep -r "example.com" build/`)

**Checkpoint**: All validation scenarios pass

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final documentation and cleanup

- [x] T035 [P] Add test scripts to `package.json` if not present (`test:ci-detection`, etc.)
- [x] T036 [P] Update `specs/010-zero-config-deployment/checklists/requirements.md` marking completed items
- [x] T037 Run full test suite: `npm test` (final validation)
- [x] T038 Verify build: `npm run build` (final validation)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - verify existing infrastructure
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

### User Story Dependencies

- **US1 (One-Click Import)**: Depends on US2 and US4 for environment detection and package config
- **US2 (Environment Auto-Detection)**: Independent - core CI detection
- **US3 (Local Development Parity)**: Independent - uses existing defaults
- **US4 (Framework Configuration Discovery)**: Independent - package.json validation

### Parallel Opportunities

**Phase 2 (RED)**: All test tasks T003-T011 can run in parallel (different test files)

**Phase 4 (REFACTOR)**: T024, T025, T026 can run in parallel (different files)

**Phase 6 (Polish)**: T035, T036 can run in parallel (different files)

---

## Parallel Example: Phase 2 Tests

```bash
# All these tests can be written in parallel (different files):
Task T003: "Write test: isCI() returns true when CI=true"
Task T004: "Write test: isCI() returns false when CI not set"
Task T006: "Write test: package.json has engines.node >= 20"
Task T007: "Write test: package.json has scripts.build"
Task T011: "Write test: build output directory is build/"
```

---

## Implementation Strategy

### MVP First (US2 + US4 - Core Infrastructure)

1. Complete Phase 1: Setup (verify Jest works)
2. Complete Phase 2: RED (write failing tests for US2 + US4)
3. Complete Phase 3: GREEN (implement `isCI()`, verify package.json)
4. **STOP and VALIDATE**: Run tests, verify all pass
5. Deploy/demo if ready - core zero-config functionality complete

### Full Feature

1. Complete MVP above
2. Add Phase 4: REFACTOR (documentation, cleanup)
3. Add Phase 5: Validation (multi-environment testing)
4. Add Phase 6: Polish (final touches)

---

## User Story Mapping

| Task Range | User Story | Description |
|------------|------------|-------------|
| T003-T005, T013-T015, T030-T031 | US2 | Environment Auto-Detection (CI=true) |
| T006-T008, T016-T019 | US4 | Framework Configuration Discovery (package.json) |
| T009-T010, T020-T021, T028-T029 | US3 | Local Development Parity |
| T011-T012, T022-T023, T032-T034 | US1 | One-Click Repository Import |

---

## Notes

- TDD approach: Write tests FIRST, see them FAIL, then implement
- [P] tasks = can run in parallel
- User stories US1+US2 are P1 priority (core functionality)
- User stories US3+US4 are P2 priority (supporting functionality)
- All validation in Phase 5 uses CLI commands per user request
- Commit after each phase completes
