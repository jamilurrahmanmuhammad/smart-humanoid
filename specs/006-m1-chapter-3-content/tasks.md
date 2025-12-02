# Tasks: Module 1 Chapter 3 - Humanoid Robot Modeling with URDF

**Input**: Design documents from `/specs/006-m1-chapter-3-content/`
**Prerequisites**: plan.md, spec.md, research.md

**Organization**: Tasks organized by content creation phases and user stories for three chapter variants.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task addresses (US1-US6)
- Include exact file paths in descriptions

## Path Conventions

- **Content Output**: `docs/module-1-robotic-nervous-system/`
- **Specs**: `specs/006-m1-chapter-3-content/`

---

## Phase 1: Setup (Chapter File Creation)

**Purpose**: Create chapter files with frontmatter for all three variants

- [X] T001 [P] Create Explorer chapter file with frontmatter in docs/module-1-robotic-nervous-system/chapter-3-urdf-modeling-explorer.md (FR-027, FR-028, FR-038)
- [X] T002 [P] Create Builder chapter file with frontmatter in docs/module-1-robotic-nervous-system/chapter-3-urdf-modeling-builder.md (FR-027, FR-029, FR-038)
- [X] T003 [P] Create Engineer chapter file with frontmatter in docs/module-1-robotic-nervous-system/chapter-3-urdf-modeling-engineer.md (FR-027, FR-030, FR-038)

**Checkpoint**: All three chapter files exist with correct frontmatter (sidebar_position, title, safety, prerequisites, personaDifficulty, learningPath, personalizationTags, ragKeywords)

---

## Phase 2: Opening & Learning Objectives (All Variants)

**Purpose**: Write opening hook and learning objectives for all variants

- [X] T004 [P] Write opening hook and learning objectives for Explorer variant (FR-035)
- [X] T005 [P] Write opening hook and learning objectives for Builder variant (FR-035)
- [X] T006 [P] Write opening hook and learning objectives for Engineer variant (FR-035)

**Checkpoint**: Each variant has engaging opening connecting to Chapter 2 and clear learning objectives

---

## Phase 3: User Story 1 - Core URDF Concepts (Priority: P1) MVP

**Goal**: Readers understand what URDF is, why it exists, and can identify links and joints

**Independent Test**: Readers can explain URDF purpose and identify links vs joints in a diagram

### Section: Why Robots Need a Body Model

- [X] T007 [P] [US1] Write "Why Robots Need a Body Model" section for Explorer variant with software analogies (FR-001, FR-002, FR-003)
- [X] T008 [P] [US1] Write "Why Robots Need a Body Model" section for Builder variant with maker context (FR-001, FR-002, FR-003)
- [X] T009 [P] [US1] Write "Why Robots Need a Body Model" section for Engineer variant with industrial context (FR-001, FR-002, FR-003)

### Section: Links - The Rigid Bodies

- [X] T010 [P] [US1] Write "Links: The Rigid Bodies" section for Explorer variant with simulated humanoid examples (FR-004, FR-005, FR-006, FR-007)
- [X] T011 [P] [US1] Write "Links: The Rigid Bodies" section for Builder variant with hobby robot examples (FR-004, FR-005, FR-006, FR-007)
- [X] T012 [P] [US1] Write "Links: The Rigid Bodies" section for Engineer variant with industrial examples (FR-004, FR-005, FR-006, FR-007)

### Section: Joints - The Connections

- [X] T013 [P] [US1] Write "Joints: The Connections" section for Explorer variant with joint type explanations (FR-008, FR-009, FR-010, FR-011)
- [X] T014 [P] [US1] Write "Joints: The Connections" section for Builder variant with servo/motor context (FR-008, FR-009, FR-010, FR-011)
- [X] T015 [P] [US1] Write "Joints: The Connections" section for Engineer variant with industrial actuator context (FR-008, FR-009, FR-010, FR-011)

### ASCII Diagram: Humanoid Link Hierarchy

- [X] T016 [P] [US1] Add humanoid link hierarchy ASCII diagram to Explorer variant (FR-036)
- [X] T017 [P] [US1] Add humanoid link hierarchy ASCII diagram to Builder variant (FR-036)
- [X] T018 [P] [US1] Add humanoid link hierarchy ASCII diagram to Engineer variant (FR-036)

**Checkpoint**: US1 complete - readers can identify links, joints, and explain URDF purpose

---

## Phase 4: User Story 2 - Kinematic Chain Understanding (Priority: P1)

**Goal**: Readers understand kinematic chains and can trace movement from base to end-effector

**Independent Test**: Readers can trace a complete kinematic chain and explain its importance for balance

### Section: Kinematic Chains

- [X] T019 [P] [US2] Write "Kinematic Chains" section for Explorer variant with game character rig analogies (FR-012, FR-013, FR-014, FR-015, FR-016)
- [X] T020 [P] [US2] Write "Kinematic Chains" section for Builder variant with hobby robot arm examples (FR-012, FR-013, FR-014, FR-015, FR-016)
- [X] T021 [P] [US2] Write "Kinematic Chains" section for Engineer variant with industrial manipulator examples (FR-012, FR-013, FR-014, FR-015, FR-016)

