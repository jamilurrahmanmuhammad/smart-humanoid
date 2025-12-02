---
title: "Chapter 3: Humanoid Robot Modeling with URDF"
sidebar_position: 8
safety: none
prerequisites:
  - understanding of ROS 2 architecture concepts (from Chapter 2)
  - familiarity with nodes, topics, and distributed systems
personaDifficulty: beginner
learningPath: explorer
personalizationTags:
  - urdf
  - robot_modeling
  - kinematic_chains
  - transform_tree
ragKeywords:
  - URDF
  - links
  - joints
  - kinematic chain
  - TF tree
  - transform
  - humanoid
  - robot description
---

# Chapter 3: Humanoid Robot Modeling with URDF

## Learning Objectives

By the end of this chapter, you will be able to:

1. Explain what URDF is and why robots need a body model
2. Describe humanoid anatomy in terms of links (rigid bodies) and joints (connections)
3. Understand kinematic chains and their role in robot movement
4. Visualize a robot as a transform tree (TF) that tracks spatial relationships
5. Distinguish between URDF and SDF conceptually

---

## A Robot Cannot Walk Until It Knows Its Own Body

In Chapter 2, you learned how ROS 2 enables a robot's nervous system—the communication infrastructure that allows sensors, processors, and motors to work together. But there is a fundamental question we have not yet answered: How does a robot know what it is?

Consider this problem. You are standing in a room, and someone asks you to touch your right elbow to your left knee. Without thinking, you can do this. Your brain knows where your elbow is, how long your forearm is, which direction your knee bends, and how all these parts connect. This spatial self-awareness—called proprioception in biology—is something humans take for granted.

A robot has no such innate knowledge. When a humanoid robot is first turned on, its processors have no idea that the robot has two legs, or that those legs have knees, or that the knees only bend in one direction. The robot does not know how long its arms are, where its cameras are mounted, or how heavy its torso is. Without this information, the robot cannot plan movements, maintain balance, or even understand sensor data in context.

This is where URDF comes in. URDF (Unified Robot Description Format) is the digital anatomy of a robot—a structured description that tells the robot's software exactly what the robot looks like, how its parts connect, and how those parts can move [1].

---

## Why Robots Need a Body Model

Think of URDF as a robot's self-image. Just as you have a mental model of your own body that lets you navigate the world without bumping into things, a robot needs a computational model of its structure to function effectively.

### The Problem Without a Body Model

Imagine writing software to control a humanoid robot without any description of the robot's structure. You would face immediate problems:

**Movement Planning**: How far should the arm motors rotate to reach a cup on a table? Without knowing arm length, joint positions, and how joints connect, this calculation is impossible.

**Balance Control**: Where is the robot's center of mass? If the robot reaches forward, will it tip over? These questions require knowing the weight and position of every body part.

**Sensor Interpretation**: A camera sees an object two meters ahead. But where is "ahead" relative to the robot's body? If the camera is mounted on the head, which can turn, the answer depends on the head's current position.

### The Solution: A Structured Body Description

URDF solves these problems by providing a complete description of the robot in a format that software can understand. Think of it like the difference between describing a building with words versus providing architectural blueprints. The blueprints give precise, computable information that architects and engineers can use.

A URDF description includes:
- What rigid parts the robot has (called **links**)
- How those parts connect (called **joints**)
- What movements each connection allows
- Physical properties like mass and dimensions

This is exactly the information that motion planning, balance control, and sensor fusion software need to function [2].

---

## Links: The Rigid Bodies

In URDF, a robot is modeled as a collection of **links**—rigid bodies that do not bend or deform during normal operation. If you think of the human body, links would be the bones: the femur, the tibia, the humerus, the skull.

### Humanoid Links

A typical humanoid robot has links corresponding to:

- **Head**: Contains cameras, microphones, and often processing units
- **Torso**: The central body, connecting arms, legs, and head
- **Upper arm**: From shoulder to elbow
- **Forearm**: From elbow to wrist
- **Hand**: The end-effector for grasping
- **Thigh**: From hip to knee
- **Shin**: From knee to ankle
- **Foot**: The ground contact surface

Each link has properties that matter for control and simulation:

**Geometry**: The physical shape—is it a cylinder, a box, or a complex mesh?

**Mass**: How heavy is this part? A 2 kg forearm behaves differently than a 0.5 kg forearm.

**Center of Mass**: Where is the weight concentrated? This affects balance calculations.

**Inertia**: How does the part resist rotation? A long, thin rod rotates differently than a compact sphere of the same mass.

### The Link Hierarchy

Links in a humanoid robot form a tree structure, with the torso typically at the root. Here is how a simplified humanoid might be organized:

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

This hierarchy is not just organizational—it directly affects how the robot computes positions. When the torso moves, everything attached to it moves too. When the shoulder rotates, the entire arm rotates with it [3].

---

## Joints: The Connections That Enable Movement

Links alone would just be a pile of disconnected parts. **Joints** are what connect links together and define how they can move relative to each other.

### Joint Types

