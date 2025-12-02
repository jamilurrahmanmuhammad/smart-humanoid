# Feature Specification: Module 1 Chapter 3 - Humanoid Robot Modeling with URDF

**Feature Branch**: `006-m1-chapter-3-content`
**Created**: 2025-12-02
**Status**: Draft
**Input**: User description: "Create Module 1 Chapter 3: Humanoid Robot Modeling with URDF - conceptual foundations of robot description format"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Core URDF Concepts (Priority: P1)

As a reader who completed Chapter 2 (ROS 2 Architecture), I want to understand how humanoid robots are structurally described in ROS 2 so that I can visualize robots as hierarchical systems of connected parts before working with simulation.

**Why this priority**: URDF is the foundational robot description format in ROS 2. Without understanding links, joints, and their relationships, readers cannot comprehend simulation, control, or perception topics in later modules.

**Independent Test**: Can be fully tested by verifying readers can correctly identify links, joints, and their relationships in a humanoid robot diagram, and explain why structural modeling matters for robot control.

**Acceptance Scenarios**:

1. **Given** a reader who understands ROS 2 node communication, **When** they read the URDF introduction, **Then** they can explain what URDF represents and why explicit robot modeling is necessary.
2. **Given** a humanoid robot diagram showing limbs and connections, **When** readers analyze the structure, **Then** they can identify which parts are links and which are joints.
3. **Given** the concept of robot anatomy, **When** readers encounter different joint types (revolute, fixed, prismatic), **Then** they can match each type to appropriate humanoid body parts.

---

### User Story 2 - Kinematic Chain Understanding (Priority: P1)

As a reader learning about humanoid robots, I want to understand kinematic chains so that I can visualize how movement propagates from the robot's base to its end-effectors (hands, feet).

**Why this priority**: Kinematic chains are essential for understanding how humanoids move. Without this concept, readers cannot grasp balance, walking, or manipulation in later modules.

**Independent Test**: Can be fully tested by verifying readers can trace a kinematic chain from base to end-effector and explain why chain accuracy matters for robot balance.

**Acceptance Scenarios**:

1. **Given** the concept of sequential joint connections, **When** readers learn about kinematic chains, **Then** they can trace the path from base_link to a foot or hand.
2. **Given** a humanoid's leg structure, **When** readers analyze the chain, **Then** they can identify each link and joint in the sequence (hip to thigh to knee to shin to ankle to foot).
3. **Given** forward kinematics explained conceptually, **When** readers consider robot balance, **Then** they understand why precise chain modeling affects stability.

---

### User Story 3 - Transform Tree (TF) Concept (Priority: P1)

As a reader preparing for simulation and perception modules, I want to understand how ROS 2 tracks spatial relationships between robot parts so that I can later work with coordinate frames in simulation and sensor data.

**Why this priority**: TF tree is how ROS 2 knows "where everything is." This concept bridges structural modeling (URDF) with runtime behavior (perception, control). Essential before Module 2.

**Independent Test**: Can be fully tested by verifying readers can interpret a TF tree diagram and explain how it enables ROS 2 to track part positions.

**Acceptance Scenarios**:

1. **Given** a hierarchical tree diagram of robot frames, **When** readers study the TF concept, **Then** they can explain how parent-child relationships define spatial positions.
2. **Given** the relationship between URDF and TF, **When** readers connect these concepts, **Then** they understand that URDF defines static structure while TF provides dynamic position tracking.
3. **Given** a sensor attached to the robot head, **When** readers consider frame relationships, **Then** they can explain how TF enables transforming sensor data to the robot's base frame.

---

### User Story 4 - Physical Properties of Links (Priority: P2)

As a reader who will work with simulation later, I want to understand mass, center of mass, and inertia conceptually so that I can appreciate why these properties matter for realistic robot behavior.

**Why this priority**: Physical properties are essential for simulation accuracy but can be understood conceptually before implementation. Builds foundation for Module 2 physics simulation.

**Independent Test**: Can be fully tested by verifying readers can explain why a robot's mass distribution affects its balance and movement behavior.

**Acceptance Scenarios**:

1. **Given** the concept of a rigid body, **When** readers learn about link properties, **Then** they can explain why mass and center of mass matter for balance.
2. **Given** the concept of inertia, **When** readers consider arm movement, **Then** they understand why heavier links require more torque to accelerate.
3. **Given** a humanoid standing on one leg, **When** readers analyze balance requirements, **Then** they can explain how incorrect mass modeling would cause simulation inaccuracy.

---

### User Story 5 - Sensor and Actuator Representation (Priority: P2)

As a reader who completed Chapter 2 (ROS 2 topics/nodes), I want to understand how sensors and actuators are represented in robot models so that I can connect structural modeling to the communication architecture learned previously.

