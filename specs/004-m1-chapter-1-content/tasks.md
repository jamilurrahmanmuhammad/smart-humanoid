# Tasks: Module 1 Chapter 1 - Foundations of Physical AI

**Input**: Design documents from `/specs/004-m1-chapter-1-content/`
**Prerequisites**: plan.md, spec.md, research.md

**Type**: Content Feature (Markdown chapters, no code)
**Output**: Three chapter variants in `docs/module-1-robotic-nervous-system/`

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- All paths are relative to repository root

## User Story Mapping

| Story | Priority | Content Section | Spec Requirement |
|-------|----------|-----------------|------------------|
| US1 | P1 | What is Physical AI? | FR-001, FR-003 |
| US2 | P1 | Why Embodiment Matters | FR-002, FR-005 |
| US3 | P2 | Perception-Action Loop | FR-004, FR-011 |
| US4 | P2 | Physics Awareness | FR-006 |
| US5 | P3 | ROS 2 Preview | FR-007 |
| US6 | P3 | Sensors Overview | FR-008 |

---

## Phase 1: Setup

**Purpose**: Verify environment and create chapter file structure

- [x] T001 Verify directory exists: `docs/module-1-robotic-nervous-system/`
- [x] T002 [P] Create Explorer variant file with frontmatter in `docs/module-1-robotic-nervous-system/chapter-1-physical-ai-foundations-explorer.md`
- [x] T003 [P] Create Builder variant file with frontmatter in `docs/module-1-robotic-nervous-system/chapter-1-physical-ai-foundations-builder.md`
- [x] T004 [P] Create Engineer variant file with frontmatter in `docs/module-1-robotic-nervous-system/chapter-1-physical-ai-foundations-engineer.md`

**Frontmatter Template** (per plan.md):
```yaml
---
title: "Chapter 1: Foundations of Physical AI"
sidebar_position: 2
safety: none
prerequisites:
  - generative AI user experience
  - high-level physics understanding
personaDifficulty: beginner | intermediate | advanced
learningPath: explorer | builder | engineer
personalizationTags: [embodied_intelligence, physical_ai, humanoids]
ragKeywords: [embodied AI, physics simulation, perception-action loop, ROS 2]
---
```

---

## Phase 2: Foundational (Common Structure)

**Purpose**: Create chapter skeleton and learning objectives for all variants

- [x] T005 Write Learning Objectives section (shared content, copy to all variants)
- [x] T006 [P] Write Introduction section for Explorer variant (software/simulation analogies)
- [x] T007 [P] Write Introduction section for Builder variant (Arduino/RPi context)
- [x] T008 [P] Write Introduction section for Engineer variant (industrial robotics context)
- [x] T009 Verify research.md citations are IEEE-formatted and accessible

**Checkpoint**: All three files have frontmatter, learning objectives, and introduction

---

## Phase 3: User Story 1 - Understand Physical AI Concept (Priority: P1)

**Goal**: Reader can explain the difference between digital AI and Physical AI

**Independent Test**: Reader can define Physical AI as AI grounded in physical constraints, perceiving and acting in real-world environments

**Requirements**: FR-001, FR-003, FR-008a

### Content for User Story 1

- [x] T010 [P] [US1] Write "What is Physical AI?" section for Explorer variant (software analogies, simulation examples) in `chapter-1-physical-ai-foundations-explorer.md`
- [x] T011 [P] [US1] Write "What is Physical AI?" section for Builder variant (maker/hobbyist context) in `chapter-1-physical-ai-foundations-builder.md`
- [x] T012 [P] [US1] Write "What is Physical AI?" section for Engineer variant (industrial examples, NVIDIA definition) in `chapter-1-physical-ai-foundations-engineer.md`
- [x] T013 [US1] Create text diagram: Digital AI vs Embodied AI comparison (shared, adapt per variant)
- [x] T014 [US1] Add IEEE citations for Physical AI definition claims (NVIDIA source)
- [x] T015 [US1] Explain AI concepts from first principles (no ML jargon without explanation) per FR-008a

**Checkpoint**: All variants have Physical AI section with citations and text diagram

---

## Phase 4: User Story 2 - Grasp Embodied Intelligence (Priority: P1)

**Goal**: Reader understands why robots need physical bodies to develop true intelligence

**Independent Test**: Reader can articulate why embodiment improves robot learning and generalization

**Requirements**: FR-002, FR-005

### Content for User Story 2

- [x] T016 [P] [US2] Write "Why Embodiment Matters" section for Explorer variant (conceptual, Pfeifer theory simplified) in `chapter-1-physical-ai-foundations-explorer.md`
- [x] T017 [P] [US2] Write "Why Embodiment Matters" section for Builder variant (hands-on learning analogy) in `chapter-1-physical-ai-foundations-builder.md`
- [x] T018 [P] [US2] Write "Why Embodiment Matters" section for Engineer variant (Pfeifer/Bongard theory, research depth) in `chapter-1-physical-ai-foundations-engineer.md`
- [x] T019 [US2] Explain why humanoids use human-like embodiment (navigate spaces, use tools, social interaction)
- [x] T020 [US2] Add IEEE citations for embodied intelligence claims (Pfeifer & Bongard source)