URDF supports several types of joints, each allowing different kinds of motion:

**Revolute Joints**: These rotate around a single axis, like a door hinge. Most joints in a humanoid robot are revolute: shoulders, elbows, hips, knees, and ankles. Revolute joints have limits—a knee might bend from 0 to 140 degrees but no further.

**Fixed Joints**: These create rigid connections with no movement. A camera bolted to the head uses a fixed joint—it moves with the head but has no independent motion.

**Prismatic Joints**: These slide along a straight line, like a drawer. While uncommon in humanoids, some robots use prismatic joints for linear actuators or telescoping limbs.

**Continuous Joints**: These rotate without limits, like a wheel. Most humanoid joints are not continuous—you cannot rotate your elbow forever—but wheels and rotating sensors use this type.

### Humanoid Joint Mapping

Consider where different joint types appear in a humanoid:

| Body Part | Joint Type | Movement |
|-----------|------------|----------|
| Shoulder | Revolute | Raises and rotates arm |
| Elbow | Revolute | Bends forearm toward upper arm |
| Wrist | Revolute | Rotates hand |
| Hip | Revolute | Moves thigh forward, backward, sideways |
| Knee | Revolute | Bends shin toward thigh |
| Ankle | Revolute | Points and flexes foot |
| Camera Mount | Fixed | No movement relative to head |
| Head-Neck | Revolute | Turns and tilts head |

### Joint Properties

Beyond the type of motion, joints have important properties:

**Limits**: How far can the joint move? A human knee bends about 135 degrees; a robot knee might have different limits.

**Friction**: How much resistance does the joint have? Some friction is desirable for stability.

**Damping**: How quickly does motion slow down? This affects how smoothly the robot moves.

These properties help simulation and control software behave realistically [4].

---

## Kinematic Chains: From Base to End-Effector

When a humanoid robot reaches for an object, it does not just move one joint—it coordinates an entire sequence of links and joints. This sequence is called a **kinematic chain**.

### What Is a Kinematic Chain?

A kinematic chain is the series of links and joints connecting a base (usually the torso or pelvis) to an end-effector (usually a hand or foot). Think of it like a chain of cause and effect: when one joint moves, it affects the position of everything downstream.

For the right arm of a humanoid:

```text
torso_link ──[shoulder_joint]──► upper_arm_link ──[elbow_joint]──► forearm_link ──[wrist_joint]──► hand_link
               (revolute)                           (revolute)                       (revolute)
```

The hand's position in space depends on:
1. Where the torso is
2. How the shoulder is rotated
3. How the elbow is bent
4. How the wrist is angled

Change any of these, and the hand ends up somewhere different.

### Forward Kinematics

Given the position of each joint in a kinematic chain, you can calculate where the end-effector is located. This is called **forward kinematics**. If you know the shoulder is at 30 degrees, the elbow at 90 degrees, and the wrist at 0 degrees, you can compute exactly where the fingertips are in 3D space.

Forward kinematics is conceptually simple: work your way along the chain, applying each joint's rotation or translation, until you reach the end [5].

### Why Kinematic Chains Matter for Humanoids

Humanoid robots have several kinematic chains operating simultaneously:

**Arm chains**: For reaching, grasping, and manipulating objects

**Leg chains**: For walking, standing, and maintaining balance

**Head chain**: For directing cameras and sensors

During walking, the leg kinematic chains are constantly in motion. The foot's position—which determines whether the robot can take a step without falling—depends on the hip, knee, and ankle positions. Balance controllers must track these chains in real-time to keep the robot upright [6].

---

## The Transform Tree: Where Everything Is

We have described links and joints, and how they form kinematic chains. But how does ROS 2 actually keep track of where everything is during operation? The answer is the **transform tree**, or **TF tree**.

### From Static to Dynamic

URDF describes the robot's structure—what connects to what, and how joints can move. But URDF itself is static. It does not know that the robot's left knee is currently bent at 45 degrees.

The TF tree is the dynamic counterpart. It tracks the actual position and orientation of every link in real-time, updated as joints move. Think of URDF as the architectural blueprints and TF as the GPS tracking where everyone in the building currently is [7].

### Coordinate Frames

Every link in the robot has a **coordinate frame**—a local X, Y, Z axis system attached to that link. The TF tree describes how these frames relate to each other.

For example:
- The camera frame is attached to the camera link
- The camera link is attached to the head link
- The head link is attached to the torso link

If you know an object's position in the camera frame (from image processing), the TF tree can transform that position into the torso frame, then into the world frame. This lets the robot answer questions like: "The camera sees an object 2 meters ahead—where is that object relative to my feet?"

### Visualizing the TF Tree

A humanoid's TF tree reflects its link hierarchy:

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

As the robot moves, every frame in this tree updates. The TF system handles these updates continuously, allowing any node in the ROS 2 system to query spatial relationships [8].

---

## Sensors and Their Frames

Sensors are how a robot perceives the world, and their positions matter enormously. A camera mounted on the head sees a different view than one mounted on the chest. An IMU (Inertial Measurement Unit) reports orientation relative to its own mounting, not necessarily relative to the robot's body.

