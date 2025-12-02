# Tasks: Module 1 Chapter 2 - ROS 2 Architecture & Conceptual Model

**Input**: Design documents from `/specs/005-m1-chapter-2-content/`
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
| US1 | P1 | ROS 2 Purpose & Introduction | FR-001, FR-002 |
| US2 | P1 | Core Constructs (Nodes/Topics/Services/Actions) | FR-003, FR-007-010, FR-013-017 |
| US3 | P2 | Distributed Computing in Humanoids | FR-011, FR-012 |
| US4 | P2 | DDS Middleware | FR-005, FR-018 |
| US5 | P3 | ROS 2 vs ROS 1 | FR-006 |
| US6 | P3 | Conceptual Diagrams | FR-004, FR-019-021 |

---

## Phase 1: Setup

**Purpose**: Verify environment and create chapter file structure

- [ ] T001 Verify directory exists: `docs/module-1-robotic-nervous-system/`
- [ ] T002 [P] Create Explorer variant file with frontmatter in `docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-explorer.md`
- [ ] T003 [P] Create Builder variant file with frontmatter in `docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-builder.md`
- [ ] T004 [P] Create Engineer variant file with frontmatter in `docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-engineer.md`

**Frontmatter Template** (per spec.md):
```yaml
---
title: "Chapter 2: ROS 2 Architecture & the Conceptual Model of Robot Control"
sidebar_position: 3
safety: none
prerequisites:
  - understanding of embodied intelligence concepts (from Chapter 1)
personaDifficulty: beginner | intermediate | advanced
learningPath: explorer | builder | engineer
personalizationTags:
  - ros2_architecture
  - robotics_middleware
  - humanoid_systems
ragKeywords:
  - ROS 2
  - nodes
  - topics
  - services
  - actions
  - DDS
---
```

---

## Phase 2: Foundational (Common Structure)

**Purpose**: Create chapter skeleton and learning objectives for all variants

- [ ] T005 Write Learning Objectives section (shared content, copy to all variants)
- [ ] T006 [P] Write Introduction section for Explorer variant (software analogies, microservices comparison) in `chapter-2-ros2-architecture-explorer.md`
- [ ] T007 [P] Write Introduction section for Builder variant (Arduino/RPi context) in `chapter-2-ros2-architecture-builder.md`
- [ ] T008 [P] Write Introduction section for Engineer variant (industrial robotics context) in `chapter-2-ros2-architecture-engineer.md`
- [ ] T009 Verify research.md citations are IEEE-formatted and accessible

**Checkpoint**: All three files have frontmatter, learning objectives, and introduction

---

## Phase 3: User Story 1 - Understand ROS 2 Purpose (Priority: P1)

**Goal**: Reader understands why ROS 2 exists and what problem it solves

**Independent Test**: Reader can articulate why a humanoid robot cannot run on one AI model and needs distributed coordination

**Requirements**: FR-001, FR-002

### Content for User Story 1

- [ ] T010 [P] [US1] Write "Why Can't a Robot Run on One AI Model?" narrative for Explorer variant (software developer perspective) in `chapter-2-ros2-architecture-explorer.md`
- [ ] T011 [P] [US1] Write "Why Can't a Robot Run on One AI Model?" narrative for Builder variant (maker perspective) in `chapter-2-ros2-architecture-builder.md`
- [ ] T012 [P] [US1] Write "Why Can't a Robot Run on One AI Model?" narrative for Engineer variant (industrial perspective) in `chapter-2-ros2-architecture-engineer.md`
- [ ] T013 [US1] Introduce nervous system metaphor in all variants (ROS 2 as robotic nervous system)
- [ ] T014 [US1] Add IEEE citations for ROS 2 purpose claims [1], [2] from research.md
- [ ] T015 [US1] Clarify ROS is middleware, not an operating system (address edge case)

**Checkpoint**: All variants explain ROS 2 purpose with nervous system metaphor introduced

---

## Phase 4: User Story 2 - Grasp ROS 2 Core Constructs (Priority: P1)

**Goal**: Reader understands nodes, topics, services, and actions conceptually without code

**Independent Test**: Reader can match scenarios to communication patterns (camera feed → topic, get map → service, walk to position → action)

**Requirements**: FR-003, FR-007, FR-008, FR-009, FR-010, FR-013, FR-014, FR-015, FR-016, FR-017

