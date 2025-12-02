# Feature Specification: Module 1 Chapter 2 - ROS 2 Architecture & Conceptual Model

**Feature Branch**: `005-m1-chapter-2-content`
**Created**: 2025-12-02
**Status**: Draft
**Specification ID**: CS-002-M1C2
**Input**: ChatGPT specification from `/mnt/c/mounted/chapter_2_specification_chatpt.txt`

---

## Chapter Overview

This chapter establishes the **mental model** required to understand ROS 2—not commands, not coding. It explains ROS 2 as a robotic nervous system, showing how distributed processes coordinate sensing, thinking, and acting.

**Purpose**: Conceptual clarity, not implementation.

**Prerequisite**: Chapter 1 - Foundations of Physical AI & Embodied Intelligence

---

## Scope

### In Scope

- High-level architecture of ROS 2
- Nodes, Topics, Services, Actions (pure conceptual)
- How ROS 2 handles distributed communication
- The role of middleware (DDS) at conceptual level
- How data flows inside a robot
- Concept of modularity & process separation
- Why ROS 2 is essential for humanoid robots
- Mental models that prepare students for rclpy in Chapter 3
- Biological metaphors (nervous system analogy)
- Text-based conceptual diagrams

### Out of Scope

- ROS 2 installation
- Running nodes
- Writing packages
- Launch files
- URDF
- Any real code (per FR-022)
- QoS profiles and transport layer details
- cyclonedds vs fastdds differences

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Understand ROS 2 Purpose (Priority: P1)

A reader wants to understand why ROS 2 exists and what problem it solves for robotics.

**Why this priority**: Without understanding the "why" of ROS 2, readers cannot appreciate subsequent technical content. This is the foundational mental model.

**Independent Test**: Reader can articulate in their own words why a humanoid robot cannot run on one AI model and needs distributed coordination. Reader can explain ROS 2's role as a "robotic nervous system."

**Acceptance Scenarios**:

1. **Given** a reader who has completed Chapter 1, **When** they read this section, **Then** they can explain why robots need dozens of cooperating processes rather than a single AI.
2. **Given** a software developer unfamiliar with robotics, **When** they finish this section, **Then** they understand ROS 2 as coordination middleware, not as an operating system.

---

### User Story 2 - Grasp ROS 2 Core Constructs Conceptually (Priority: P1)

A reader wants to understand nodes, topics, services, and actions without seeing any code.

**Why this priority**: These four communication patterns are the foundation of all ROS 2 programming. Conceptual understanding must precede implementation.

**Independent Test**: Reader can correctly match scenarios to communication patterns (e.g., "continuous camera feed" → topic, "get map once" → service, "walk to position" → action).

**Acceptance Scenarios**:

1. **Given** definitions of nodes, topics, services, and actions, **When** presented with robot scenarios, **Then** the reader can identify which pattern fits each scenario.
2. **Given** the nervous system metaphor, **When** the reader encounters "topic," **Then** they associate it with continuous neural signals.

---

### User Story 3 - Visualize Distributed Computing in Robotics (Priority: P2)

A reader wants to understand how humanoid robots coordinate parallel perception, motor control, and decision-making.

**Why this priority**: Humanoid complexity requires distributed architecture. This story connects abstract concepts to concrete robot requirements.

**Independent Test**: Reader can trace data flow from sensor input through perception, planning, control, and actuation in a humanoid example.

**Acceptance Scenarios**:

1. **Given** a text diagram of humanoid data flow, **When** the reader studies it, **Then** they can explain how camera data becomes motor commands.
2. **Given** the concept of parallel perception, **When** asked about humanoid balance, **Then** the reader understands multiple sensors (IMU, foot pressure, vision) must coordinate simultaneously.

---

### User Story 4 - Understand DDS at High Level (Priority: P2)

A reader wants to understand what DDS (Data Distribution Service) does without implementation details.

**Why this priority**: DDS is the "engine beneath ROS 2" but readers often skip middleware understanding. Conceptual grasp prevents later confusion.

**Independent Test**: Reader can explain DDS as enabling low-latency, real-time, multi-process, multi-machine communication without mentioning QoS tables or specific implementations.

