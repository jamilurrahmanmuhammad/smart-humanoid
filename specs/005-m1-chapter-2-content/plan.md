# Implementation Plan: Module 1 Chapter 2 - ROS 2 Architecture

**Branch**: `005-m1-chapter-2-content` | **Date**: 2025-12-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-m1-chapter-2-content/spec.md`

## Summary

Create three chapter variants (Explorer, Builder, Engineer) explaining ROS 2 architecture conceptually using the nervous system metaphor. Pure conceptual content—no code, CLI commands, or installation instructions. Content establishes mental models preparing readers for rclpy implementation in Chapter 3.

## Technical Context

**Content Type**: Educational Markdown chapters (not code)
**Platform**: Docusaurus 3.x
**Output Format**: MDX-compatible Markdown
**Testing**: Docusaurus build verification
**Target**: Web documentation site

**Content Requirements**:
- Three variants: Explorer (~2800 words), Builder (~3000 words), Engineer (~3500 words)
- IEEE-format citations for all factual claims
- Text-based diagrams (ASCII/Markdown format)
- "Try With AI" scenario-matching activity per variant
- Translation-ready (no idioms)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Status |
|------|-------------|--------|
| VI. Citation Requirements | IEEE format for all factual claims | ✅ PASS (FR-023) |
| VII. Source Verification | Tier 1-2 sources only | ✅ PASS (research.md will verify) |
| VIII. Technical Accuracy | No hallucinated APIs/features | ✅ PASS (no code) |
| IX. Plagiarism Prevention | Original content | ✅ PASS (FR-009 specifies original) |
| XIII. Adaptive Content | Three variants required | ✅ PASS (FR-025) |
| XIII. Reader Baseline | First principles, no ML jargon | ✅ PASS (FR-028) |
| V. Minimal Sufficient | "Try With AI" required | ✅ PASS (FR-024) |
| XXXVI. Chapter Structure | Learning objectives, prerequisites | ✅ PASS (metadata specified) |

**All gates PASS.** No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/005-m1-chapter-2-content/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── research.md          # Phase 0 output - IEEE citation sources
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Content Output (repository root)

```text
docs/module-1-robotic-nervous-system/
├── index.md                                    # Module index (update needed)
├── chapter-2-ros2-architecture-explorer.md     # Explorer variant (new)
├── chapter-2-ros2-architecture-builder.md      # Builder variant (new)
└── chapter-2-ros2-architecture-engineer.md     # Engineer variant (new)
```

**Structure Decision**: Content feature following Chapter 1 pattern. Three separate Markdown files per variant, placed in module directory.

## Content Architecture

### Section Flow (All Variants)

```text
1. Frontmatter (YAML metadata)
2. Learning Objectives
3. Introduction: "Why can't a robot run on one AI model?"
4. ROS 2 as the Robotic Nervous System
   - Nervous system metaphor introduction
   - Why distributed coordination matters
5. Core Constructs (Conceptual)
   - Nodes (neurons)
   - Topics (neural signals)
   - Services (reflex pathways)
   - Actions (goal-driven behaviors)
6. Distributed Computing in Humanoids
   - Parallel perception requirements
   - Real-time motor control
   - Multi-sensor fusion
7. DDS: The Communication Backbone
   - Bloodstream metaphor
   - Reliability, low-latency, multi-machine
8. ROS 2 vs ROS 1 (Brief)
   - Why ROS 2 for humanoids
9. Conceptual Diagrams
   - Diagram 1: Humanoid as Distributed System
   - Diagram 2: ROS 2 Communication Map
   - Diagram 3: Sensor-Perception-Control Loop
10. Try With AI Activity
    - Scenario matching exercise (variant-specific)
11. References (IEEE format)
```

### Variant Differentiation Strategy

| Section | Explorer | Builder | Engineer |
|---------|----------|---------|----------|
| Examples | Software analogies (microservices, message queues) | Arduino/RPi communication patterns | Industrial robot cells, PLCs |
| Depth | High-level conceptual only | Moderate technical detail | Full architectural considerations |
| Diagrams | Simple flow diagrams | Component-level diagrams | System architecture diagrams |
| Try With AI | Simulation scenarios | Hobby robot scenarios | Industrial/humanoid scenarios |
| Word Count | ~2800 | ~3000 | ~3500 |

### Diagram Specifications

**Diagram 1: Humanoid as Distributed System**
```text
[ Camera Node ]
     │ (Image Topic)
[ Perception Node ]
     │ (Bounding Boxes Topic)
[ Planning Node ]
     │ (Trajectory Action)
[ Control Node ]
     │ (Joint Commands Topic)
[ Motors ]
```

**Diagram 2: ROS 2 Communication Map**
```text
┌─────────┐     Topics      ┌─────────┐
│  Node A │ ──────────────► │  Node B │
└─────────┘                 └─────────┘
     │                           │
     │ Services (request/response)
     └───────────────────────────┘

     │◄──── Actions (goal/feedback/result) ────►│
```

**Diagram 3: Sensor-Perception-Control Loop**
```text
Sensors → ROS 2 Topics → Perception → Planning → Control → Actuators
    ▲                                                          │
    └──────────────── Feedback Loop ───────────────────────────┘
```

## Research Requirements

See [research.md](./research.md) for:

1. **ROS 2 Architecture Sources** - Official documentation, design papers
2. **DDS Specification** - OMG DDS standard, purpose and benefits
3. **Distributed Robotics** - Academic papers on robot middleware
4. **ROS 1 vs ROS 2** - Migration guides, comparison articles
5. **Humanoid Examples** - Industry robots (Tesla Optimus, Figure, Unitree)

## Definition of Done

### Content Checklist

- [ ] All three variants created with correct frontmatter
- [ ] Learning objectives present in all variants
- [ ] All 6 user stories addressed
- [ ] All 31 functional requirements met
- [ ] 3+ text diagrams in each variant
- [ ] Nervous system metaphor consistently applied
- [ ] IEEE citations for all factual claims (5-8 per variant)
- [ ] "Try With AI" activity with variant-specific scenarios
- [ ] No code, CLI commands, or installation instructions
- [ ] Translation-ready (no idioms)
- [ ] Word counts within target range

### Build Verification

- [ ] Docusaurus build successful
- [ ] All variants render correctly
- [ ] Module index updated with Chapter 2 links
- [ ] No MDX parsing errors

### Quality Gates

- [ ] SC-001 through SC-013 all pass
- [ ] Constitution gates re-verified post-implementation

## Complexity Tracking

> No violations requiring justification. Content feature follows established Chapter 1 pattern.

## Next Steps

1. ✅ `/sp.plan` - This document (complete)
2. ⏳ `/sp.tasks` - Generate implementation tasks
3. ⏳ `/sp.implement` - Create chapter content
4. ⏳ `/sp.git.commit_pr` - Commit and create PR