### Content for User Story 2

- [ ] T016 [P] [US2] Write "Nodes" section for Explorer variant (microservices analogy, neurons metaphor) in `chapter-2-ros2-architecture-explorer.md`
- [ ] T017 [P] [US2] Write "Nodes" section for Builder variant (Arduino processes analogy) in `chapter-2-ros2-architecture-builder.md`
- [ ] T018 [P] [US2] Write "Nodes" section for Engineer variant (process isolation, single responsibility) in `chapter-2-ros2-architecture-engineer.md`
- [ ] T019 [P] [US2] Write "Topics" section for Explorer variant (message queues analogy, neural signals metaphor) in `chapter-2-ros2-architecture-explorer.md`
- [ ] T020 [P] [US2] Write "Topics" section for Builder variant (sensor data streams) in `chapter-2-ros2-architecture-builder.md`
- [ ] T021 [P] [US2] Write "Topics" section for Engineer variant (pub-sub patterns, data flow) in `chapter-2-ros2-architecture-engineer.md`
- [ ] T022 [P] [US2] Write "Services" section for Explorer variant (API calls analogy, reflex pathways metaphor) in `chapter-2-ros2-architecture-explorer.md`
- [ ] T023 [P] [US2] Write "Services" section for Builder variant (request-response pattern) in `chapter-2-ros2-architecture-builder.md`
- [ ] T024 [P] [US2] Write "Services" section for Engineer variant (synchronous operations) in `chapter-2-ros2-architecture-engineer.md`
- [ ] T025 [P] [US2] Write "Actions" section for Explorer variant (long-running tasks analogy, goal-driven behaviors metaphor) in `chapter-2-ros2-architecture-explorer.md`
- [ ] T026 [P] [US2] Write "Actions" section for Builder variant (robot arm movement example) in `chapter-2-ros2-architecture-builder.md`
- [ ] T027 [P] [US2] Write "Actions" section for Engineer variant (feedback loops, preemption) in `chapter-2-ros2-architecture-engineer.md`
- [ ] T028 [US2] Add IEEE citations for communication patterns [2], [3] from research.md
- [ ] T029 [US2] Verify NO CODE appears in any construct explanation (FR-022)

**Checkpoint**: All four ROS 2 constructs explained with appropriate metaphors per variant

---

## Phase 5: User Story 3 - Visualize Distributed Computing (Priority: P2)

**Goal**: Reader understands how humanoid robots coordinate parallel perception, motor control, and decision-making

**Independent Test**: Reader can trace data flow from sensor input through perception, planning, control, and actuation

**Requirements**: FR-011, FR-012

### Content for User Story 3

- [ ] T030 [P] [US3] Write "Distributed Computing in Humanoids" section for Explorer variant (high-level conceptual) in `chapter-2-ros2-architecture-explorer.md`
- [ ] T031 [P] [US3] Write "Distributed Computing in Humanoids" section for Builder variant (practical examples) in `chapter-2-ros2-architecture-builder.md`
- [ ] T032 [P] [US3] Write "Distributed Computing in Humanoids" section for Engineer variant (full technical depth) in `chapter-2-ros2-architecture-engineer.md`
- [ ] T033 [US3] Include humanoid-specific examples: leg joint controller, foot pressure sensor, balance controller, IMU node
- [ ] T034 [US3] Explain parallel perception requirements
- [ ] T035 [US3] Explain real-time motor control needs
- [ ] T036 [US3] Explain multi-sensor fusion concept
- [ ] T037 [US3] Add IEEE citations for distributed robotics [15], [16], [17] from research.md

**Checkpoint**: Distributed computing explained with humanoid-specific examples

---

## Phase 6: User Story 4 - Understand DDS (Priority: P2)

**Goal**: Reader understands what DDS does without implementation details

**Independent Test**: Reader can explain DDS as enabling low-latency, real-time, multi-machine communication

**Requirements**: FR-005, FR-018

### Content for User Story 4

