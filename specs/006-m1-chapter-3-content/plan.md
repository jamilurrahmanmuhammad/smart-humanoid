# Implementation Plan: Module 1 Chapter 3 - URDF Modeling

**Branch**: `006-m1-chapter-3-content` | **Date**: 2025-12-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-m1-chapter-3-content/spec.md`

## Summary

Create Chapter 3 of Module 1: "Humanoid Robot Modeling with URDF" - a conceptual introduction to robot description formats. The chapter explains links, joints, kinematic chains, and transform trees without any code or XML syntax. Content will be delivered as three variants (Explorer, Builder, Engineer) per Constitution v1.2.0.

## Technical Context

**Content Type**: Educational Markdown (Docusaurus)
**Language/Version**: Markdown with MDX support (Docusaurus 3.x)
**Primary Dependencies**: Docusaurus, React (for rendering)
**Storage**: Git-versioned markdown files
**Testing**: Docusaurus build verification, manual content review
**Target Platform**: Web (Docusaurus static site)
**Project Type**: Documentation/Content
**Performance Goals**: N/A (static content)
**Constraints**: No code blocks, no XML syntax, conceptual only
**Scale/Scope**: 3 chapter variants (~2800/3000/3500 words each)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Status |
|------|-------------|--------|
| XIII. Adaptive Content | Three variants required (Explorer, Builder, Engineer) | PASS |
| V. Minimal Sufficient Content | End with "Try With AI" activity | PASS |
| VI. Citation Requirements | IEEE format for all factual claims | PASS |
| VIII. Technical Accuracy | No hallucinated APIs or features | PASS |
| IX. Plagiarism Prevention | Original content, proper attribution | PASS |
| XXXVI. Chapter Structure | Learning objectives, prerequisites, Try With AI | PASS |
| FR-034 | No code blocks or XML syntax | PASS |

**All gates PASS** - Proceed to Phase 0.

## Content Architecture

### Section Flow (All Variants)

```text
1. Opening Hook
   - "A robot cannot walk, balance, or perceive unless it understands its own body"
   - Connect to Chapter 2 (ROS 2 knows HOW to communicate, now needs to know WHAT it is)

2. Learning Objectives
   - Explain what URDF is and what problems it solves
   - Describe humanoid anatomy in terms of links and joints
   - Understand kinematic chains and their role in movement
   - Visualize a robot as a TF tree
   - Distinguish URDF from SDF conceptually

3. Why Robots Need a Body Model (FR-001, FR-002, FR-003)
   - The "digital anatomy" concept
   - Why robots can't just "know" their structure
   - Analogy: humans have proprioception, robots need URDF

4. Links: The Rigid Bodies (FR-004, FR-005, FR-006, FR-007)
   - Definition: rigid bodies that don't deform
   - Humanoid examples: torso, thigh, shin, forearm, head
   - Properties: mass, center of mass, inertia, geometry (conceptual)
   - ASCII diagram: humanoid link hierarchy

5. Joints: The Connections (FR-008, FR-009, FR-010, FR-011)
   - Definition: functional connections between links
   - Joint types with humanoid mapping:
     - Revolute: hip, knee, elbow, shoulder
     - Fixed: skull-to-spine, sensor mounts
     - Prismatic: linear actuators (rare in humanoids)
     - Continuous: wheels (not typical for humanoids)
   - Joint properties: limits, friction, mimic

6. Kinematic Chains (FR-012, FR-013, FR-014, FR-015, FR-016)
   - Definition: sequence from base to end-effector
   - Leg chain: base_link → hip → thigh → knee → shin → ankle → foot
   - Arm chain: shoulder → upper_arm → elbow → forearm → wrist → hand
   - Forward kinematics concept (joint positions → end-effector position)
   - Connection to balance and walking
   - ASCII diagram: kinematic chain visualization

7. Transform Tree (TF) (FR-017, FR-018, FR-019, FR-020)
   - Definition: dynamic coordinate frame system
   - How TF knows "where everything is"
   - URDF (static structure) vs TF (runtime tracking)
   - ASCII diagram: humanoid TF tree hierarchy

