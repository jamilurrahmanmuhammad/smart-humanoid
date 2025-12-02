---
title: "Chapter 3: Humanoid Robot Modeling with URDF"
sidebar_position: 10
safety: none
prerequisites:
  - understanding of ROS 2 architecture concepts (from Chapter 2)
  - familiarity with nodes, topics, and distributed systems
  - exposure to industrial robotics or mechanical engineering concepts
personaDifficulty: advanced
learningPath: engineer
personalizationTags:
  - urdf
  - robot_modeling
  - kinematic_chains
  - transform_tree
  - industrial
ragKeywords:
  - URDF
  - links
  - joints
  - kinematic chain
  - TF tree
  - transform
  - humanoid
  - robot description
  - inertia
  - dynamics
  - industrial manipulator
---

# Chapter 3: Humanoid Robot Modeling with URDF

## Learning Objectives

By the end of this chapter, you will be able to:

1. Explain URDF's role in the ROS 2 kinematic and dynamic pipeline
2. Describe humanoid anatomy using precise link and joint parameterization
3. Analyze kinematic chains for forward kinematics computation
4. Apply transform tree concepts to multi-sensor fusion problems
5. Evaluate URDF and SDF trade-offs for industrial applications

---

## The Model-Based Control Imperative

In Chapter 2, you examined how ROS 2 provides a distributed middleware for robot systems—nodes, topics, services, and actions forming the communication substrate. But communication infrastructure alone does not enable control. Industrial robots from ABB, KUKA, and Fanuc all share a common foundation: model-based control architectures that require precise mathematical descriptions of the manipulator.

Consider the control problem for a humanoid robot. A Unitree G1 has 23 degrees of freedom. Each actuator receives torque or position commands at kilohertz rates. The controller must solve several interrelated problems:

**Trajectory generation**: Given a desired end-effector path in Cartesian space, compute the joint-space trajectory that achieves it while respecting velocity, acceleration, and torque limits.

**Dynamic compensation**: Calculate the torques needed to overcome gravity, inertia, and Coriolis effects at each joint configuration.

**Collision avoidance**: Verify that no configuration along the planned trajectory causes self-collision or environmental collision.

**State estimation**: Fuse proprioceptive and exteroceptive sensor data into a unified state estimate, requiring knowledge of sensor placement.

None of these computations are possible without a formal kinematic and dynamic model of the robot. URDF (Unified Robot Description Format) provides this model in the ROS 2 ecosystem [1][2].

---

## URDF in the Control Pipeline

### Where URDF Fits

In industrial robotics, the kinematic model serves multiple subsystems:

| Subsystem | Model Requirement | URDF Provides |
|-----------|-------------------|---------------|
| Forward Kinematics | Link lengths, joint axes | Joint origins, axes, limits |
| Inverse Kinematics | Kinematic chain structure | Parent-child relationships |
| Dynamics | Mass, CoM, inertia tensors | Inertial element per link |
| Collision Detection | Geometry primitives or meshes | Collision element per link |
| Visualization | Visual representation | Visual element per link |
| State Publishing | Joint enumeration | Joint names and types |

URDF is the single source of truth for the robot's physical description. When correctly specified, it enables:

- `robot_state_publisher` to broadcast TF transforms
- MoveIt to compute motion plans
- Gazebo to simulate dynamics
- RViz to render the robot model
- Custom nodes to query kinematic/dynamic parameters

### The Kinematic Model

URDF encodes a kinematic tree—links connected by joints—where each joint defines a transformation from parent to child link. The robot's configuration is specified by the vector of joint positions q = [q₁, q₂, ..., qₙ]ᵀ.

For a serial chain, the end-effector pose is computed by composing joint transforms:

T₀ₙ(q) = T₀₁(q₁) · T₁₂(q₂) · ... · Tₙ₋₁,ₙ(qₙ)

Each Tᵢ,ᵢ₊₁ depends on the joint type (revolute, prismatic, etc.) and the static offset defined in URDF [3].

### The Dynamic Model

For torque-controlled robots, URDF's inertial parameters enable computation of the manipulator dynamics equation:

