---
title: "Chapter 2: ROS 2 Architecture & the Conceptual Model of Robot Control"
sidebar_position: 5
safety: none
prerequisites:
  - understanding of embodied intelligence concepts (from Chapter 1)
personaDifficulty: beginner
learningPath: explorer
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

# Chapter 2: ROS 2 Architecture & the Conceptual Model of Robot Control

## Learning Objectives

By the end of this chapter, you will be able to:

1. Describe the purpose of ROS 2 in a robotic system
2. Understand how ROS 2 enables distributed, real-time coordination
3. Explain nodes, topics, services, and actions conceptually (without code)
4. Understand the role of DDS (Data Distribution Service) at a conceptual level
5. Visualize a humanoid robot as a network of communicating processes
6. Explain why ROS 2 replaced ROS 1 for complex robotics applications

---

## Why Can't a Robot Run on One AI Model?

Imagine you are building a software application. You might start with a single program that handles everything: the user interface, business logic, database access, and background tasks. This works fine for simple applications, but as complexity grows, this monolithic approach becomes unmanageable. The solution? Break it into microservices—independent programs that communicate through well-defined interfaces.

Now imagine a humanoid robot. It must simultaneously:
- Process camera images to recognize objects and people
- Read force sensors in its fingers to grasp objects without crushing them
- Monitor gyroscopes and accelerometers to maintain balance
- Plan arm movements to reach for a cup
- Control 40+ motors to execute those movements smoothly
- Listen for voice commands and respond appropriately

Could a single AI model handle all of this? Consider what happens when the robot tries to pick up a cup. The vision system needs to update at 30 frames per second to track the cup's position. The balance controller needs to run at 1000 Hz to prevent falling. The motor controllers need to adjust torque hundreds of times per second. A single program trying to do all of this would be impossibly complex and would fail to meet these different timing requirements.

This is why robots need a **distributed architecture**—dozens of specialized processes running simultaneously, each handling one aspect of the robot's operation, communicating through a shared infrastructure. This infrastructure is what ROS 2 provides.

---

## ROS 2: The Robotic Nervous System

ROS 2 (Robot Operating System 2) is often misunderstood because of its name. Despite being called an "operating system," ROS 2 is actually **middleware**—software that sits between the operating system (like Linux) and your robot applications, enabling them to communicate with each other [1].

Think of ROS 2 as a robot's nervous system. Just as your nervous system allows your brain, eyes, muscles, and skin to work together seamlessly, ROS 2 enables a robot's cameras, sensors, processors, and motors to coordinate their actions.

This nervous system metaphor helps explain ROS 2's core concepts:

| Human Nervous System | ROS 2 Equivalent | Function |
|---------------------|------------------|----------|
| Clusters of neurons | **Nodes** | Independent processing units with specific responsibilities |
| Neural signals | **Topics** | Continuous streams of information flowing between nodes |
| Reflex pathways | **Services** | Quick request-response interactions |
| Goal-driven behaviors | **Actions** | Long-running tasks with progress feedback |
| Bloodstream carrying signals | **DDS** | The transport layer that delivers all communications |

Let us explore each of these concepts in detail.

---

## Nodes: The Building Blocks

In software development, you are familiar with the concept of microservices—small, independent applications that each handle a specific function. ROS 2 **nodes** are the robotics equivalent.

A node is an independent process that performs a single, well-defined task. In a humanoid robot, you might have:

- A **camera node** that captures and publishes images
- A **perception node** that processes images to detect objects
- A **planning node** that decides how to move the arm
- A **control node** that sends commands to motors
- An **IMU node** that reads orientation data from sensors
- A **balance node** that keeps the robot from falling over

Each node runs independently. If the camera node crashes, the balance node keeps working. If you need to upgrade the perception algorithm, you only modify that node—the rest of the system continues unchanged.

This modularity is why the nervous system metaphor works so well. Just as neurons specialize for specific functions (some process vision, others control movement), nodes specialize for specific robot tasks. And just as neurons communicate through synapses, nodes communicate through ROS 2's messaging system.

---

## Topics: Continuous Data Streams

When neurons fire, they send electrical signals to other neurons. This happens continuously—your eyes are constantly sending visual information to your brain, even when you are not consciously paying attention.