### ASCII Diagram: Kinematic Chain (Leg)

- [X] T022 [P] [US2] Add kinematic chain ASCII diagram to Explorer variant (FR-036)
- [X] T023 [P] [US2] Add kinematic chain ASCII diagram to Builder variant (FR-036)
- [X] T024 [P] [US2] Add kinematic chain ASCII diagram to Engineer variant (FR-036)

**Checkpoint**: US2 complete - readers can trace kinematic chains and understand forward kinematics concept

---

## Phase 5: User Story 3 - Transform Tree (TF) Concept (Priority: P1)

**Goal**: Readers understand how ROS 2 tracks spatial relationships via TF tree

**Independent Test**: Readers can interpret a TF tree diagram and explain parent-child frame relationships

### Section: Transform Tree (TF)

- [X] T025 [P] [US3] Write "Transform Tree (TF)" section for Explorer variant with coordinate system basics (FR-017, FR-018, FR-019, FR-020)
- [X] T026 [P] [US3] Write "Transform Tree (TF)" section for Builder variant with maker sensor context (FR-017, FR-018, FR-019, FR-020)
- [X] T027 [P] [US3] Write "Transform Tree (TF)" section for Engineer variant with industrial frame conventions (FR-017, FR-018, FR-019, FR-020)

### ASCII Diagram: TF Tree

- [X] T028 [P] [US3] Add TF tree ASCII diagram to Explorer variant (FR-036)
- [X] T029 [P] [US3] Add TF tree ASCII diagram to Builder variant (FR-036)
- [X] T030 [P] [US3] Add TF tree ASCII diagram to Engineer variant (FR-036)

**Checkpoint**: US3 complete - readers can interpret TF trees and connect URDF to runtime tracking

---

## Phase 6: User Story 4 - Physical Properties of Links (Priority: P2)

**Goal**: Readers understand mass, center of mass, and inertia conceptually

**Independent Test**: Readers can explain why mass distribution affects robot balance

### Section: Physical Properties (within Links section enhancement)

- [X] T031 [P] [US4] Enhance Links section with mass/inertia concepts for Explorer variant (FR-006, FR-007)
- [X] T032 [P] [US4] Enhance Links section with mass/inertia concepts for Builder variant (FR-006, FR-007)
- [X] T033 [P] [US4] Enhance Links section with mass/inertia concepts for Engineer variant (FR-006, FR-007)

**Checkpoint**: US4 complete - readers understand physical properties without mathematical formulas

---

## Phase 7: User Story 5 - Sensor and Actuator Representation (Priority: P2)

**Goal**: Readers understand how sensors and actuators connect to robot models

**Independent Test**: Readers can explain sensor frames and connect to ROS 2 topics from Chapter 2

### Section: Sensors and Frames

- [X] T034 [P] [US5] Write "Sensors and Frames" section for Explorer variant connecting to ROS 2 topics (FR-021, FR-022, FR-023)
- [X] T035 [P] [US5] Write "Sensors and Frames" section for Builder variant with maker sensor examples (FR-021, FR-022, FR-023)
- [X] T036 [P] [US5] Write "Sensors and Frames" section for Engineer variant with industrial sensor context (FR-021, FR-022, FR-023)

**Checkpoint**: US5 complete - readers understand sensor frame attachment and ROS 2 topic connection

---

## Phase 8: User Story 6 - URDF vs SDF Distinction (Priority: P3)

**Goal**: Readers understand when to use URDF vs SDF

**Independent Test**: Readers can explain URDF vs SDF differences and appropriate use cases

### Section: URDF vs SDF

- [X] T037 [P] [US6] Write "URDF vs SDF" section for Explorer variant with visualization focus (FR-024, FR-025, FR-026, FR-037)
- [X] T038 [P] [US6] Write "URDF vs SDF" section for Builder variant with simulation context (FR-024, FR-025, FR-026, FR-037)
- [X] T039 [P] [US6] Write "URDF vs SDF" section for Engineer variant with industrial simulation context (FR-024, FR-025, FR-026, FR-037)

**Checkpoint**: US6 complete - readers prepared for Module 2 with clear URDF/SDF distinction

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Try With AI activities, citations, and validation

### Try With AI Activities (Differentiated per FR-032)

- [X] T040 [P] Write "Try With AI" kinematic chain tracing activity for Explorer variant (FR-032)
- [X] T041 [P] Write "Try With AI" diagram interpretation activity for Builder variant (FR-032)
- [X] T042 [P] Write "Try With AI" TF tree construction activity for Engineer variant (FR-032)

### References (IEEE Citations)

- [X] T043 [P] Add IEEE-format references section to Explorer variant from research.md (FR-033)
- [X] T044 [P] Add IEEE-format references section to Builder variant from research.md (FR-033)
- [X] T045 [P] Add IEEE-format references section to Engineer variant from research.md (FR-033)