M(q)q̈ + C(q, q̇)q̇ + g(q) = τ

Where:
- M(q) is the mass matrix (depends on link masses and inertias)
- C(q, q̇) captures Coriolis and centrifugal effects
- g(q) is the gravity vector
- τ is the joint torque vector

Accurate inertial parameters in URDF are essential for computed torque control, impedance control, and simulation fidelity [4].

---

## Links: Rigid Body Parameterization

In URDF, each link is a rigid body with three component specifications: visual, collision, and inertial.

### Inertial Properties

The inertial element specifies:

**Mass**: Scalar mass m in kilograms.

**Origin**: The position and orientation of the center of mass (CoM) relative to the link frame.

**Inertia Tensor**: The 3×3 symmetric inertia matrix about the CoM, expressed in the CoM frame. Since it is symmetric, only six values are needed: Ixx, Iyy, Izz, Ixy, Ixz, Iyz.

For a link with uniform density, the inertia tensor can be computed from CAD software or analytical formulas. For example, a solid cylinder of mass m, radius r, and length l aligned with the z-axis has:

- Ixx = Iyy = (1/12)m(3r² + l²)
- Izz = (1/2)mr²
- Ixy = Ixz = Iyz = 0

Incorrect inertia values cause simulation instability and poor control performance. Industrial practice involves system identification or CAD-derived values [5].

### Humanoid Link Structure

A production humanoid like the Unitree G1 or Boston Dynamics Atlas has approximately 20-30 links. The structure forms a tree rooted at the pelvis or torso:

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

Each arm chain might have 7 DOF (shoulder: 3, elbow: 1, wrist: 3), each leg chain 6 DOF (hip: 3, knee: 1, ankle: 2), plus head and torso articulation [6][7].

### Collision Geometry Considerations

For motion planning, collision geometry must be:

**Conservative**: Bounding volumes should fully enclose the actual link geometry to prevent undetected collisions.

**Computationally efficient**: Complex meshes slow collision checking. Industrial practice uses primitive decomposition—cylinders, boxes, spheres—or convex hulls.

**Appropriately resolved**: Too coarse loses precision; too fine loses performance. The balance depends on planning cycle time requirements.

URDF supports boxes, cylinders, spheres, and mesh files. For real-time planning at 10+ Hz, primitive decomposition is often preferred over high-resolution meshes.

---

## Joints: Kinematic Constraints

Joints in URDF define the relative motion between parent and child links. The specification includes:

### Joint Types

**Revolute**: Rotation about a single axis with position limits [lower, upper]. The transform is a rotation about the specified axis by angle q.

**Continuous**: Unlimited rotation about an axis. Used for wheels or rotating tools. Mathematically identical to revolute without limits.

**Prismatic**: Translation along a single axis with position limits. The transform is a translation by distance d along the axis.

**Fixed**: Zero degrees of freedom. The child link is rigidly attached to the parent. Useful for sensors, end-effectors, or structural components.

**Floating** and **Planar**: Six-DOF and three-DOF joints respectively. Rarely used; typically for simulating free-flying or ground-contact robots.

### Joint Parameterization

Each joint defines:

**Origin**: The transform from parent link frame to joint frame when q = 0. This is the "home" configuration.

**Axis**: Unit vector [x, y, z] defining the rotation or translation axis.

**Limits**: For revolute/prismatic joints:
- Position limits (radians or meters)
- Velocity limits (rad/s or m/s)
- Effort limits (Nm or N)

**Dynamics**: Optional friction and damping coefficients for simulation.

**Mimic**: Allows one joint to mimic another with a multiplier and offset. Used for coupled finger joints in grippers.

### Industrial Joint Mapping

Consider the joint configuration for a 6-DOF industrial manipulator:

| Joint | Type | Axis | Typical Limits |
|-------|------|------|----------------|
| Base rotation | Revolute | Z | ±180° |
| Shoulder | Revolute | Y | -90° to +90° |
| Elbow | Revolute | Y | -135° to +0° |
| Wrist 1 | Revolute | Y | ±180° |
| Wrist 2 | Revolute | Z | ±120° |
| Wrist 3 | Revolute | Y | ±360° |