In ROS 2, **topics** serve this purpose. A topic is a named channel for continuous, one-way data flow using a **publish-subscribe** pattern.

Think of it like a radio station:
- The radio station (publisher) broadcasts music continuously
- Anyone with a radio tuned to that frequency (subscribers) receives the music
- The station does not know or care how many listeners there are
- Listeners can tune in or out at any time

In a robot:
- The camera node **publishes** images to a topic called `/camera/image`
- Any node that needs camera data **subscribes** to that topic
- The perception node subscribes to process objects
- A logging node might also subscribe to record video
- The camera does not know or care who is listening

This decoupling is powerful. You can add new subscribers without modifying the publisher. You can replace one subscriber with another without affecting the system. The camera just keeps publishing; whoever wants the data can receive it.

Topics are perfect for sensor data that flows continuously: camera images, laser scans, joint positions, IMU readings. The data keeps coming whether anyone is listening or not.

---

## Services: Request-Response Interactions

Not all robot communication fits the continuous streaming model. Sometimes a node needs to ask a question and get an answer. This is like a reflex—a quick stimulus-response interaction.

ROS 2 **services** provide synchronous request-response communication. One node sends a request, waits for the response, and then continues.

Examples in a robot:
- "What is the robot's current position?" → Returns coordinates
- "Save the current map to disk" → Returns success/failure
- "Calculate inverse kinematics for this target pose" → Returns joint angles
- "Is the gripper currently holding something?" → Returns true/false

Services are like function calls across processes. The calling node blocks (waits) until the service responds. This makes services unsuitable for long-running operations—you would not want your robot frozen while waiting for a navigation task to complete.

Think of services as quick database queries or API calls in web development. You ask a question, get an answer, and move on. They are perfect for getting the current state of something or performing quick calculations.

---

## Actions: Long-Running Goals

What about tasks that take time? When you decide to walk across a room, your brain does not freeze until you arrive. You can monitor progress, adjust your path, or decide to stop early.

ROS 2 **actions** handle long-running, goal-oriented tasks. Unlike services, actions:
- Accept a goal from the client
- Provide regular feedback during execution
- Can be canceled mid-execution
- Report a final result when complete

Consider a humanoid robot walking to a destination:
1. A navigation node receives the goal: "Go to the kitchen"
2. While walking, it sends feedback: "2 meters traveled, 5 meters remaining"
3. If obstacles appear, it adjusts the path and continues sending updates
4. The requesting node can cancel: "Stop, I changed my mind"
5. Eventually, the robot reports: "Goal reached" or "Goal failed: path blocked"

Actions map perfectly to the "goal-driven behaviors" in our nervous system metaphor. When you reach for a cup, your brain sets a goal (grasp the cup), monitors progress (watching your hand approach), can adjust (if the cup moves), and eventually reports success or failure (cup grasped or dropped).

---

## Distributed Computing in Humanoid Robots

Now let us see how these concepts come together in a humanoid robot. Consider the challenge of balancing while walking—something humans do without thinking but that requires incredible coordination in a robot.

A walking humanoid needs:
- **Parallel perception**: Multiple sensors providing data simultaneously
  - Cameras tracking the environment
  - IMUs measuring body orientation
  - Force sensors in feet detecting ground contact
  - Joint encoders reporting limb positions

- **Real-time motor control**: Actuators responding within milliseconds
  - Leg joints adjusting to maintain balance
  - Arm joints compensating for weight shifts
  - Ankle motors correcting foot placement

- **Multi-sensor fusion**: Combining data from multiple sources
  - Integrating IMU and foot sensor data for balance estimation
  - Combining camera and LiDAR for obstacle detection
  - Merging joint feedback with commanded positions

This is why ROS 2's distributed architecture is essential. Each sensor has its own node publishing data. Each motor controller has its own node receiving commands. A central control node subscribes to all sensor data, makes decisions, and publishes commands to all motor nodes.

If any single process had to handle all of this, it would be impossibly complex and would fail to meet the timing requirements. The camera might need data at 30 Hz, the IMU at 200 Hz, and the balance controller at 1000 Hz. By distributing the work across nodes, each can run at its required frequency.

---