**Acceptance Scenarios**:

1. **Given** the DDS explanation, **When** asked "what makes ROS 2 work across multiple computers," **Then** the reader can credit DDS middleware.
2. **Given** the bloodstream metaphor, **When** asked about DDS, **Then** the reader associates it with signal transport throughout the robot body.

---

### User Story 5 - Understand ROS 2 vs ROS 1 Differences (Priority: P3)

A reader wants to understand why ROS 2 replaced ROS 1, especially for humanoid applications.

**Why this priority**: Many resources reference ROS 1. Readers need context for why ROS 2 is the modern choice.

**Independent Test**: Reader can list 4 reasons ROS 2 is better for humanoids (multi-threading, multi-platform, real-time, security).

**Acceptance Scenarios**:

1. **Given** the comparison section, **When** asked "why not use ROS 1," **Then** the reader can cite specific ROS 2 advantages.
2. **Given** humanoid complexity requirements, **When** the reader considers real-time control needs, **Then** they understand why ROS 1 was insufficient.

---

### User Story 6 - Visualize Robot Communication Patterns (Priority: P3)

A reader wants to see how nodes, topics, services, and actions relate through diagrams.

**Why this priority**: Visual learners need diagrammatic representation. Text diagrams support all three variants.

**Independent Test**: Reader can interpret text diagrams showing node-topic-service-action relationships and trace message flow.

**Acceptance Scenarios**:

1. **Given** the Humanoid as Distributed System diagram, **When** the reader traces the flow, **Then** they can identify each node's role.
2. **Given** the Sensor-Perception-Control loop diagram, **When** asked about continuous operation, **Then** the reader understands the cyclic nature.

---

### Edge Cases

- What happens when readers have prior ROS 1 experience? (Content must not assume ROS 1 knowledge but should acknowledge it exists)
- How does system handle readers who want to skip to code? (Clear statement that this chapter is conceptual preparation, code comes in Chapter 3)
- What if readers confuse "operating system" meaning? (Explicit clarification that ROS is middleware, not an OS despite the name)

---

## Requirements *(mandatory)*

### Functional Requirements

#### Content Structure Requirements

- **FR-001**: Chapter MUST begin with a motivating narrative introduction posing the question "Why can't a robot run on one AI model?"
- **FR-002**: Chapter MUST explain ROS 2 using the biological/nervous system metaphor throughout
- **FR-003**: Chapter MUST define nodes, topics, services, and actions conceptually without code
- **FR-004**: Chapter MUST include at least 3 text-based conceptual diagrams
- **FR-005**: Chapter MUST explain DDS at a high level (reliability, low-latency, distributed nature)
- **FR-006**: Chapter MUST include a short ROS 2 vs ROS 1 comparison section

#### Conceptual Content Requirements

- **FR-007**: Chapter MUST explain nodes as independent processes with single responsibilities
- **FR-008**: Chapter MUST explain topics as continuous publish-subscribe data streams
- **FR-009**: Chapter MUST explain services as request-response patterns for one-time data needs
- **FR-010**: Chapter MUST explain actions as long-running goal-based behaviors with feedback
- **FR-011**: Chapter MUST include humanoid-specific examples (leg joint controller, foot pressure sensor, balance controller, IMU node)
- **FR-012**: Chapter MUST explain distributed computing requirements for humanoid robots (parallel perception, real-time motor control, multi-sensor fusion)

#### Nervous System Metaphor Requirements

- **FR-013**: Sensors MUST be presented as "sensory organs"
- **FR-014**: Nodes MUST be presented as "clusters of neurons"
- **FR-015**: Topics MUST be presented as "neural signals"
- **FR-016**: Services MUST be presented as "reflex pathways"
- **FR-017**: Actions MUST be presented as "goal-driven behaviors"
- **FR-018**: DDS MUST be presented as "bloodstream/network carrying signals"

#### Diagram Requirements