Humanoid joints follow similar patterns. Hip joints typically have three revolute DOF (flexion/extension, abduction/adduction, rotation), while the knee has one (flexion/extension) [8].

---

## Kinematic Chains and Forward Kinematics

### Serial Kinematic Chains

A kinematic chain is the sequence of links and joints from a base frame to an end-effector frame. For humanoids, multiple chains share the same root:

**Right arm chain**: torso → shoulder → upper_arm → elbow → forearm → wrist → hand

**Left leg chain**: pelvis → hip → thigh → knee → shin → ankle → foot

Each chain can be analyzed independently for forward/inverse kinematics, though dynamics couples them through the base [9].

### Forward Kinematics Computation

Given joint positions q, forward kinematics computes end-effector pose:

For the right arm with joints q = [q₁, q₂, q₃, q₄, q₅, q₆, q₇]ᵀ:

```text
torso ──[shoulder_pitch]──► shoulder ──[shoulder_roll]──► upper_arm ──[shoulder_yaw]──► ...
              q₁                            q₂                             q₃

... ──[elbow_pitch]──► forearm ──[wrist_roll]──► wrist ──[wrist_pitch]──► wrist2 ──[wrist_yaw]──► hand
            q₄                       q₅                      q₆                        q₇
```

The hand frame pose relative to torso is:

T_hand = T_shoulder(q₁) · T_upper_arm(q₂) · T_forearm(q₃) · T_wrist(q₄) · T_wrist2(q₅) · T_wrist3(q₆) · T_hand(q₇)

ROS 2's `tf2` library performs these computations using URDF-derived transforms [10].

### Jacobian and Singularities

The manipulator Jacobian J(q) relates joint velocities to end-effector velocity:

ẋ = J(q)q̇

Where ẋ is the 6×1 end-effector twist (linear and angular velocity). The Jacobian is computed from URDF using:

Jᵢ = [zᵢ × (p - pᵢ)] for revolute joint i
     [zᵢ]

     [zᵢ] for prismatic joint i
     [0]

At singular configurations (det(J) = 0), inverse kinematics becomes ill-conditioned. Common singularities occur at:
- Fully extended configurations (arm straight)
- Wrist singularities (alignment of consecutive rotation axes)
- Shoulder singularities (overhead configurations)

Motion planners must detect and handle these cases [11].

---

## Transform Tree: Multi-Frame State Estimation

### TF Architecture

The Transform Tree (TF) in ROS 2 maintains a directed acyclic graph of coordinate frames, updated in real-time as joints move. Key characteristics:

**Static transforms**: Fixed relationships (sensor mounts, fixed joints). Published once or periodically with long validity.

**Dynamic transforms**: Joint-dependent relationships. Published at the joint state update rate.

**Time-stamped**: Each transform has a timestamp. TF can interpolate or extrapolate for temporal alignment.

**Queryable**: Any node can request the transform between any two frames at any time [12].

### Humanoid TF Tree

A humanoid's TF tree reflects the URDF structure:

```text
base_link
  ├── torso_link
  │     ├── head_link
  │     │     ├── camera_frame
  │     │     ├── camera_optical_frame
  │     │     └── imu_frame
  │     ├── left_shoulder_link
  │     │     └── left_elbow_link
  │     │           └── left_wrist_link
  │     │                 └── left_hand_link
  │     │                       └── left_force_sensor_frame
  │     └── right_shoulder_link
  │           └── right_elbow_link
  │                 └── right_wrist_link
  │                       └── right_hand_link
  │                             └── right_force_sensor_frame
  ├── left_hip_link
  │     └── left_knee_link
  │           └── left_ankle_link
  │                 └── left_foot_link
  │                       └── left_foot_force_sensor_frame
  └── right_hip_link
        └── right_knee_link
              └── right_ankle_link
                    └── right_foot_link
                          └── right_foot_force_sensor_frame
```

### Multi-Sensor Fusion Application

