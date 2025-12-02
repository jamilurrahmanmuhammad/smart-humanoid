# Tasks: Docusaurus Platform Setup

**Input**: Design documents from `/specs/001-docusaurus-setup/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md

**Tests**: TDD approach requested - tests written FIRST and must FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: Docusaurus at repository root
- Paths: `src/`, `docs/`, `static/`, `i18n/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, Docusaurus bootstrap, and testing infrastructure

- [x] T001 Verify Node.js >= 18 is installed via CLI
- [x] T002 Initialize Docusaurus 3.x with TypeScript at repository root: `npx create-docusaurus@latest . classic --typescript`
- [x] T003 [P] Remove default blog content (delete `/blog/` directory)
- [x] T004 [P] Configure `tsconfig.json` for strict TypeScript
- [x] T005 Install Playwright as dev dependency: `npm install -D @playwright/test`
- [x] T006 [P] Create `playwright.config.ts` with webServer config for localhost:3000
- [x] T007 [P] Create `tests/e2e/` directory structure for Playwright tests

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core configuration and theme setup that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Configure `docusaurus.config.ts` with project metadata: title "Smart Humanoid", tagline "Build robots that understand the physical world"
- [x] T009 [P] Configure dark mode as default, disable theme switch toggle in `docusaurus.config.ts`
- [x] T010 [P] Create `src/css/custom.css` with CSS custom properties: `--ifm-background-color: #0D0D0F`, `--ifm-color-primary: #4ECFFE`
- [x] T011 [P] Configure full Infima token system in `src/css/custom.css` per research.md
- [x] T012 [P] Create `.env.example` with all feature flags disabled (ENABLE_AUTH, ENABLE_LLM, ENABLE_VECTOR_SEARCH, ENABLE_ANALYTICS)
- [x] T013 [P] Create `src/config/features.ts` reading feature flags from environment
- [x] T014 Verify `npm run build` succeeds with zero warnings

**Checkpoint**: Foundation ready - Docusaurus builds with dark theme, user story implementation can now begin

---

## Phase 3: User Story 1 - View Styled Landing Page (Priority: P1) 🎯 MVP

**Goal**: Professionally styled landing page with dark theme and modern hero section

