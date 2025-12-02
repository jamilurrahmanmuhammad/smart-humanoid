---
title: "Chapter 3: Humanoid Robot Modeling with URDF"
sidebar_position: 9
safety: none
prerequisites:
  - understanding of ROS 2 architecture concepts (from Chapter 2)
  - familiarity with nodes, topics, and distributed systems
  - basic experience with hobby robotics or 3D printing
personaDifficulty: intermediate
learningPath: builder
personalizationTags:
  - urdf
  - robot_modeling
  - kinematic_chains
  - transform_tree
  - maker
ragKeywords:
  - URDF
  - links
  - joints
  - kinematic chain
  - TF tree
  - transform
  - humanoid
  - robot description
  - servo
  - actuator
---

# Chapter 3: Humanoid Robot Modeling with URDF

## Learning Objectives

By the end of this chapter, you will be able to:

1. Explain what URDF is and why robots need a body model
2. Map physical robot parts to URDF links and joints
3. Understand kinematic chains and how they affect servo coordination
4. Visualize a robot as a transform tree (TF) for sensor integration
5. Distinguish between URDF and SDF and know when to use each

---

## Your Servo Arm Knows Its Angles—But Does It Know Its Arm?

If you have built a servo-based robot arm or a 3D-printed quadruped, you have probably written code that commands servos to specific angles. "Move servo 1 to 45 degrees, servo 2 to 90 degrees." The servos obey, and the arm moves. But here is a question: does your robot actually know where its gripper ends up?

Consider what happens when you change the length of a link—maybe you printed a longer forearm segment. Your old servo angles no longer produce the same end position. The gripper overshoots or undershoots the target. This happens because your control code does not have a model of the arm's geometry. It only knows servo angles, not arm structure.

In Chapter 2, you learned how ROS 2 provides the communication backbone for robots—nodes publishing sensor data, services handling requests, actions managing complex tasks. But ROS 2 needs something more: a description of the robot itself. Without knowing what the robot looks like—how long the arms are, where the cameras are mounted, how the joints connect—the software cannot perform intelligent motion planning or sensor fusion.

This is where URDF (Unified Robot Description Format) comes in. URDF is the standard way to describe a robot's physical structure in ROS 2. Think of it as the CAD model your software uses to understand the machine it controls [1].

---

## Why Your Robot Needs a Body Model

### The Maker's Problem

When you build a robot from servos and 3D-printed parts, you know exactly how it is constructed. You designed it. But your software does not have access to your mental model. Consider the challenges:

**End-effector positioning**: You want the gripper to reach a specific point in space. With just servo angles, you cannot calculate this—you need link lengths, joint orientations, and the chain connecting base to gripper.

**Collision avoidance**: Will the arm hit the robot's own body if you command these joint angles? Without geometry information, there is no way to check.

**Sensor interpretation**: Your camera sees an object. Where is that object relative to the robot's base? The camera is mounted somewhere on the robot, but where exactly?

**Simulation testing**: Before running on hardware, you want to test in Gazebo. The simulator needs exact dimensions and physical properties to model behavior correctly.

### The URDF Solution

URDF provides a structured format to describe:

- **Links**: The rigid parts of your robot (3D-printed segments, the gripper, the base)
- **Joints**: The connections between parts (where your servos are)
- **Physical properties**: Mass, dimensions, and visual/collision geometry
- **Sensor locations**: Where cameras, IMUs, and other sensors are mounted

With this description, ROS 2 tools can compute forward kinematics (where does the gripper end up given joint angles?), check for collisions, render the robot in visualization tools, and integrate sensor data spatially [2].

---

## Links: Your Robot's Rigid Parts

In URDF, every rigid piece of your robot is a **link**. If you have built a 6-DOF arm, you might have:

- Base link (mounted to a table or body)
- Shoulder link (first rotating segment)
- Upper arm link
- Forearm link
- Wrist link
- Gripper link (end-effector)

### What Makes a Link

A link in URDF has several components:

**Visual geometry**: What the link looks like. This could be a simple shape (cylinder, box) or a mesh file from your CAD software. When you view your robot in RViz, this is what renders.