Consider a manipulation task where the robot must grasp an object detected by a head-mounted camera:

1. **Camera publishes detection**: Object at position [x, y, z] in camera_optical_frame
2. **TF query**: Transform from camera_optical_frame to right_hand_link
3. **Grasp planning**: Compute approach trajectory in hand frame
4. **Execution**: Transform trajectory to joint space

Each step requires TF. Without accurate transforms, the hand misses the object. Industrial tolerances for manipulation are often sub-centimeter, requiring careful URDF calibration [13].

---

## Sensor Frames and Conventions

### Standard Frame Conventions

ROS Enhancement Proposals define standard conventions:

**REP 103** (Coordinate Frames):
- X forward, Y left, Z up for robot body frames
- Right-hand rule for rotation
- SI units (meters, radians, seconds)

**REP 105** (Mobile Platforms):
- `base_link`: Robot body frame
- `odom`: Odometry frame (continuous, drifts)
- `map`: World frame (discontinuous, corrected)

**REP 104** (Camera Frames):
- Camera optical frame: Z forward, X right, Y down
- Camera body frame: Standard REP 103 orientation

### Industrial Sensor Placement

For humanoid manipulation, typical sensor frames include:

**Stereo cameras (head)**: Depth perception for object detection and SLAM. Frame offset from head link with camera optical convention.

**IMU (torso)**: Orientation and acceleration for state estimation. Frame aligned with robot body axes.

**Force/torque sensors (wrists, feet)**: Contact force measurement. Frame at the sensor origin with Z along the sensitive axis.

**Joint encoders**: Implicit in joint states. Not separately framed but provide q measurements.

**LiDAR (optional)**: For navigation and obstacle detection. Frame origin at scanner center [14][15].

### Sensor-to-TF Integration

Each sensor driver must:

1. Publish sensor data with correct timestamp
2. Broadcast sensor frame to TF (or rely on robot_state_publisher for static mounts)
3. Use consistent frame_id in message headers

Downstream fusion nodes query TF to relate sensor measurements. Time synchronization is critical—TF extrapolation beyond buffer limits fails.

---

## URDF and SDF: Format Trade-offs

### URDF Capabilities and Limitations

URDF is optimized for single-robot description:

**Strengths**:
- Native ROS 2 integration (robot_state_publisher, MoveIt)
- Clear link-joint hierarchy
- Sufficient for most robot state publishing and visualization

**Limitations**:
- Single robot only (no multi-robot environments)
- No world description (terrain, obstacles, lighting)
- Limited physics parameters (no friction models beyond simple damping)
- No closed kinematic loops (parallel mechanisms require workarounds)
- No model nesting (cannot include URDF within URDF) [16]

### SDF Capabilities

SDF (Simulation Description Format) extends beyond robot description:

**World modeling**: Complete simulation environments with terrain, obstacles, and lighting.

**Multi-robot**: Multiple robots in one simulation.

**Physics properties**: Detailed friction, contact, and constraint parameters.

**Model composition**: Nested models with relative poses.

**Sensor simulation**: Gazebo-specific sensor plugins with noise models.

Gazebo uses SDF natively. URDF robots are internally converted to SDF for simulation [17].

### Industrial Decision Matrix

| Requirement | Format | Reasoning |
|-------------|--------|-----------|
| ROS 2 visualization | URDF | Native RViz support |
| Motion planning | URDF | MoveIt uses URDF |
| Simple simulation | URDF→SDF | Automatic conversion |
| Multi-robot simulation | SDF | Required for world description |
| HIL testing | SDF | Environment modeling needed |
| Deployment | URDF | robot_state_publisher uses URDF |

### Practical Workflow

For production humanoid development:

1. **Maintain URDF** as the canonical robot description
2. **Auto-convert to SDF** via Gazebo's spawn mechanisms
3. **Create SDF world files** for simulation environments
4. **Use URDF for runtime** (robot_state_publisher, MoveIt, visualization)

Module 2 will detail this workflow with practical implementation.

---

## Try With AI