## DDS: The Communication Backbone

How do all these nodes communicate reliably? This is where **DDS** (Data Distribution Service) comes in—the "bloodstream" of our nervous system metaphor [4].

DDS is an industry standard for real-time data distribution, originally developed for mission-critical systems like air traffic control and naval combat systems. ROS 2 adopted DDS as its communication layer because it provides:

- **Reliability**: Messages can be guaranteed to arrive, even if the network is congested
- **Low latency**: Data moves quickly between nodes, essential for real-time control
- **Multi-process support**: Nodes can run as separate processes, even on different computers
- **Discovery**: Nodes automatically find each other without manual configuration
- **Quality of Service**: Different communication patterns for different needs

Think of DDS as the internet infrastructure for your robot. Just as TCP/IP handles the complexity of routing data across the internet, DDS handles the complexity of routing messages between robot nodes. You do not need to understand how packets travel through networks to build a website; similarly, you do not need to understand DDS internals to use ROS 2.

What matters is that DDS ensures your robot's "nervous system" can communicate reliably and quickly, whether nodes are running on the same computer or distributed across multiple machines.

---

## Why ROS 2 Instead of ROS 1?

You may encounter references to "ROS 1" (also called "ROS" or "ROS Noetic"). ROS 1 served the robotics community well for over a decade, but it had limitations that became critical as robots grew more complex [7][8]:

| Limitation | ROS 1 | ROS 2 |
|-----------|-------|-------|
| **Threading** | Single-threaded by default | Multi-threaded, concurrent execution |
| **Platforms** | Linux only | Linux, Windows, macOS |
| **Real-time** | No real-time guarantees | Designed for real-time control |
| **Security** | None built-in | Encryption and authentication |
| **Communication** | Custom TCP/UDP | Industry-standard DDS |
| **Lifecycle** | End of Life: May 2025 | Active development |

For humanoid robots, these improvements are essential:
- **Multi-threading** allows parallel sensor processing
- **Real-time support** enables precise motor control
- **Security** protects robots operating in public spaces
- **Cross-platform** support enables diverse hardware configurations

If you are starting robotics today, ROS 2 is the clear choice.

---

## Visualizing the Architecture

Let us bring everything together with diagrams showing how ROS 2 organizes robot communication.

### Diagram 1: Humanoid as a Distributed System

```text
┌─────────────────────────────────────────────────────────────────┐
│                    HUMANOID ROBOT ARCHITECTURE                   │
└─────────────────────────────────────────────────────────────────┘

        ┌──────────────┐
        │ Camera Node  │
        │   (Eyes)     │
        └──────┬───────┘
               │ /camera/image (Topic)
               ▼
        ┌──────────────┐
        │ Perception   │
        │   Node       │
        │  (Visual     │
        │   Cortex)    │
        └──────┬───────┘
               │ /detected_objects (Topic)
               ▼
        ┌──────────────┐
        │ Planning     │◄─── /navigate_to (Action Goal)
        │   Node       │
        │ (Prefrontal  │───► /navigation_feedback (Action Feedback)
        │   Cortex)    │
        └──────┬───────┘
               │ /trajectory (Topic)
               ▼
        ┌──────────────┐
        │ Control Node │
        │  (Motor      │
        │   Cortex)    │
        └──────┬───────┘
               │ /joint_commands (Topic)
               ▼
        ┌──────────────┐
        │   Motors     │
        │ (Muscles)    │
        └──────────────┘
```

### Diagram 2: ROS 2 Communication Patterns

```text
┌─────────────────────────────────────────────────────────────────┐
│                 ROS 2 COMMUNICATION PATTERNS                     │
└─────────────────────────────────────────────────────────────────┘

    TOPICS (Continuous Data Flow)
    ──────────────────────────────
    ┌──────────┐                    ┌──────────┐
    │ Camera   │ ───/image────────► │ Viewer   │
    │  Node    │        │           │   Node   │
    └──────────┘        │           └──────────┘
                        │           ┌──────────┐
                        └─────────► │ Recorder │
                                    │   Node   │
                                    └──────────┘

    SERVICES (Request-Response)
    ──────────────────────────────
    ┌──────────┐    Request     ┌──────────┐
    │ Planner  │ ─────────────► │   Map    │
    │   Node   │ ◄───────────── │  Server  │
    └──────────┘    Response    └──────────┘

    ACTIONS (Long-Running Tasks)
    ──────────────────────────────
    ┌──────────┐      Goal      ┌──────────┐
    │   User   │ ─────────────► │Navigation│
    │Interface │ ◄───Feedback── │  Server  │
    └──────────┘ ◄───Result──── └──────────┘
```