- [ ] T038 [P] [US4] Write "DDS: The Communication Backbone" section for Explorer variant (bloodstream metaphor emphasized) in `chapter-2-ros2-architecture-explorer.md`
- [ ] T039 [P] [US4] Write "DDS: The Communication Backbone" section for Builder variant (network layer analogy) in `chapter-2-ros2-architecture-builder.md`
- [ ] T040 [P] [US4] Write "DDS: The Communication Backbone" section for Engineer variant (middleware architecture) in `chapter-2-ros2-architecture-engineer.md`
- [ ] T041 [US4] Explain reliability guarantees conceptually
- [ ] T042 [US4] Explain low-latency communication benefits
- [ ] T043 [US4] Explain multi-machine coordination capability
- [ ] T044 [US4] Add IEEE citations for DDS [4], [5], [6] from research.md
- [ ] T045 [US4] Verify NO QoS profiles or implementation details included (out of scope)

**Checkpoint**: DDS explained at conceptual level with bloodstream metaphor

---

## Phase 7: User Story 5 - ROS 2 vs ROS 1 (Priority: P3)

**Goal**: Reader understands why ROS 2 replaced ROS 1 for humanoid applications

**Independent Test**: Reader can list 4 reasons ROS 2 is better for humanoids

**Requirements**: FR-006

### Content for User Story 5

- [ ] T046 [P] [US5] Write "Why ROS 2 Instead of ROS 1" section for Explorer variant (brief, beginner-friendly) in `chapter-2-ros2-architecture-explorer.md`
- [ ] T047 [P] [US5] Write "Why ROS 2 Instead of ROS 1" section for Builder variant (practical migration context) in `chapter-2-ros2-architecture-builder.md`
- [ ] T048 [P] [US5] Write "Why ROS 2 Instead of ROS 1" section for Engineer variant (technical comparison) in `chapter-2-ros2-architecture-engineer.md`
- [ ] T049 [US5] Cover multi-threading advantage
- [ ] T050 [US5] Cover multi-platform support (Linux, Windows, macOS)
- [ ] T051 [US5] Cover real-time capability
- [ ] T052 [US5] Cover security features
- [ ] T053 [US5] Add IEEE citations for ROS comparison [7], [8] from research.md

**Checkpoint**: ROS 2 advantages clearly explained for humanoid use cases

---

## Phase 8: User Story 6 - Conceptual Diagrams (Priority: P3)

**Goal**: Reader can visualize node-topic-service-action relationships through diagrams

**Independent Test**: Reader can interpret text diagrams and trace message flow

**Requirements**: FR-004, FR-019, FR-020, FR-021

### Content for User Story 6

- [ ] T054 [P] [US6] Create Diagram 1: Humanoid as Distributed System for Explorer variant (simple flow) in `chapter-2-ros2-architecture-explorer.md`
- [ ] T055 [P] [US6] Create Diagram 1: Humanoid as Distributed System for Builder variant (component-level) in `chapter-2-ros2-architecture-builder.md`
- [ ] T056 [P] [US6] Create Diagram 1: Humanoid as Distributed System for Engineer variant (system architecture) in `chapter-2-ros2-architecture-engineer.md`
- [ ] T057 [P] [US6] Create Diagram 2: ROS 2 Communication Map for Explorer variant in `chapter-2-ros2-architecture-explorer.md`
- [ ] T058 [P] [US6] Create Diagram 2: ROS 2 Communication Map for Builder variant in `chapter-2-ros2-architecture-builder.md`
- [ ] T059 [P] [US6] Create Diagram 2: ROS 2 Communication Map for Engineer variant in `chapter-2-ros2-architecture-engineer.md`
- [ ] T060 [P] [US6] Create Diagram 3: Sensor-Perception-Control Loop for Explorer variant in `chapter-2-ros2-architecture-explorer.md`
- [ ] T061 [P] [US6] Create Diagram 3: Sensor-Perception-Control Loop for Builder variant in `chapter-2-ros2-architecture-builder.md`
- [ ] T062 [P] [US6] Create Diagram 3: Sensor-Perception-Control Loop for Engineer variant in `chapter-2-ros2-architecture-engineer.md`
- [ ] T063 [US6] Verify all diagrams are text-based (ASCII/Markdown) for MDX compatibility

**Checkpoint**: All 3 diagrams present in each variant with appropriate complexity level

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final content, validation, and quality checks

### Try With AI Activity (Required per Constitution V)