**Why this priority**: Bridges URDF structure with ROS 2 communication. Readers need to understand that sensors have frames and actuators connect to joints before working with sensor data.

**Independent Test**: Can be fully tested by verifying readers can explain how a camera's coordinate frame relates to the robot model and why sensor placement matters.

**Acceptance Scenarios**:

1. **Given** a camera sensor attached to the robot head, **When** readers analyze sensor representation, **Then** they can explain that the camera has its own coordinate frame attached to a link.
2. **Given** an actuator (motor) at a joint, **When** readers connect to ROS 2 concepts, **Then** they understand that joint commands flow through topics to control physical movement.
3. **Given** multiple sensors (camera, IMU, LiDAR) on a humanoid, **When** readers consider data fusion, **Then** they understand why each sensor's frame must be precisely defined relative to the robot base.

---

### User Story 6 - URDF vs SDF Distinction (Priority: P3)

As a reader preparing for Module 2 (simulation), I want to understand the conceptual difference between URDF and SDF so that I can appreciate why simulation environments may use different formats.

**Why this priority**: Sets expectations for Module 2 where SDF/Gazebo appears. Prevents confusion about why different formats exist. Conceptual only—no implementation details.

**Independent Test**: Can be fully tested by verifying readers can explain when URDF vs SDF would be appropriate and what each format emphasizes.

**Acceptance Scenarios**:

1. **Given** URDF's focus on robot structure, **When** readers learn about SDF's scope, **Then** they understand that SDF includes environment modeling (lights, terrain, physics properties).
2. **Given** the purpose of RViz (visualization) vs Gazebo (simulation), **When** readers compare formats, **Then** they can explain why URDF suffices for visualization but simulation often needs SDF.
3. **Given** the progression from robot description to simulation, **When** readers look ahead to Module 2, **Then** they understand that SDF will extend their URDF knowledge, not replace it.

---

### Edge Cases

- What happens when readers have no prior 3D/spatial reasoning experience? Content must include intuitive analogies (skeleton, puppet, articulated action figures).
- How does content handle readers who expect code examples? Explicit callouts that this chapter is conceptual; implementation comes in later modules.
- What if readers confuse URDF with actual robot hardware? Clear distinction that URDF is a model/description, not the physical robot.

## Requirements *(mandatory)*

### Functional Requirements

**Core URDF Concepts**

- **FR-001**: Chapter MUST explain what URDF is and what problems it solves for robotics systems
- **FR-002**: Chapter MUST describe URDF as the "digital anatomy" or "blueprint" of a robot
- **FR-003**: Chapter MUST explain why explicit robot modeling is necessary (cannot just "tell" the robot about itself)

**Links Requirements**

- **FR-004**: Chapter MUST define links as rigid bodies with no deformation
- **FR-005**: Chapter MUST provide humanoid examples of links (torso, thigh, shin, forearm, head, etc.)
- **FR-006**: Chapter MUST explain that each link has mass, center of mass, inertia, and geometric shape (conceptually)
- **FR-007**: Chapter MUST NOT include mathematical formulas for inertia tensors or mass matrices

**Joints Requirements**

- **FR-008**: Chapter MUST define joints as functional connections between links
- **FR-009**: Chapter MUST explain joint types: fixed, revolute, prismatic, continuous (conceptual definitions only)
- **FR-010**: Chapter MUST map joint types to humanoid body parts (hip=revolute, skull-to-spine=fixed, etc.)
- **FR-011**: Chapter MUST introduce joint limits, friction, and mimic concepts (conceptually)

**Kinematic Chains Requirements**

- **FR-012**: Chapter MUST define kinematic chain as sequence of joints from base to end-effector
- **FR-013**: Chapter MUST provide leg chain example: base_link to hip to thigh to knee to shin to ankle to foot
- **FR-014**: Chapter MUST provide arm chain example: shoulder to upper_arm to elbow to forearm to wrist to hand
- **FR-015**: Chapter MUST explain forward kinematics conceptually (how joint positions determine end-effector position)
- **FR-016**: Chapter MUST connect kinematic chains to balance and walking requirements

**TF Tree Requirements**

- **FR-017**: Chapter MUST explain TF as ROS 2's dynamic coordinate frame system
- **FR-018**: Chapter MUST explain how TF enables ROS 2 to know "where everything is"
- **FR-019**: Chapter MUST include ASCII diagram of humanoid TF tree hierarchy
- **FR-020**: Chapter MUST connect URDF (static definition) to TF (runtime tracking)

**Sensor/Actuator Requirements**

- **FR-021**: Chapter MUST explain how sensors are attached to links with coordinate frames
- **FR-022**: Chapter MUST explain sensor frames: camera frame, IMU frame, LiDAR frame
- **FR-023**: Chapter MUST connect sensor representation to ROS 2 topics from Chapter 2