**Collision geometry**: The shape used for collision detection. Often simplified compared to visual geometry for faster computation. A detailed mesh might become a bounding box for collision checks.

**Inertial properties**: Mass, center of mass, and inertia tensor. These matter for dynamics simulation and balance calculations.

### Humanoid Link Example

A humanoid robot scales up the concept. Instead of a 6-DOF arm, you have two arms, two legs, a torso, and a head. Each segment becomes a link:

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

This tree structure is not arbitrary. It reflects how motion propagates: move the torso, and everything attached moves with it. Move the shoulder, and the entire arm follows [3].

### Physical Properties Matter

For makers building real robots, link properties have practical consequences:

**Mass distribution** affects balance. If your robot arm's gripper is heavy, the arm may droop or require more torque. URDF captures this so simulation matches reality.

**Center of mass** determines pivot points. A link's COM affects how forces transmit through the structure.

**Inertia** describes resistance to rotation. A long, thin arm link has different inertia than a compact, chunky one. This affects how quickly servos can accelerate and decelerate the link.

When your simulation does not match your real robot, incorrect link properties are often the cause [4].

---

## Joints: Where Your Servos Live

Links are the structure; **joints** are what connect them and enable motion. In a physical robot, a joint typically corresponds to a servo or motor.

### Joint Types in URDF

**Revolute joints** rotate around an axis with limits. This matches most hobby servos—they rotate to a commanded angle within a range (often 0-180 degrees or similar). Your elbow joint, shoulder pitch, and hip rotate this way.

**Continuous joints** rotate without limits. These match motors that can spin freely, like wheels or rotating sensors.

**Prismatic joints** slide linearly. These match linear actuators—less common in humanoids but useful for grippers or telescoping mechanisms.

**Fixed joints** have no motion. They rigidly attach one link to another. Use these for sensor mounts or decorative parts that do not move.

### Mapping Your Hardware

Consider a typical hobby arm:

| Physical Part | URDF Element | Joint Type |
|---------------|--------------|------------|
| Base servo | shoulder_joint | Revolute |
| Upper arm servo | elbow_joint | Revolute |
| Wrist servo | wrist_joint | Revolute |
| Gripper servo | gripper_joint | Prismatic (or revolute) |
| Camera bracket | camera_joint | Fixed |

Each revolute joint needs:
- **Axis**: Which direction does it rotate? X, Y, or Z?
- **Limits**: What are the min/max angles? Match your servo's physical limits.
- **Parent/child**: Which link connects to which?

### Joint Properties for Servos

When modeling servo joints, these properties matter:

**Position limits**: Match your servo's mechanical range. A servo that physically moves 0-180 degrees should have limits reflecting that.

**Velocity limits**: How fast can the joint move? This affects motion planning feasibility.

**Effort limits**: Maximum torque. Smaller servos have lower torque limits.

Getting these right ensures simulation behavior matches your hardware [5].

---

## Kinematic Chains: From Base to Gripper

When you command your robot arm to reach a point in space, you are not directly commanding that point—you are commanding joint angles. The relationship between joint angles and end-effector position depends on the **kinematic chain**: the sequence of links and joints from base to end-effector.

### Your Arm as a Chain

For a simple 3-DOF arm:

```text
base_link ──[shoulder_joint]──► upper_arm ──[elbow_joint]──► forearm ──[wrist_joint]──► gripper
              (revolute)                       (revolute)                (revolute)
```

The gripper's position depends on:
1. Shoulder rotation angle
2. Upper arm length
3. Elbow rotation angle
4. Forearm length
5. Wrist rotation angle
6. Gripper offset from wrist

Change any of these, and the gripper ends up somewhere different.

### Forward Kinematics

Given joint angles, calculate end-effector position. This is **forward kinematics** (FK).

Your ROS 2 system needs FK for:
- Knowing where the gripper currently is
- Collision checking (where is every link in space?)
- Sensor fusion (where is the camera pointing?)

Forward kinematics requires the URDF because it depends on link lengths and joint axes [6].