### Attaching Sensors to Links

In URDF, sensors are attached to links using fixed joints. A camera might be attached to the head link with a fixed joint that positions it 5 centimeters forward and 2 centimeters up from the head's center.

This attachment creates a **sensor frame**—a coordinate system for that sensor. When the camera reports that an object is "1 meter in front," that measurement is relative to the camera frame. The TF tree allows this to be transformed into any other frame [9].

### Common Sensor Frames

A humanoid might have:

**Camera frames**: For each RGB or depth camera, positioned where the camera looks

**IMU frame**: For the inertial sensor, oriented according to its mounting

**LiDAR frame**: For laser scanners, showing the origin of scan measurements

**Force sensor frames**: In the wrists or feet, measuring contact forces

### Connecting to ROS 2

Remember from Chapter 2 that sensors publish data to topics. A camera publishes images to `/camera/image`. But that image data is only meaningful if you know where the camera is—and that is what the sensor frame provides.

The camera node publishes images and also broadcasts the camera frame to the TF tree. Any node that subscribes to the images can also look up the camera's position, allowing it to interpret the images in a global context [10].

---

## URDF and SDF: Two Description Formats

You may encounter another format called **SDF** (Simulation Description Format). Understanding the difference helps clarify when to use each.

### URDF: Robot-Centric

URDF focuses on describing a single robot:
- Links and joints
- Physical properties (mass, inertia)
- Visual appearance
- Collision geometry
- Sensor attachments

URDF is what ROS 2 natively understands. When you load a robot into RViz (the ROS visualization tool), you provide a URDF [11].

### SDF: World-Centric

SDF describes entire simulation environments:
- Multiple robots
- Terrain and obstacles
- Lighting conditions
- Physics engine parameters
- Environmental sensors (like ceiling-mounted cameras)

SDF is the native format for Gazebo, the physics simulator often used with ROS 2. A Gazebo world file might include three robots, a room with furniture, and realistic lighting—none of which URDF can describe [12].

### When to Use Each

**Use URDF when**: You need to describe your robot for ROS 2 tools, visualize the robot model, or perform robot-state tracking.

**Use SDF when**: You need to simulate the robot in a realistic environment with physics, terrain, and multiple objects.

In practice, many ROS 2 projects use both: URDF for the robot model, converted to SDF (or embedded in SDF) when running Gazebo simulations. Module 2 will explore this workflow in detail.

---

## Try With AI

Now it is time to test your understanding. Use your preferred AI assistant to work through this kinematic chain tracing exercise.

**Prompt to use:**

```
I'm learning about URDF and kinematic chains. Help me trace through
the kinematic chain for a humanoid robot's left leg.

Starting from the torso (base), identify:
1. Each link in the chain (name and function)
2. Each joint connecting the links (type and motion)
3. How many degrees of freedom the leg has total

Then, explain what happens to the foot's position if:
- The hip joint rotates forward 30 degrees
- The knee joint bends 45 degrees
- The ankle joint tilts down 10 degrees

Finally, create a similar exercise for me to try with the right arm.
```

**What to look for:**
- Links should follow a logical progression (thigh, shin, foot)
- Joints should mostly be revolute (rotating)
- The total degrees of freedom depends on how many moving joints exist
- Position changes should cascade—hip movement affects everything below it

Compare your AI's answers with what you learned in this chapter. If the explanations do not match, ask follow-up questions to understand the differences.

---

## References

[1] Open Robotics, "URDF - Unified Robot Description Format," ROS 2 Documentation, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html

[2] Open Robotics, "Building a Visual Robot Model from Scratch," ROS 2 Documentation, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-with-URDF-from-Scratch.html

[3] D. V. Lu, "URDF XML Specification," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML

[4] Open Robotics, "URDF Joint Element," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML/joint

[5] B. Siciliano, L. Sciavicco, L. Villani, and G. Oriolo, Robotics: Modelling, Planning and Control. London, UK: Springer, 2009, pp. 39-100.

[6] J. J. Craig, Introduction to Robotics: Mechanics and Control, 4th ed. London, UK: Pearson, 2018, ch. 3.

[7] Open Robotics, "tf2 - ROS 2 Documentation," docs.ros.org, 2024. [Online]. Available: https://docs.ros.org/en/humble/Concepts/Intermediate/About-Tf2.html

[8] Open Robotics, "Introduction to tf2," ROS 2 Tutorials, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html

[9] REP 103, "Standard Units of Measure and Coordinate Conventions," ROS Enhancement Proposals, 2010. [Online]. Available: https://www.ros.org/reps/rep-0103.html

[10] REP 105, "Coordinate Frames for Mobile Platforms," ROS Enhancement Proposals, 2010. [Online]. Available: https://www.ros.org/reps/rep-0105.html

[11] Open Robotics, "URDF Link Element," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML/link

[12] Open Source Robotics Foundation, "SDFormat Specification," sdformat.org, 2024. [Online]. Available: http://sdformat.org/spec