Test your understanding with this TF tree construction exercise.

**Prompt to use:**

```
I'm learning about URDF and TF trees for industrial robotics. Help me construct the TF tree for a 7-DOF humanoid arm with the following specifications:

Kinematic chain:
- torso_link (base)
- shoulder_pitch_joint (revolute, Y-axis)
- shoulder_link
- shoulder_roll_joint (revolute, X-axis)
- upper_arm_link
- shoulder_yaw_joint (revolute, Z-axis)
- elbow_pitch_joint (revolute, Y-axis)
- forearm_link
- wrist_roll_joint (revolute, X-axis)
- wrist_link
- wrist_pitch_joint (revolute, Y-axis)
- wrist_yaw_joint (revolute, Z-axis)
- hand_link

Sensors:
- Force/torque sensor between wrist and hand (fixed joint)
- Camera on hand palm facing forward (fixed joint)

Questions:
1. Draw the TF tree structure
2. How many transforms are needed to compute hand-to-torso position?
3. If the shoulder_pitch_joint is at 45°, what is the rotation matrix for T_shoulder_link?
4. What are the potential singularities in this configuration?
5. If I want to compute the camera's view of an object in torso coordinates, what TF query would I use?

Then, give me a similar exercise for a 6-DOF leg chain with foot force sensors.
```

**What to look for:**
- TF tree should show proper parent-child relationships
- Transform count should equal the number of joints plus fixed sensor mounts
- Singularities occur when rotation axes align (gimbal lock) or at full extension
- TF queries should use proper frame names: lookupTransform(torso_link, camera_frame)

---

## References

[1] Open Robotics, "URDF - Unified Robot Description Format," ROS 2 Documentation, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html

[2] S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall, "Robot Operating System 2: Design, architecture, and uses in the wild," Science Robotics, vol. 7, no. 66, May 2022. [Online]. Available: https://www.science.org/doi/10.1126/scirobotics.abm6074

[3] B. Siciliano, L. Sciavicco, L. Villani, and G. Oriolo, Robotics: Modelling, Planning and Control. London, UK: Springer, 2009, pp. 39-100.

[4] R. Featherstone, Rigid Body Dynamics Algorithms. New York, NY: Springer, 2008, ch. 2.

[5] Open Robotics, "URDF Link Element," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML/link

[6] Unitree Robotics, "G1 Humanoid Robot," Unitree Documentation, 2024. [Online]. Available: https://www.unitree.com/g1

[7] Boston Dynamics, "Atlas Technical Specifications," Boston Dynamics, 2024. [Online]. Available: https://bostondynamics.com/atlas/

[8] Open Robotics, "URDF Joint Element," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML/joint

[9] J. J. Craig, Introduction to Robotics: Mechanics and Control, 4th ed. London, UK: Pearson, 2018, ch. 3.

[10] Open Robotics, "tf2 - ROS 2 Documentation," docs.ros.org, 2024. [Online]. Available: https://docs.ros.org/en/humble/Concepts/Intermediate/About-Tf2.html

[11] M. W. Spong, S. Hutchinson, and M. Vidyasagar, Robot Modeling and Control, 2nd ed. Hoboken, NJ: Wiley, 2020, ch. 4.

[12] Open Robotics, "Introduction to tf2," ROS 2 Tutorials, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html

[13] T. Foote, "tf: The Transform Library," in Proc. IEEE Int. Conf. Technologies for Practical Robot Applications (TePRA), Woburn, MA, 2013, pp. 1-6.

[14] REP 103, "Standard Units of Measure and Coordinate Conventions," ROS Enhancement Proposals, 2010. [Online]. Available: https://www.ros.org/reps/rep-0103.html

[15] REP 105, "Coordinate Frames for Mobile Platforms," ROS Enhancement Proposals, 2010. [Online]. Available: https://www.ros.org/reps/rep-0105.html

[16] D. V. Lu, "URDF XML Specification," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML

[17] Open Source Robotics Foundation, "SDFormat Specification," sdformat.org, 2024. [Online]. Available: http://sdformat.org/spec