- **FR-019**: Chapter MUST include Diagram 1: Humanoid as a Distributed System (Camera → Perception → Planning → Control → Motors)
- **FR-020**: Chapter MUST include Diagram 2: ROS 2 Communication Map (Nodes ↔ Topics/Services/Actions ↔ Nodes)
- **FR-021**: Chapter MUST include Diagram 3: Sensor-Perception-Control Loop

#### Constitution Compliance Requirements

- **FR-022**: Chapter MUST NOT contain any code, CLI commands, or installation instructions (pure conceptual)
- **FR-023**: Chapter MUST include IEEE-format citations for all factual claims
- **FR-024**: Chapter MUST end with a "Try With AI" scenario-matching activity where readers identify correct ROS 2 communication patterns (topic/service/action) for given robot scenarios, adapted per variant context
- **FR-025**: Chapter MUST be delivered as three variants: Explorer, Builder, Engineer
- **FR-026**: All variants MUST share same learning objectives and "Try With AI" structure
- **FR-027**: Content MUST be translation-ready (no culture-specific idioms)
- **FR-028**: Content MUST explain concepts from first principles (no assumed ML/neural network knowledge)

#### Variant Differentiation Requirements

- **FR-029**: Explorer variant MUST use software analogies and simulation-only context (~2800 words)
- **FR-030**: Builder variant MUST reference Arduino/Raspberry Pi context where appropriate (~3000 words)
- **FR-031**: Engineer variant MUST include industrial robotics context and deeper technical considerations (~3500 words)

---

## Learning Objectives

By the end of this chapter, the reader MUST be able to:

1. Describe the purpose of ROS 2 in a robotic system
2. Understand how ROS 2 enables distributed, real-time coordination
3. Explain nodes, topics, services, and actions conceptually (without code)
4. Understand the role of DDS (Data Distribution Service) at a conceptual level
5. Visualize a humanoid robot as a network of communicating processes
6. Explain why ROS 1 could not handle humanoid-level complexity

---

## Metadata Requirements

Each chapter variant MUST include this frontmatter:

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

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All four ROS 2 communication patterns (nodes, topics, services, actions) are introduced correctly and completely
- **SC-002**: Humanoid robots as distributed systems are explained with concrete examples
- **SC-003**: DDS is described accurately but simply (no QoS tables, no implementation details)
- **SC-004**: At least 3 conceptual text diagrams are present and correctly illustrate concepts
- **SC-005**: The narrative connects Physical AI (Chapter 1) → ROS 2 necessity (Chapter 2)
- **SC-006**: Zero code appears in any variant (no Python, no CLI, no installation)
- **SC-007**: Language is smooth, narrative, and beginner-friendly across all variants
- **SC-008**: All factual claims have IEEE citations
- **SC-009**: No plagiarism (original content throughout)
- **SC-010**: Constitution's clarity, structure, and cognitive scaffolding principles are followed

### Build Verification

- **SC-011**: Docusaurus build completes successfully with no errors
- **SC-012**: All three chapter variants render correctly in the documentation site
- **SC-013**: Module index page links to all three variants correctly

---

## Output Files

This feature will produce:

1. `docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-explorer.md`
2. `docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-builder.md`
3. `docs/module-1-robotic-nervous-system/chapter-2-ros2-architecture-engineer.md`

---

## References (for research phase)

Input specification source:
- ChatGPT specification: `/mnt/c/mounted/chapter_2_specification_chatpt.txt`

Required research for IEEE citations:
- ROS 2 official documentation and design papers
- DDS specification and purpose
- Distributed robotics architecture papers
- ROS 1 vs ROS 2 comparison sources

---

## Clarifications

### Session 2025-12-02

- Q: What type of "Try With AI" activity is appropriate for a conceptual, no-code chapter? → A: Scenario matching activity adapted per user profile (Explorer/Builder/Engineer each get contextually appropriate scenarios)
- Q: Should Chapter 2 follow similar word count proportions as Chapter 1? → A: Yes, same proportions (~2800/3000/3500 words for Explorer/Builder/Engineer)

---

## Next Steps

1. `/sp.clarify` - Identify any underspecified areas
2. `/sp.plan` - Create architectural plan and research strategy
3. `/sp.tasks` - Generate implementation tasks
4. `/sp.implement` - Create chapter content