**Independent Test**: Navigate to homepage, verify dark background (#0D0D0F) visible, hero section with headline and CTAs present

### Tests for User Story 1 (TDD - Write FIRST, must FAIL) ⚠️

- [x] T015 [P] [US1] E2E test: homepage loads with dark background color in `tests/e2e/homepage.spec.ts`
- [x] T016 [P] [US1] E2E test: hero section displays platform label "SMART HUMANOID" in `tests/e2e/homepage.spec.ts`
- [x] T017 [P] [US1] E2E test: hero headline contains "understand" with cyan highlight in `tests/e2e/homepage.spec.ts`
- [x] T018 [P] [US1] E2E test: two CTA buttons ("Get Started", "Browse Content") are present and keyboard accessible in `tests/e2e/homepage.spec.ts`
- [x] T019 [P] [US1] E2E test: hero section occupies 50-60% viewport height on desktop (1920x1080) in `tests/e2e/homepage.spec.ts`
- [x] T020 [P] [US1] E2E test: diagram placeholder visible on right side of hero in `tests/e2e/homepage.spec.ts`
- [x] T021 [US1] Run tests - verify ALL tests FAIL (RED phase)

### Implementation for User Story 1 (GREEN phase)

- [x] T022 [P] [US1] Create `src/components/Hero/index.tsx` with platform label, headline, subheading, and CTA buttons
- [x] T023 [P] [US1] Create `src/components/Hero/styles.module.css` with flex layout, typography, and spacing
- [x] T024 [US1] Add animated underline CSS keyframes for "understand" highlight in `src/components/Hero/styles.module.css`
- [x] T025 [US1] Add `prefers-reduced-motion` media query to disable animation for accessibility in `src/components/Hero/styles.module.css`
- [x] T026 [US1] Create diagram placeholder component in `src/components/Hero/DiagramPlaceholder.tsx` (integrated into Hero component)
- [x] T027 [US1] Create `src/pages/index.tsx` using Hero component as above-the-fold content
- [x] T028 [US1] Remove default Docusaurus homepage template content from `src/pages/index.tsx`
- [x] T029 [US1] Add ARIA labels and roles to Hero component for accessibility
- [x] T030 [US1] Run tests - verify ALL tests PASS (GREEN phase)

### Refactor for User Story 1 (REFACTOR phase)

- [x] T031 [US1] Review Hero component code for DRY principles and clean up any duplication
- [x] T032 [US1] Validate color contrast meets WCAG 2.1 AA (4.5:1 minimum) using MCP Playwright

**Checkpoint**: User Story 1 complete - Homepage displays dark-themed hero section with all elements

---

## Phase 4: User Story 2 - Navigate Platform Structure (Priority: P2)

**Goal**: Navigation bar with menu items for different content areas

**Independent Test**: View navbar, verify "Learn Free", "Labs", "Personalize" items present, search placeholder and GitHub icon visible

### Tests for User Story 2 (TDD - Write FIRST, must FAIL) ⚠️

- [ ] T033 [P] [US2] E2E test: navbar displays "Learn Free" menu item linking to /docs/intro in `tests/e2e/navigation.spec.ts`
- [ ] T034 [P] [US2] E2E test: navbar displays "Labs" menu item (disabled placeholder) in `tests/e2e/navigation.spec.ts`
- [ ] T035 [P] [US2] E2E test: navbar displays "Personalize" menu item (disabled placeholder) in `tests/e2e/navigation.spec.ts`
- [ ] T036 [P] [US2] E2E test: navbar displays search box placeholder on right side in `tests/e2e/navigation.spec.ts`
- [ ] T037 [P] [US2] E2E test: navbar displays GitHub repository link icon on far right in `tests/e2e/navigation.spec.ts`
- [ ] T038 [P] [US2] E2E test: navbar is transparent over dark background in `tests/e2e/navigation.spec.ts`
- [ ] T039 [P] [US2] E2E test: menu items show hover feedback in `tests/e2e/navigation.spec.ts`
- [ ] T040 [US2] Run tests - verify ALL tests FAIL (RED phase)

### Implementation for User Story 2 (GREEN phase)

- [ ] T041 [US2] Configure navbar items in `docusaurus.config.ts`: "Learn Free" -> /docs/intro
- [ ] T042 [P] [US2] Create `src/components/placeholders/PersonalizeButton.tsx` with disabled state and "Coming Soon" tooltip
- [ ] T043 [P] [US2] Create `src/components/placeholders/LabsButton.tsx` with disabled state and "Coming Soon" tooltip
- [ ] T044 [US2] Add navbar items for Labs and Personalize placeholders in `docusaurus.config.ts`
- [ ] T045 [US2] Configure search box placeholder in navbar in `docusaurus.config.ts`
- [ ] T046 [US2] Add GitHub repository link icon to navbar in `docusaurus.config.ts`
- [ ] T047 [US2] Style navbar transparent background in `src/css/custom.css`: `--ifm-navbar-background-color: transparent`
- [ ] T048 [US2] Add ARIA labels to placeholder buttons for accessibility ("Coming Soon" announcement)
- [ ] T049 [US2] Run tests - verify ALL tests PASS (GREEN phase)

### Refactor for User Story 2 (REFACTOR phase)

- [ ] T050 [US2] Extract shared placeholder button logic to `src/components/placeholders/PlaceholderButton.tsx` if duplicated
- [ ] T051 [US2] Verify all 5 navbar elements keyboard accessible using MCP Playwright

**Checkpoint**: User Story 2 complete - Full navigation visible with all 5 elements

---

## Phase 5: User Story 3 - Access Book Content Structure (Priority: P3)

**Goal**: Pre-configured documentation folder structure for book content

**Independent Test**: Navigate to /docs, verify sidebar shows hierarchy, folder structure exists

### Tests for User Story 3 (TDD - Write FIRST, must FAIL) ⚠️

- [ ] T052 [P] [US3] E2E test: /docs route loads intro page successfully in `tests/e2e/docs.spec.ts`
- [ ] T053 [P] [US3] E2E test: sidebar displays with auto-generated hierarchy in `tests/e2e/docs.spec.ts`
- [ ] T054 [P] [US3] E2E test: sidebar shows "modules" category in `tests/e2e/docs.spec.ts`
- [ ] T055 [P] [US3] E2E test: sidebar shows "chapters" category in `tests/e2e/docs.spec.ts`
- [ ] T056 [US3] Run tests - verify ALL tests FAIL (RED phase)

### Implementation for User Story 3 (GREEN phase)

- [ ] T057 [US3] Create `docs/intro.md` with placeholder content and frontmatter including safety metadata fields
- [ ] T058 [P] [US3] Create `docs/modules/.gitkeep` for modules section
- [ ] T059 [P] [US3] Create `docs/chapters/.gitkeep` for chapters section
- [ ] T060 [P] [US3] Create `docs/rag/.gitkeep` and `docs/rag/_index.json` placeholder for RAG manifest
- [ ] T061 [P] [US3] Create `docs/assets/.gitkeep` for static assets
- [ ] T062 [US3] Configure `sidebars.ts` for auto-generation based on folder structure
- [ ] T063 [US3] Run tests - verify ALL tests PASS (GREEN phase)

### Refactor for User Story 3 (REFACTOR phase)

- [ ] T064 [US3] Verify docs plugin configuration supports adding a second book instance without core config changes

**Checkpoint**: User Story 3 complete - Documentation structure ready for content

---

## Phase 6: User Story 4 - Deploy Platform Automatically (Priority: P4)

**Goal**: Automated deployment workflow for GitHub Pages

**Independent Test**: Push to main branch, verify deployment workflow triggers and site builds successfully

### Tests for User Story 4 (TDD - Write FIRST, must FAIL) ⚠️

- [ ] T065 [P] [US4] Validation test: `.github/workflows/deploy.yml` exists with correct structure
- [ ] T066 [P] [US4] Validation test: `docusaurus.config.ts` contains valid `url` and `baseUrl` settings
- [ ] T067 [US4] Run validation tests - verify tests FAIL (RED phase)

### Implementation for User Story 4 (GREEN phase)

- [ ] T068 [US4] Create `.github/workflows/deploy.yml` with GitHub Pages deployment using peaceiris/actions-gh-pages@v3
- [ ] T069 [US4] Configure `url` and `baseUrl` in `docusaurus.config.ts` for GitHub Pages
- [ ] T070 [US4] Add build step validation in workflow (npm run build must succeed)
- [ ] T071 [US4] Run validation tests - verify tests PASS (GREEN phase)

**Checkpoint**: User Story 4 complete - Deployment workflow configured

---

## Phase 7: User Story 5 - Verify UI Components (Priority: P5)

**Goal**: Automated tests to verify key UI components render correctly

**Independent Test**: Run `npx playwright test`, verify all tests pass

### Tests for User Story 5 (Already created in US1-US3, validate comprehensive coverage) ⚠️

- [ ] T072 [US5] Review all E2E tests for comprehensive coverage of FR-038 (navbar), FR-039 (hero), FR-040 (buttons accessible)
- [ ] T073 [US5] Add axe-core accessibility audit to `tests/e2e/accessibility.spec.ts` for WCAG 2.1 AA compliance
- [ ] T074 [P] [US5] Add responsive viewport tests at 1920x1080, 768x1024, 375x667 in `tests/e2e/responsive.spec.ts`

### Implementation for User Story 5 (GREEN phase)

- [ ] T075 [US5] Install @axe-core/playwright: `npm install -D @axe-core/playwright`
- [ ] T076 [US5] Create `tests/e2e/accessibility.spec.ts` with axe-core audit
- [ ] T077 [US5] Create `tests/e2e/responsive.spec.ts` with viewport resize tests
- [ ] T078 [US5] Add `test` script to `package.json`: `npx playwright test`
- [ ] T079 [US5] Run full test suite - verify ALL tests PASS

**Checkpoint**: User Story 5 complete - Full test coverage established

---

## Phase 8: Plugin Architecture & Constitution Compliance

**Purpose**: Enable frictionless future extensions and ensure constitution compliance

- [ ] T080 [P] Create `src/providers/types.ts` with TypeScript interfaces: IAuthProvider, ILLMProvider, IVectorProvider, IDataProvider
- [ ] T081 [P] Create `src/providers/README.md` documenting how to add providers
- [ ] T082 [P] Create `src/providers/index.ts` exporting provider types
- [ ] T083 [P] Create `src/hooks/useFeatureFlag.ts` hook for checking feature flags
- [ ] T084 [P] Create `src/components/placeholders/TryWithAI.tsx` disabled placeholder
- [ ] T085 [P] Create `src/components/placeholders/TranslateButton.tsx` disabled placeholder with locale dropdown

---

## Phase 9: i18n & RTL Scaffold

**Purpose**: Prepare for Urdu translation (constitution requirement)

- [ ] T086 [P] Create `i18n/ur/docusaurus-theme-classic/navbar.json` placeholder
- [ ] T087 [P] Add RTL-ready CSS to `src/css/custom.css`: `[dir='rtl']` selectors
- [ ] T088 [P] Configure i18n in `docusaurus.config.ts` (disabled by default, ur locale registered)

---

## Phase 10: Reusable Intelligence Scaffold

**Purpose**: Constitution compliance for skills and subagents directories

- [ ] T089 [P] Create `src/skills/README.md` explaining future skill registration
- [ ] T090 [P] Create `src/skills/_registry.ts` placeholder for skill manifest
- [ ] T091 [P] Create `src/subagents/README.md` explaining future subagent configuration
- [ ] T092 [P] Create `src/subagents/_registry.ts` placeholder for subagent manifest

---

## Phase 11: Polish & Final Validation

**Purpose**: Final checks and cross-cutting improvements

- [ ] T093 Run `npm run build` - verify zero warnings
- [ ] T094 Run full Playwright test suite - verify ALL tests pass
- [ ] T095 [P] Validate with MCP Playwright: browser_snapshot for accessibility tree
- [ ] T096 [P] Validate with MCP Playwright: browser_take_screenshot for visual verification
- [ ] T097 Test responsive layout at 320px, 768px, 1920px viewports using MCP Playwright browser_resize
- [ ] T098 Verify keyboard navigation works for all interactive elements
- [ ] T099 Final constitution compliance checklist validation against plan.md Section "Constitution Check"

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in priority order (P1 → P2 → P3 → P4 → P5)
  - Each story follows TDD cycle: RED → GREEN → REFACTOR
- **Plugin Architecture (Phase 8)**: Can run in parallel with User Stories after Foundational
- **i18n Scaffold (Phase 9)**: Can run in parallel with User Stories after Foundational
- **Reusable Intelligence (Phase 10)**: Can run in parallel with User Stories after Foundational
- **Polish (Phase 11)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after US1 completion (navbar requires homepage context)
- **User Story 3 (P3)**: Can start after Foundational - Independent of US1/US2
- **User Story 4 (P4)**: Can start after US3 completion (needs docs structure for meaningful deploy)
- **User Story 5 (P5)**: Depends on US1-US4 completion (tests verify all implemented features)

### TDD Cycle Per User Story

1. Write all test cases (RED phase) - tests MUST FAIL
2. Implement minimum code to pass tests (GREEN phase)
3. Refactor for quality (REFACTOR phase)
4. Move to next user story

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- All tests within a user story marked [P] can run in parallel
- Phase 8, 9, 10 can run in parallel with user stories after Foundational
- Models within a story marked [P] can run in parallel

---

## Parallel Example: User Story 1 Tests (RED phase)

```bash
# Launch all tests for User Story 1 together (TDD RED phase):
# These run in parallel as they test different aspects of the homepage

Task: "E2E test: homepage loads with dark background color"
Task: "E2E test: hero section displays platform label"
Task: "E2E test: hero headline contains 'understand' with cyan highlight"
Task: "E2E test: two CTA buttons are present and keyboard accessible"
Task: "E2E test: hero section occupies 50-60% viewport height"
Task: "E2E test: diagram placeholder visible on right side"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (TDD: RED → GREEN → REFACTOR)
4. **STOP and VALIDATE**: Homepage works independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Deployment automated
6. Add User Story 5 → Full test coverage
7. Each story adds value without breaking previous stories

### CLI Automation Preference

Per user request, prefer CLI automation:
- Use `npm` commands for dependency installation
- Use `npx playwright test` for test execution
- Use `npm run build` for build validation
- Use MCP Playwright for browser-based validation

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 99 |
| Phase 1 (Setup) | 7 |
| Phase 2 (Foundational) | 7 |
| User Story 1 (P1) | 18 |
| User Story 2 (P2) | 19 |
| User Story 3 (P3) | 13 |
| User Story 4 (P4) | 7 |
| User Story 5 (P5) | 8 |
| Phase 8-10 (Architecture/Scaffolds) | 13 |
| Phase 11 (Polish) | 7 |
| Parallel Tasks [P] | 55 |

**MVP Scope**: Phase 1 + Phase 2 + User Story 1 = 32 tasks
**Full Implementation**: 99 tasks

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story follows TDD cycle: RED (write failing tests) → GREEN (implement to pass) → REFACTOR
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MCP Playwright used for browser-based validation (accessibility, visual, responsive)
- CLI automation preferred per user request