**Checkpoint**: All variants explain embodiment with appropriate depth per persona

---

## Phase 5: User Story 3 - Understand Perception-Action Loop (Priority: P2)

**Goal**: Reader understands how robots sense, process, plan, and act in continuous loop

**Independent Test**: Reader can trace through the loop (Sensors → Perception → Mapping → Planning → Control → Actuation) for a simple robot task

**Requirements**: FR-004, FR-011, FR-012

### Content for User Story 3

- [x] T021 [P] [US3] Write "Perception-Action Loop" section for Explorer variant (high-level conceptual) in `chapter-1-physical-ai-foundations-explorer.md`
- [x] T022 [P] [US3] Write "Perception-Action Loop" section for Builder variant (moderate detail, practical examples) in `chapter-1-physical-ai-foundations-builder.md`
- [x] T023 [P] [US3] Write "Perception-Action Loop" section for Engineer variant (full technical depth) in `chapter-1-physical-ai-foundations-engineer.md`
- [x] T024 [US3] Create text diagram of perception-action loop (ASCII/markdown format)
- [x] T025 [P] [US3] Write "Motivating Scenario: Pick Up the Bottle" section for Explorer variant
- [x] T026 [P] [US3] Write "Motivating Scenario: Pick Up the Bottle" section for Builder variant
- [x] T027 [P] [US3] Write "Motivating Scenario: Pick Up the Bottle" section for Engineer variant
- [x] T028 [US3] Break down scenario into perception, object detection, grasp planning, balance maintenance

**Checkpoint**: All variants have loop diagram and motivating scenario

---

## Phase 6: User Story 4 - Awareness of Physics Constraints (Priority: P2)

**Goal**: Reader understands key physical concepts robots must handle

**Independent Test**: Reader can list 5 physical constraints that make robot control harder than software control

**Requirements**: FR-006, FR-014

### Content for User Story 4

- [x] T029 [P] [US4] Write "Physics Awareness for Robots" section for Explorer variant (conceptual only, no math) in `chapter-1-physical-ai-foundations-explorer.md`
- [x] T030 [P] [US4] Write "Physics Awareness for Robots" section for Builder variant (practical implications) in `chapter-1-physical-ai-foundations-builder.md`
- [x] T031 [P] [US4] Write "Physics Awareness for Robots" section for Engineer variant (deeper physics concepts) in `chapter-1-physical-ai-foundations-engineer.md`
- [x] T032 [US4] Cover all required concepts: gravity, friction, inertia, balance, contact physics, collisions
- [x] T033 [US4] Explain why physics simulation is needed for training (no heavy math)

**Checkpoint**: All variants explain physics constraints at appropriate depth

---

## Phase 7: User Story 5 - ROS 2 Conceptual Foreshadowing (Priority: P3)

**Goal**: Reader understands conceptually why middleware like ROS 2 exists

**Independent Test**: Reader can explain what nodes, topics, services, and actions are conceptually (no code)

**Requirements**: FR-007, FR-022

### Content for User Story 5

- [x] T034 [P] [US5] Write "The Robotic Nervous System (ROS 2 Preview)" section for Explorer variant (metaphor-focused) in `chapter-1-physical-ai-foundations-explorer.md`
- [x] T035 [P] [US5] Write "The Robotic Nervous System (ROS 2 Preview)" section for Builder variant (practical context) in `chapter-1-physical-ai-foundations-builder.md`
- [x] T036 [P] [US5] Write "The Robotic Nervous System (ROS 2 Preview)" section for Engineer variant (architectural detail) in `chapter-1-physical-ai-foundations-engineer.md`
- [x] T037 [US5] Explain nodes, topics, services, actions conceptually (NO CODE per FR-022)
- [x] T038 [US5] Use nervous system metaphor (nodes=neurons, topics=signals, etc.)
- [x] T039 [US5] Add IEEE citations for ROS 2 architecture claims

**Checkpoint**: All variants explain ROS 2 concepts without any code

---

## Phase 8: User Story 6 - Hardware Awareness (Priority: P3)

**Goal**: Reader understands key sensors used in robotics

**Independent Test**: Reader can name 4 sensor types and explain their purpose in robot perception

**Requirements**: FR-008, FR-010

### Content for User Story 6

- [x] T040 [P] [US6] Write "Sensors: How Robots Perceive" section for Explorer variant (abstract sensors) in `chapter-1-physical-ai-foundations-explorer.md`
- [x] T041 [P] [US6] Write "Sensors: How Robots Perceive" section for Builder variant (consumer hardware: RealSense, hobbyist IMUs) in `chapter-1-physical-ai-foundations-builder.md`
- [x] T042 [P] [US6] Write "Sensors: How Robots Perceive" section for Engineer variant (industrial-grade sensors) in `chapter-1-physical-ai-foundations-engineer.md`
- [x] T043 [US6] Cover all required sensors: LiDAR, depth cameras, IMUs, force/torque sensors
- [x] T044 [US6] Include industry examples: Tesla Optimus, Figure 01, Unitree G1 with original explanations
- [x] T045 [US6] Add IEEE citations for sensor technology claims