### Validation

- [X] T046 Validate Explorer variant: no code blocks, word count ~2800, all FRs addressed (FR-034, SC-007, SC-010)
- [X] T047 Validate Builder variant: no code blocks, word count ~3000, all FRs addressed (FR-034, SC-007, SC-010)
- [X] T048 Validate Engineer variant: no code blocks, word count ~3500, all FRs addressed (FR-034, SC-007, SC-010)
- [X] T049 Validate frontmatter completeness for all variants (FR-038, SC-013)

### Module Index Update

- [X] T050 Update module index with Chapter 3 links in docs/module-1-robotic-nervous-system/index.md

### Build Verification

- [X] T051 Run Docusaurus build and verify all chapter variants render correctly (SC-006)

**Checkpoint**: All chapters complete, validated, and building successfully

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - create all three chapter files in parallel
- **Phase 2 (Opening)**: Depends on Phase 1 - files must exist
- **Phases 3-8 (User Stories)**: Depend on Phase 2 - opening must be written first
- **Phase 9 (Polish)**: Depends on Phases 3-8 - content must exist before Try With AI and citations

### User Story Dependencies

- **US1 (Core URDF)**: No dependencies on other stories - foundational content
- **US2 (Kinematic Chains)**: Builds on US1 link/joint concepts but independently testable
- **US3 (TF Tree)**: Builds on US1/US2 but independently testable
- **US4 (Physical Properties)**: Enhances US1 content, can be done in parallel after US1
- **US5 (Sensors)**: Connects to Chapter 2, can be done in parallel after US3
- **US6 (URDF vs SDF)**: Standalone comparison, can be done in parallel after US1

### Parallel Opportunities

Within each phase, all tasks marked [P] can run in parallel:
- Phase 1: All 3 file creation tasks (T001-T003)
- Phase 2: All 3 opening tasks (T004-T006)
- Phase 3: All 12 US1 tasks (T007-T018)
- Phase 4: All 6 US2 tasks (T019-T024)
- Phase 5: All 6 US3 tasks (T025-T030)
- Phase 6: All 3 US4 tasks (T031-T033)
- Phase 7: All 3 US5 tasks (T034-T036)
- Phase 8: All 3 US6 tasks (T037-T039)
- Phase 9: Try With AI tasks (T040-T042), Citation tasks (T043-T045) in parallel

**Parallelizable**: 45 of 51 tasks (88%)

---

## Parallel Example: Phase 3 (User Story 1)

```text
# Launch all "Why Robots Need Body Model" sections together:
Task T007: Explorer - Why Robots Need Body Model
Task T008: Builder - Why Robots Need Body Model
Task T009: Engineer - Why Robots Need Body Model

# Launch all "Links" sections together:
Task T010: Explorer - Links section
Task T011: Builder - Links section
Task T012: Engineer - Links section

# Launch all "Joints" sections together:
Task T013: Explorer - Joints section
Task T014: Builder - Joints section
Task T015: Engineer - Joints section

# Launch all link hierarchy diagrams together:
Task T016: Explorer - Link hierarchy diagram
Task T017: Builder - Link hierarchy diagram
Task T018: Engineer - Link hierarchy diagram
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (all 3 chapter files)
2. Complete Phase 2: Opening (all 3 variants)
3. Complete Phase 3: User Story 1 - Core URDF (links, joints, diagrams)
4. Add Try With AI and References
5. **STOP and VALIDATE**: Build and review US1 content

### Incremental Delivery

1. Setup + Opening → Chapter structure ready
2. Add US1 (Core URDF) → Foundational content complete
3. Add US2 (Kinematic Chains) → Movement concepts added
4. Add US3 (TF Tree) → ROS 2 integration explained
5. Add US4-US6 → Complete depth and comparisons
6. Polish → Try With AI, citations, validation

### Parallel Variant Strategy

With content parallelization:
- Writer A: Explorer variant (all sections)
- Writer B: Builder variant (all sections)
- Writer C: Engineer variant (all sections)
- Each variant can be completed independently then merged

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 51 |
| Parallelizable | 45 (88%) |
| User Stories | 6 |
| Variants | 3 |
| Phases | 9 |

| User Story | Tasks | Priority |
|------------|-------|----------|
| US1 - Core URDF | 12 | P1 |
| US2 - Kinematic Chains | 6 | P1 |
| US3 - TF Tree | 6 | P1 |
| US4 - Physical Properties | 3 | P2 |
| US5 - Sensors | 3 | P2 |
| US6 - URDF vs SDF | 3 | P3 |
| Setup/Opening | 6 | - |
| Polish | 12 | - |

---

## Notes

- [P] tasks = different files, safe to parallelize
- All content must avoid code blocks and XML syntax (FR-034)
- IEEE citations required for all factual claims (FR-033)
- Word count targets: Explorer ~2800, Builder ~3000, Engineer ~3500
- Try With AI activities are differentiated by variant per FR-032
- Verify Docusaurus build after final tasks