8. Sensors and Frames (FR-021, FR-022, FR-023)
   - Sensors attached to links with coordinate frames
   - Camera frame, IMU frame, LiDAR frame
   - Connection to ROS 2 topics from Chapter 2

9. URDF vs SDF (FR-024, FR-025, FR-026)
   - URDF: robot structure focus
   - SDF: simulation environment (lights, terrain, physics)
   - When to use each: RViz vs Gazebo
   - Foreshadow Module 2

10. Try With AI (FR-032 - differentiated)
    - Explorer: Kinematic chain tracing exercises
    - Builder: Diagram interpretation (identify links/joints)
    - Engineer: TF tree construction from descriptions

11. References
    - IEEE format citations
```

### Variant Differentiation Strategy

| Section | Explorer | Builder | Engineer |
|---------|----------|---------|----------|
| Analogies | Software objects, class hierarchies | Arduino servo arms, 3D-printed robots | Industrial robot arms, ABB/KUKA |
| Depth | High-level conceptual | Moderate technical detail | Full technical depth |
| Examples | Simulated humanoid, game character rigs | Hobby robot arms, quadrupeds | Unitree G1, Boston Dynamics, industrial manipulators |
| Difficulty | Beginner | Intermediate | Advanced |
| Word Count | ~2800 | ~3000 | ~3500 |

### ASCII Diagram Specifications

**Diagram 1: Humanoid Link Hierarchy**
```text
                    [head_link]
                         │
                   [torso_link]
                    /    │    \
        [left_arm]    [spine]    [right_arm]
             │           │            │
        [forearm]   [pelvis]    [forearm]
             │       /    \          │
         [hand]  [left_leg] [right_leg]  [hand]
                    │          │
                [shin]      [shin]
                    │          │
                [foot]      [foot]
```

**Diagram 2: Kinematic Chain (Leg)**
```text
base_link ──[hip_joint]──► thigh_link ──[knee_joint]──► shin_link ──[ankle_joint]──► foot_link
              (revolute)                  (revolute)                   (revolute)
```

**Diagram 3: TF Tree**
```text
base_link
  ├── torso_link
  │     ├── head_link
  │     │     ├── camera_frame
  │     │     └── imu_frame
  │     ├── left_shoulder_link
  │     │     └── left_elbow_link
  │     │           └── left_hand_link
  │     └── right_shoulder_link
  │           └── ...
  ├── left_hip_link
  │     └── left_knee_link
  │           └── left_ankle_link
  │                 └── left_foot_link
  └── right_hip_link
        └── ...
```

## Project Structure

### Documentation (this feature)

```text
specs/006-m1-chapter-3-content/
├── plan.md              # This file
├── research.md          # Phase 0 output - IEEE citations
├── spec.md              # Feature specification
├── checklists/
│   └── requirements.md  # Quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Content Output (repository docs/)

```text
docs/module-1-robotic-nervous-system/
├── index.md                                    # Module index (update with Chapter 3)
├── chapter-3-urdf-modeling-explorer.md         # Explorer variant
├── chapter-3-urdf-modeling-builder.md          # Builder variant
└── chapter-3-urdf-modeling-engineer.md         # Engineer variant
```

**Structure Decision**: Content feature - markdown files in docs/ directory following existing chapter pattern.

## Definition of Done

- [ ] All three chapter variants created (Explorer, Builder, Engineer)
- [ ] Each variant includes all 10 content sections
- [ ] ASCII diagrams present in all variants (link hierarchy, kinematic chain, TF tree)
- [ ] Try With AI activities differentiated per variant
- [ ] IEEE citations present for all factual claims
- [ ] Zero code blocks or XML syntax in any variant
- [ ] Frontmatter complete with personaDifficulty, personalizationTags, ragKeywords
- [ ] Word count targets met (~2800/3000/3500)
- [ ] Module index updated with Chapter 3 links
- [ ] Docusaurus build passes without errors
- [ ] Constitution v1.2.0 compliance verified

## Complexity Tracking

No violations requiring justification - content feature follows established patterns from Chapter 1 and Chapter 2.