- [ ] T064 [P] Write "Try With AI" scenario-matching activity for Explorer variant (simulation scenarios) in `chapter-2-ros2-architecture-explorer.md`
- [ ] T065 [P] Write "Try With AI" scenario-matching activity for Builder variant (hobby robot scenarios) in `chapter-2-ros2-architecture-builder.md`
- [ ] T066 [P] Write "Try With AI" scenario-matching activity for Engineer variant (industrial/humanoid scenarios) in `chapter-2-ros2-architecture-engineer.md`
- [ ] T067 Ensure activity tests pattern matching: topic vs service vs action (FR-024)

### References & Citations

- [ ] T068 Compile IEEE-format references section for Explorer variant
- [ ] T069 [P] Compile IEEE-format references section for Builder variant
- [ ] T070 [P] Compile IEEE-format references section for Engineer variant
- [ ] T071 Verify all factual claims have citations (FR-023)

### Quality Validation

- [ ] T072 Verify no code in any variant (FR-022) - scan for code blocks
- [ ] T073 Verify no culture-specific idioms (translation-ready per FR-027)
- [ ] T074 Verify frontmatter metadata complete for personalization (FR-025, FR-026)
- [ ] T075 Verify word counts: Explorer ~2800, Builder ~3000, Engineer ~3500
- [ ] T076 Build Docusaurus site and verify chapters render correctly
- [ ] T077 Update module index.md with Chapter 2 links in `docs/module-1-robotic-nervous-system/index.md`
- [ ] T078 Review against all FR-001 through FR-031 requirements
- [ ] T079 Final review against Definition of Done checklist in plan.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phases 3-8)**: Depend on Foundational phase completion
  - US1 (P1) and US2 (P1): Can proceed in parallel after Foundational
  - US3 (P2) and US4 (P2): Can proceed after US1/US2 or in parallel with them
  - US5 (P3) and US6 (P3): Can proceed after earlier stories or in parallel
- **Polish (Phase 9)**: Depends on all user story content being complete

### User Story Dependencies

- **US1 (P1)**: Foundation for all - ROS 2 purpose and nervous system metaphor
- **US2 (P1)**: Can parallel with US1 - Core constructs (nodes/topics/services/actions)
- **US3 (P2)**: References US1/US2 concepts - Distributed computing
- **US4 (P2)**: Can parallel with US3 - DDS middleware
- **US5 (P3)**: References US1 concepts - ROS 1 vs ROS 2
- **US6 (P3)**: References US2 constructs - Conceptual diagrams

### Parallel Opportunities

Within each user story phase:
- All three variant tasks marked [P] can be written in parallel
- Explorer → Builder → Engineer OR all three simultaneously

---

## Parallel Example: User Story 2 (Core Constructs)

```bash
# Launch all Nodes section tasks in parallel:
Task: "Write Nodes section for Explorer variant"
Task: "Write Nodes section for Builder variant"
Task: "Write Nodes section for Engineer variant"

# Then Topics in parallel:
Task: "Write Topics section for Explorer variant"
Task: "Write Topics section for Builder variant"
Task: "Write Topics section for Engineer variant"

# Continue for Services and Actions...

# Then complete shared tasks:
Task: "Add IEEE citations for communication patterns"
Task: "Verify NO CODE in construct explanations"
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
- **Engineer**: Add technical depth, industrial examples, research references

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|----------------------|
| Setup | T001-T004 | T002-T004 (all variants) |
| Foundational | T005-T009 | T006-T008 (intro variants) |
| US1 (P1) | T010-T015 | T010-T012 (content variants) |
| US2 (P1) | T016-T029 | T016-T027 (all construct variants) |
| US3 (P2) | T030-T037 | T030-T032 (content variants) |
| US4 (P2) | T038-T045 | T038-T040 (content variants) |
| US5 (P3) | T046-T053 | T046-T048 (content variants) |
| US6 (P3) | T054-T063 | T054-T062 (all diagram variants) |
| Polish | T064-T079 | T064-T066, T068-T070 (variants) |

**Total Tasks**: 79
**Parallelizable**: ~45 tasks (57%)
**MVP Scope**: Explorer variant only (Tasks focusing on Explorer + shared tasks)

---

## Notes

- [P] tasks = different files, can run in parallel
- [Story] label maps task to specific user story for traceability
- NO CODE in any content (FR-022)
- IEEE citations required for all factual claims
- Translation-ready (no idioms, no culture-specific references)
- Each variant should be independently readable and complete
- Escape `<` characters in MDX to avoid parsing errors (lesson from Chapter 1)