**Checkpoint**: All variants cover sensor types with variant-appropriate examples

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final content, validation, and quality checks

### Try With AI Activity (Required per Constitution V)

- [x] T046 [P] Write "Try With AI" activity for Explorer variant (simulation-based prompt activity)
- [x] T047 [P] Write "Try With AI" activity for Builder variant (hardware-oriented prompt activity)
- [x] T048 [P] Write "Try With AI" activity for Engineer variant (technical analysis prompt activity)
- [x] T049 Ensure activity applies chapter concepts practically (FR-017)

### References & Citations

- [x] T050 Compile IEEE-format references section for Explorer variant
- [x] T051 [P] Compile IEEE-format references section for Builder variant
- [x] T052 [P] Compile IEEE-format references section for Engineer variant
- [x] T053 Verify all factual claims have citations (FR-018)

### Quality Validation

- [x] T054 Plagiarism check all three variants (FR-019) - Original content written
- [x] T055 Verify no code in any variant (FR-022)
- [x] T056 Verify no culture-specific idioms (translation-ready per FR-021)
- [x] T057 Verify frontmatter metadata complete for personalization (FR-020, FR-023)
- [x] T058 Build Docusaurus site and verify chapters render correctly
- [x] T059 Review against all FR-001 through FR-024 requirements
- [x] T060 Final review against Definition of Done checklist in plan.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phases 3-8)**: Depend on Foundational phase completion
  - User stories can proceed in priority order (P1 → P2 → P3)
  - Variants within each story can be written in parallel [P]
- **Polish (Phase 9)**: Depends on all user story content being complete

### User Story Dependencies

- **US1 (P1)**: Foundation for all other stories - Physical AI definition comes first
- **US2 (P1)**: Can be written alongside US1 - Embodiment theory
- **US3 (P2)**: Depends on US1/US2 concepts - References Physical AI and embodiment
- **US4 (P2)**: Can be written alongside US3 - Physics concepts
- **US5 (P3)**: References perception-action loop from US3
- **US6 (P3)**: Can be written alongside US5 - Sensor overview

### Parallel Opportunities

Within each user story phase:
- All three variant tasks marked [P] can be written in parallel
- Explorer → Builder → Engineer OR all three simultaneously

---

## Parallel Example: User Story 1

```bash
# Launch all variant content tasks in parallel:
Task: "Write Physical AI section for Explorer variant"
Task: "Write Physical AI section for Builder variant"
Task: "Write Physical AI section for Engineer variant"

# Then complete shared tasks:
Task: "Create text diagram: Digital AI vs Embodied AI"
Task: "Add IEEE citations for Physical AI definition"
```

---

## Implementation Strategy

### MVP First (Explorer Variant Only)

1. Complete Phase 1: Setup (create all 3 files with frontmatter)
2. Complete Phase 2: Foundational (Explorer intro + learning objectives)
3. Complete Phases 3-8: Write Explorer variant content for all user stories
4. Complete Phase 9: Try With AI + citations + validation for Explorer only
5. **STOP and VALIDATE**: Review Explorer variant against all requirements
6. Build Docusaurus and verify Explorer chapter renders

### Incremental Delivery

1. **Explorer MVP** → Review → Iterate if needed
2. **Add Builder variant** → Adapt content with moderate depth
3. **Add Engineer variant** → Adapt content with full technical depth
4. Each variant adds learner path coverage without breaking previous

### Content Adaptation Pattern

For each section, start with Explorer (simplest), then:
- **Builder**: Add practical hardware context, moderate detail
- **Engineer**: Add technical depth, industry examples, research references

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|----------------------|
| Setup | T001-T004 | T002-T004 (all variants) |
| Foundational | T005-T009 | T006-T008 (intro variants) |
| US1 (P1) | T010-T015 | T010-T012 (content variants) |
| US2 (P1) | T016-T020 | T016-T018 (content variants) |
| US3 (P2) | T021-T028 | T021-T023, T025-T027 (variants) |
| US4 (P2) | T029-T033 | T029-T031 (content variants) |
| US5 (P3) | T034-T039 | T034-T036 (content variants) |
| US6 (P3) | T040-T045 | T040-T042 (content variants) |
| Polish | T046-T060 | T046-T048, T050-T052 (variants) |

**Total Tasks**: 60
**Parallelizable**: ~30 tasks (50%)
**MVP Scope**: Explorer variant only (Tasks focusing on Explorer + shared tasks)

---

## Notes

- [P] tasks = different files, can run in parallel
- [Story] label maps task to specific user story for traceability
- NO CODE in any content (FR-022)
- IEEE citations required for all factual claims
- Translation-ready (no idioms, no culture-specific references)
- Each variant should be independently readable and complete