### Inverse Kinematics

Given a desired end-effector position, calculate the joint angles needed. This is **inverse kinematics** (IK).

IK is what makes "move gripper to position X,Y,Z" possible. It is mathematically harder than FK—often there are multiple solutions or no solution at all. But with a correct URDF, ROS 2 planning tools can solve IK automatically.

### Humanoid Chains

A humanoid has multiple kinematic chains operating simultaneously:

**Arm chains** (2): From torso to each hand. Used for manipulation.

**Leg chains** (2): From pelvis to each foot. Critical for walking and balance.

**Head chain**: From torso to camera sensors. Used for gaze control.

During walking, the leg chains must coordinate precisely. The position of each foot—determined by hip, knee, and ankle angles—affects whether the robot stands or falls. Balance controllers continuously compute these chain positions [7].

---

## The Transform Tree: Real-Time Position Tracking

URDF describes the robot's structure, but it is static—it does not know the current joint angles. The **Transform Tree (TF)** provides real-time tracking of where every link is in space.

### How TF Works

As your robot moves, joint state publishers broadcast current angles to ROS 2 topics. The TF system uses the URDF and current joint angles to compute the transform (position and orientation) of every link.

Think of it like this:
- URDF = the blueprint (fixed structure)
- Joint states = current measurements (changing)
- TF = the live map showing where everything is right now

Any ROS 2 node can query TF to get the transform between any two frames at any time [8].

### Why Builders Need TF

**Sensor fusion**: Your gripper camera sees an object 30cm ahead. Where is that in robot coordinates? TF provides the camera-to-base transform.

**Motion validation**: Before commanding a motion, check if the planned positions are valid. TF lets you compute where links will be.

**Debugging**: When your robot misbehaves, TF visualization shows exactly where the system thinks links are. Mismatches reveal calibration errors.

### TF Tree Structure

The TF tree mirrors your URDF link hierarchy:

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
  │           └── right_elbow_link
  │                 └── right_hand_link
  ├── left_hip_link
  │     └── left_knee_link
  │           └── left_ankle_link
  │                 └── left_foot_link
  └── right_hip_link
        └── right_knee_link
              └── right_ankle_link
                    └── right_foot_link
```

Each node in this tree has a transform to its parent. The system can compute any transform by traversing the tree [9].

---

## Sensors and Their Frames

When you add sensors to your robot, they need to be positioned in the URDF. A camera mounted on the head sees the world from a specific viewpoint—and the system needs to know that viewpoint.

### Mounting Sensors in URDF

Sensors attach to links with fixed joints. The joint specifies the sensor's position and orientation relative to the parent link.

For example, a camera mounted on the head:
- Parent link: head_link
- Child link: camera_link
- Joint type: fixed
- Position: 5cm forward, 2cm up from head_link center
- Orientation: facing forward

This creates a **camera_frame** that the camera driver uses when publishing images.

### Common Sensor Frames

**Camera optical frame**: The coordinate system from the camera's perspective. Z-axis points along the viewing direction. Image processing results are in this frame.

**IMU frame**: The inertial measurement unit's orientation. Accelerometer and gyroscope readings are relative to this frame.

**LiDAR frame**: The laser scanner's origin. Point clouds are measured from this position.

**Force sensor frame**: In the wrist or gripper, measuring contact forces.

### Connecting Sensors to ROS 2

From Chapter 2, you know sensors publish to topics. A camera publishes images to `/camera/image`. But that data is only useful if you know where the camera is.

The sensor driver broadcasts its frame to TF. Any node processing camera data can look up the camera-to-robot transform and interpret the data correctly [10].

---

## URDF vs SDF: When to Use Each

As a maker, you will encounter two robot description formats: URDF and SDF. Understanding the difference helps you choose correctly.

### URDF: Robot Description

URDF describes a single robot:
- Links and joints
- Visual and collision geometry
- Physical properties
- Sensor attachments

ROS 2 tools (RViz, robot_state_publisher, MoveIt) work natively with URDF. When you want to visualize your robot or plan motions, you use URDF [11].

**Limitations**: URDF cannot describe:
- Multiple robots
- The environment (walls, obstacles, terrain)
- Lighting
- Advanced physics properties

### SDF: Simulation Worlds

SDF (Simulation Description Format) describes entire simulated environments:
- Multiple robots
- Static objects (tables, walls, furniture)
- Dynamic objects (balls, doors)
- Terrain and ground planes
- Lighting and visual settings
- Physics engine parameters

Gazebo, the primary ROS 2 simulator, uses SDF. When you simulate your robot picking up objects from a table, the table and objects are defined in SDF [12].

### Practical Workflow

For makers, the typical workflow is:

1. **Create URDF** for your robot. This describes your physical robot for ROS 2 tools.

2. **Convert or embed in SDF** for simulation. Gazebo can convert URDF to SDF automatically, or you can embed URDF within an SDF world.

3. **Create SDF world** with environment objects. Add tables, walls, and test objects.

4. **Run simulation** using Gazebo with SDF. Your robot (from URDF) operates in the environment (from SDF).

5. **Deploy to hardware** using URDF. ROS 2 tools on the real robot use URDF for state publishing and motion planning.

Module 2 will walk through this workflow in detail with hands-on exercises.

---

## Try With AI

Test your understanding with this diagram interpretation exercise. Use your preferred AI assistant.

**Prompt to use:**

```
I'm learning about URDF for building hobby robots. Look at this robot arm diagram and help me identify the URDF elements:

Robot arm description:
- A base that rotates left/right (like a lazy susan)
- An upper arm segment that tilts up/down
- A forearm segment that tilts up/down
- A wrist that rotates
- A two-finger gripper that opens/closes

For each part, identify:
1. Is it a link or a joint?
2. If a joint, what type (revolute, prismatic, fixed)?
3. What is the parent and child relationship?

Then, draw an ASCII diagram showing the kinematic chain from base to gripper fingertip.

Finally, if I 3D-printed a longer forearm segment (20cm instead of 15cm):
- What would I need to update in the URDF?
- How would this affect the robot's reach?
- Would my old motion plans still work?
```

**What to look for:**
- The base rotation, upper arm tilt, forearm tilt, and wrist rotation are all revolute joints
- The gripper might be prismatic (if fingers slide) or revolute (if fingers pivot)
- Link lengths directly affect reach calculations
- Changing link dimensions requires URDF updates for accurate motion planning

Compare your AI's answers with this chapter. Ask follow-up questions if anything is unclear.

---

## References

[1] Open Robotics, "URDF - Unified Robot Description Format," ROS 2 Documentation, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html

[2] Open Robotics, "Building a Visual Robot Model from Scratch," ROS 2 Documentation, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-with-URDF-from-Scratch.html

[3] D. V. Lu, "URDF XML Specification," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML

[4] Open Robotics, "URDF Link Element," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML/link

[5] Open Robotics, "URDF Joint Element," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML/joint

[6] B. Siciliano, L. Sciavicco, L. Villani, and G. Oriolo, Robotics: Modelling, Planning and Control. London, UK: Springer, 2009, pp. 39-100.

[7] J. J. Craig, Introduction to Robotics: Mechanics and Control, 4th ed. London, UK: Pearson, 2018, ch. 3.

[8] Open Robotics, "tf2 - ROS 2 Documentation," docs.ros.org, 2024. [Online]. Available: https://docs.ros.org/en/humble/Concepts/Intermediate/About-Tf2.html

[9] Open Robotics, "Introduction to tf2," ROS 2 Tutorials, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html

[10] REP 103, "Standard Units of Measure and Coordinate Conventions," ROS Enhancement Proposals, 2010. [Online]. Available: https://www.ros.org/reps/rep-0103.html

[11] R. Featherstone, Rigid Body Dynamics Algorithms. New York, NY: Springer, 2008, ch. 2.

[12] Open Source Robotics Foundation, "SDFormat Specification," sdformat.org, 2024. [Online]. Available: http://sdformat.org/spec