### Diagram 3: Sensor-Perception-Control Loop

```text
┌─────────────────────────────────────────────────────────────────┐
│               CONTINUOUS PERCEPTION-ACTION LOOP                  │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────┐     ┌───────────┐     ┌────────────┐
    │ Sensors │────►│Perception │────►│  Planning  │
    │         │     │           │     │            │
    │ Camera  │     │  Object   │     │   Path     │
    │  IMU    │     │ Detection │     │  Planning  │
    │  LiDAR  │     │  Mapping  │     │  Decision  │
    └─────────┘     └───────────┘     └─────┬──────┘
         ▲                                  │
         │                                  ▼
         │                            ┌────────────┐
         │                            │  Control   │
         │                            │            │
         │                            │   Motor    │
         │                            │  Commands  │
         │                            └─────┬──────┘
         │                                  │
         │         ┌───────────┐            │
         └─────────┤ Actuators │◄───────────┘
                   │           │
                   │  Motors   │
                   │  Grippers │
                   └───────────┘

    The loop runs continuously:
    Sense → Perceive → Plan → Control → Act → Sense...
```

---

## Try With AI

Now it is time to test your understanding. Use your preferred AI assistant to work through this scenario-matching exercise.

**Prompt to use:**

```
I'm learning about ROS 2 communication patterns. For each scenario below,
help me identify whether it should use a Topic, Service, or Action, and explain why.

Scenarios:
1. A camera continuously capturing 30 frames per second
2. Checking if the robot's battery level is above 20%
3. A robot arm moving to pick up an object (takes 5 seconds)
4. A LiDAR sensor scanning the environment 10 times per second
5. Saving the current map to a file
6. A robot navigating from the kitchen to the living room
7. An IMU reporting orientation data at 200 Hz
8. Calculating the inverse kinematics for a target position

After you explain each answer, give me two new scenarios to test myself.
```

**What to look for:**
- Topics: Continuous data streams, multiple subscribers possible
- Services: Quick request-response, blocking call
- Actions: Long-running tasks, progress feedback, can be canceled

Compare your AI's answers with what you learned in this chapter. If the explanations do not match, ask follow-up questions to understand the differences.

---

## References

[1] S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall, "Robot Operating System 2: Design, architecture, and uses in the wild," Science Robotics, vol. 7, no. 66, May 2022. [Online]. Available: https://www.science.org/doi/10.1126/scirobotics.abm6074

[2] Open Robotics, "ROS 2 Design," design.ros2.org, 2024. [Online]. Available: https://design.ros2.org/

[3] Open Robotics, "ROS 2 Documentation: Humble Hawksbill," docs.ros.org, 2024. [Online]. Available: https://docs.ros.org/en/humble/

[4] Object Management Group, "Data Distribution Service for Real-Time Systems, Version 1.4," OMG Document formal/2015-04-10, Apr. 2015. [Online]. Available: https://www.omg.org/spec/DDS/1.4/PDF

[5] Object Management Group, "DDS Interoperability Wire Protocol (DDSI-RTPS), Version 2.5," OMG Document formal/2022-04-01, Apr. 2022. [Online]. Available: https://www.omg.org/spec/DDSI-RTPS/2.5/About-DDSI-RTPS

[6] DDS Foundation, "What is DDS?," dds-foundation.org, 2024. [Online]. Available: https://www.dds-foundation.org/what-is-dds-3/

[7] Open Robotics, "Migrating from ROS 1 to ROS 2," docs.ros.org, 2024. [Online]. Available: https://docs.ros.org/en/humble/How-To-Guides/Migrating-from-ROS1.html

[8] Open Robotics, "Changes between ROS 1 and ROS 2," design.ros2.org, 2024. [Online]. Available: http://design.ros2.org/articles/changes.html