**URDF vs SDF Requirements**

- **FR-024**: Chapter MUST compare URDF (robot structure) with SDF (simulation environment) conceptually
- **FR-025**: Chapter MUST explain when each format is appropriate (RViz vs Gazebo use cases)
- **FR-026**: Chapter MUST NOT include actual URDF/SDF syntax or XML examples

**Constitution v1.2.0 Content Requirements**

- **FR-027**: Chapter MUST be delivered as three variants: Explorer, Builder, Engineer
- **FR-028**: Explorer variant MUST use software/simulation analogies and high-level conceptual depth
- **FR-029**: Builder variant MUST use Arduino/Raspberry Pi/maker hardware context with moderate technical detail
- **FR-030**: Engineer variant MUST use industrial robotics context with full technical depth
- **FR-031**: All variants MUST share same learning objectives and IEEE citations; Try With AI activities are differentiated per FR-032
- **FR-032**: Chapter MUST end with "Try With AI" activity differentiated by variant: Explorer uses kinematic chain tracing exercises, Builder uses diagram interpretation (identify links/joints from descriptions), Engineer uses TF tree construction from robot descriptions
- **FR-033**: Chapter MUST include IEEE-format citations for all factual claims
- **FR-034**: Chapter MUST NOT contain any code blocks, XML, or implementation syntax

**Structural Requirements**

- **FR-035**: Chapter MUST include narrative introduction explaining why robots need explicit modeling
- **FR-036**: Chapter MUST include ASCII diagrams for: humanoid link hierarchy, TF tree, kinematic chain
- **FR-037**: Chapter MUST foreshadow Module 2 (Gazebo/SDF simulation) gently
- **FR-038**: Chapter frontmatter MUST include personaDifficulty, personalizationTags, and ragKeywords

### Key Entities

- **Link**: Rigid body component of a robot (torso, limb segment, head); has mass, inertia, geometry; connects to other links via joints
- **Joint**: Connection point between two links; defines motion type (revolute, fixed, prismatic); has limits, friction; enables/constrains movement
- **Kinematic Chain**: Ordered sequence of links and joints from base to end-effector; defines motion pathways; critical for movement planning
- **TF Tree**: Hierarchical coordinate frame system; tracks spatial relationships; updated dynamically during robot operation
- **Frame**: Coordinate system attached to a link or sensor; defines position/orientation reference; essential for sensor data interpretation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Readers can correctly identify links and joints in a humanoid robot diagram with 90% accuracy
- **SC-002**: Readers can trace a complete kinematic chain from base to end-effector without assistance
- **SC-003**: Readers can explain in plain language why URDF modeling is necessary for robot control
- **SC-004**: Readers can interpret a TF tree diagram and explain parent-child frame relationships
- **SC-005**: Readers can distinguish URDF from SDF and explain when each is appropriate
- **SC-006**: All three chapter variants build successfully in Docusaurus without errors
- **SC-007**: Each variant maintains word count targets: Explorer ~2800, Builder ~3000, Engineer ~3500
- **SC-008**: "Try With AI" activity is included and appropriate for robot modeling concepts
- **SC-009**: IEEE citations are present for all factual claims about URDF, TF, and robot modeling
- **SC-010**: Zero code blocks or XML syntax appear in any variant
- **SC-011**: Readers report increased confidence in understanding robot structure (qualitative feedback)
- **SC-012**: Chapter content prepares readers for Module 2 simulation topics without overwhelming them
- **SC-013**: Frontmatter metadata is complete and matches Constitution requirements

## Clarifications

### Session 2025-12-02

- Q: What type of Try With AI activity should each variant use? → A: Explorer uses kinematic chain tracing, Builder uses diagram interpretation (identify links/joints), Engineer uses TF tree construction from robot description.

## Assumptions

- Readers have completed Chapter 1 (Physical AI foundations) and Chapter 2 (ROS 2 architecture)
- Readers understand nodes, topics, services from Chapter 2
- Readers are familiar with generative AI tools but may not understand AI theory
- No prior 3D modeling or CAD experience is assumed
- No prior physics or mathematics background beyond basic intuition
- URDF is presented as ROS 2's standard; xacro and advanced tooling deferred to implementation modules
- ASCII diagrams are acceptable; no image assets required at this stage

## Out of Scope

- Writing actual URDF files or XML syntax
- Visual or collision mesh creation
- Gazebo/SDF simulation (covered in Module 2)
- xacro macros and parameterization
- Launch files for robot_state_publisher
- RViz visualization hands-on (deferred to implementation)
- Inverse kinematics mathematics
- Dynamics and physics equations
