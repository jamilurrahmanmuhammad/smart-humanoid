---
title: "Chapter 2: ROS 2 Architecture & the Conceptual Model of Robot Control"
sidebar_position: 5
safety: none
prerequisites:
  - understanding of embodied intelligence concepts (from Chapter 1)
personaDifficulty: advanced
learningPath: engineer
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

Industrial robotics engineers understand the constraints of real-time systems. A single-threaded control loop running at 1 kHz cannot simultaneously process megapixel camera feeds, run neural network inference, coordinate multi-axis motion, and handle network communications. The computational demands conflict with timing guarantees.

Consider Tesla's Optimus humanoid: 40 electromechanical actuators requiring coordinated torque control at kilohertz rates, combined with vision processing for object manipulation, speech recognition for human interaction, and high-level task planning [20]. The computational architecture cannot be monolithic.

Similarly, Figure AI's humanoid robots deployed in BMW manufacturing facilities operate with 40+ degrees of freedom while integrating OpenAI language models for instruction following [21]. The perception, planning, and control pipelines run on different computational substrates with different timing requirements.

The fundamental challenge is **heterogeneous timing constraints**:

| Subsystem | Update Rate | Latency Tolerance |
|-----------|-------------|-------------------|
| Motor current control | 10 kHz | Sub-100 microseconds |
| Joint position control | 1 kHz | Sub-1 millisecond |
| Balance/stability | 200-500 Hz | 2-5 milliseconds |
| Trajectory planning | 10-100 Hz | 10-100 milliseconds |
| Perception (vision) | 30-60 Hz | 33-100 milliseconds |
| Task planning (LLM) | 0.1-1 Hz | 1-10 seconds |

No single process can satisfy these conflicting requirements. A 1 kHz control loop cannot block for neural network inference. An LLM generating a task plan cannot monopolize the CPU while balance control falters.

The solution is **distributed architecture**: independent processes with dedicated computational resources, communicating through standardized middleware. ROS 2 provides this middleware infrastructure.

---

## ROS 2: The Robotic Nervous System

ROS 2 (Robot Operating System 2) is middleware—a software layer between the operating system and application processes that provides communication, discovery, and lifecycle management services [1]. The "Operating System" in the name is a historical artifact; ROS 2 runs atop Linux, Windows, or real-time operating systems like VxWorks or QNX.

The **nervous system metaphor** provides a useful mental model for ROS 2's architecture:

| Nervous System Component | ROS 2 Equivalent | Technical Function |
|-------------------------|------------------|-------------------|
| Neuron clusters | **Nodes** | Independent processes with defined computational responsibility |
| Axon signaling | **Topics** | Asynchronous publish-subscribe data distribution |
| Reflex arcs | **Services** | Synchronous request-response RPC |
| Goal-directed behavior | **Actions** | Asynchronous goal-feedback-result state machines |
| Vascular transport | **DDS** | Wire protocol for discovery, serialization, and transport |

This metaphor scales from simple sensor-actuator loops to complex cognitive architectures. A reflex (service call) bypasses higher processing for speed. Goal-directed behavior (action) maintains state through execution. Continuous sensory streams (topics) flow to multiple processing centers simultaneously.

---

## Nodes: Process Isolation and Single Responsibility

In industrial automation, distributed control systems (DCS) partition functionality across dedicated controllers: a PLC handles discrete I/O, a motion controller manages servo axes, a vision system processes images. Each controller runs specialized firmware optimized for its domain.

ROS 2 **nodes** apply this principle at the software level. A node is an OS process (or intraprocess composition) that:

- Encapsulates a single functional responsibility
- Manages its own lifecycle (unconfigured → inactive → active → finalized)
- Declares explicit interfaces (publishers, subscribers, services, action servers)
- Can be deployed, monitored, and replaced independently

Consider the node decomposition for a humanoid manipulation task:

| Node | Responsibility | Execution Context |
|------|----------------|-------------------|
| `joint_state_broadcaster` | Publish joint encoder feedback | Real-time, 1 kHz |
| `forward_kinematics` | Compute end-effector pose from joint states | Real-time, 1 kHz |
| `collision_checker` | Validate configurations against environment | Non-RT, 100 Hz |
| `motion_planner` | Generate collision-free trajectories | Non-RT, on-demand |
| `trajectory_controller` | Execute trajectories with feedback | Real-time, 1 kHz |
| `gripper_controller` | Manage grasp force and position | Real-time, 500 Hz |
| `object_detector` | Identify objects from camera feeds | GPU-accelerated, 30 Hz |
| `pose_estimator` | Estimate 6-DoF object poses | GPU-accelerated, 30 Hz |
| `task_executor` | Coordinate pick-and-place sequences | Non-RT, event-driven |

This decomposition enables:

- **Isolation**: A crash in motion planning does not halt joint control
- **Optimization**: Real-time nodes run on isolated CPU cores; GPU nodes share accelerator access
- **Replaceability**: Swap MoveIt2 for a custom planner without modifying controllers
- **Scalability**: Distribute nodes across multiple machines for compute-intensive workloads

The ros2_control framework enforces this separation, distinguishing **hardware interfaces** (direct actuator access), **controllers** (feedback loops), and **broadcasters** (state publication) as separate node types with defined contracts [29].

---

## Topics: Asynchronous Publish-Subscribe Data Distribution

Industrial fieldbus protocols (EtherCAT, PROFINET, EtherNet/IP) provide deterministic cyclic data exchange between controllers and I/O modules. ROS 2 **topics** extend this concept to arbitrary data types with configurable reliability semantics.

A topic is a named communication channel with:

- **Message type**: Strongly-typed serialized data structure (e.g., `sensor_msgs/msg/Image`)
- **Publish semantics**: Any node can publish; no coordination required
- **Subscribe semantics**: Any node can subscribe; receives all published messages
- **QoS policies**: Configurable reliability, durability, history, and deadline parameters

The publish-subscribe pattern decouples producers from consumers:

```text
┌─────────────────────────────────────────────────────────────────┐
│                TOPIC: /camera/depth/points                       │
└─────────────────────────────────────────────────────────────────┘

   Publishers                              Subscribers
┌──────────────┐                        ┌──────────────┐
│ RealSense    │                        │ SLAM Node    │
│ Driver Node  │──────────┬────────────►│ (Mapping)    │
└──────────────┘          │             └──────────────┘
                          │             ┌──────────────┐
                          ├────────────►│ Obstacle     │
                          │             │ Detection    │
                          │             └──────────────┘
                          │             ┌──────────────┐
                          └────────────►│ Point Cloud  │
                                        │ Recorder     │
                                        └──────────────┘
```

Critical characteristics for industrial applications:

**Late-joiner support**: Subscribers receive messages regardless of when they start, subject to history depth settings.

**Multi-publisher composition**: Multiple sensors can publish to the same topic type (e.g., `/scan` from multiple LiDARs).

**Bandwidth management**: Large messages (images, point clouds) use zero-copy transport within a process and shared memory between processes on the same host.

**Deadline enforcement**: QoS policies can trigger callbacks when expected messages fail to arrive within specified intervals.

---

## Services: Synchronous Request-Response RPC

While topics handle continuous data flow, many robot operations require transactional semantics: query the current state, execute a discrete operation, return a result. ROS 2 **services** provide synchronous remote procedure calls (RPC).

A service defines:

- **Request message**: Input parameters for the operation
- **Response message**: Output results
- **Server**: Node providing the service implementation
- **Client**: Node invoking the service

Industrial use cases:

| Service | Request | Response | Application |
|---------|---------|----------|-------------|
| `/compute_ik` | Target pose, seed state | Joint configuration | Motion planning |
| `/get_planning_scene` | Components filter | Collision world state | Safety verification |
| `/trigger_snapshot` | (empty) | Image, timestamp | Quality inspection |
| `/set_io` | Channel, state | Previous state | Discrete I/O control |
| `/load_program` | Program ID | Success, message | Task switching |

Service calls block the caller until response arrives. This blocking behavior is appropriate for:

- **State queries**: Reading current values without continuous subscription overhead
- **Configuration changes**: Updating parameters with acknowledgment
- **Computations**: Offloading calculations (IK, path validation) to specialized nodes

Service calls are **not** appropriate for:

- Long-running operations (use actions instead)
- High-frequency queries (use topics with state publishing)
- Time-critical paths (blocking is incompatible with deterministic timing)

---

## Actions: Asynchronous Goal-Feedback-Result State Machines

Complex robot behaviors—navigation, manipulation, assembly—require sustained execution with progress monitoring and cancellation capability. ROS 2 **actions** implement a standardized state machine for goal-oriented tasks.

An action comprises:

- **Goal**: Parameterized objective (destination pose, object to grasp)
- **Feedback**: Periodic progress updates during execution
- **Result**: Final outcome upon completion or cancellation
- **Status**: Current execution state (pending, executing, succeeded, canceled, aborted)

The action protocol:

```text
┌──────────────────────────────────────────────────────────────────┐
│                    ACTION STATE MACHINE                           │
└──────────────────────────────────────────────────────────────────┘

    Client                                              Server
       │                                                   │
       │────── send_goal(target_pose) ────────────────────►│
       │◄───── goal_response(accepted/rejected) ───────────│
       │                                                   │
       │◄───── feedback(progress: 25%) ────────────────────│
       │◄───── feedback(progress: 50%) ────────────────────│
       │                                                   │
       │────── cancel_goal() ─────────────────────────────►│ (optional)
       │◄───── cancel_response(canceling) ─────────────────│
       │                                                   │
       │◄───── result(status: canceled, final_pose) ───────│
       │                                                   │
```

Industrial applications:

| Action | Goal | Feedback | Result |
|--------|------|----------|--------|
| `FollowJointTrajectory` | Waypoint sequence | Current position, error | Final position, error code |
| `NavigateToPose` | Target coordinate | Distance remaining, path | Success/failure, actual pose |
| `GripObject` | Object ID, grasp type | Force applied, slip detected | Grasp success, contact points |
| `ExecuteTask` | Task specification | Current step, progress % | Completion status, execution log |

Actions are essential for:

- **Supervisory control**: Higher-level nodes commanding lower-level behaviors
- **Human-robot interaction**: Commands that humans expect to monitor and interrupt
- **Recovery behaviors**: Long-running diagnostics or calibration sequences

---

## Distributed Computing in Humanoid Robots

Humanoid robots exemplify the need for distributed, heterogeneous computation. Consider the architectural requirements for a production humanoid like Unitree's G1 [22]:

**Sensor Processing Pipeline:**

- 3D LiDAR: Point cloud preprocessing, ground plane extraction (200 Hz)
- Stereo cameras: Depth computation, visual odometry (60 Hz)
- IMU array: State estimation, sensor fusion (1000 Hz)
- Force/torque sensors: Contact detection, impedance control (2000 Hz)
- Joint encoders: Position/velocity feedback (10 kHz)

**Control Hierarchy:**

```text
┌─────────────────────────────────────────────────────────────────┐
│                   HUMANOID CONTROL HIERARCHY                     │
└─────────────────────────────────────────────────────────────────┘

         ┌─────────────────────────────────────┐
         │        Task Planning Layer          │  (0.1-1 Hz)
         │   LLM-based instruction parsing     │
         │   Behavior tree execution           │
         └──────────────────┬──────────────────┘
                            │ Skill commands
                            ▼
         ┌─────────────────────────────────────┐
         │       Motion Planning Layer         │  (10-100 Hz)
         │   Whole-body trajectory generation  │
         │   Collision avoidance               │
         │   Footstep planning                 │
         └──────────────────┬──────────────────┘
                            │ Reference trajectories
                            ▼
         ┌─────────────────────────────────────┐
         │       Stabilization Layer           │  (200-500 Hz)
         │   Balance control (ZMP/DCM)         │
         │   Contact force distribution        │
         │   Compliance adaptation             │
         └──────────────────┬──────────────────┘
                            │ Joint torque/position commands
                            ▼
         ┌─────────────────────────────────────┐
         │       Servo Control Layer           │  (1-10 kHz)
         │   Current/torque loops              │
         │   Position/velocity loops           │
         │   Motor driver communication        │
         └─────────────────────────────────────┘
```

**Multi-sensor Fusion Requirements:**

Balance control requires fusing:
- IMU orientation (high frequency, drift-prone)
- Joint encoder positions (high frequency, accurate)
- Foot force sensors (contact timing, load distribution)
- Visual odometry (drift correction, low frequency)

Each sensor stream runs on its optimal hardware (IMU on MCU, vision on GPU) with its native timing, yet the fusion algorithm must synthesize a coherent state estimate.

ROS 2's distributed architecture enables:

1. **Hardware-matched deployment**: GPU nodes on NVIDIA Jetson, real-time nodes on dedicated cores, MCU nodes via micro-ROS
2. **Independent development**: Perception team iterates on vision pipeline while control team refines balance algorithm
3. **Fault isolation**: Vision node crash does not halt motor control
4. **Performance scaling**: Add compute nodes for demanding perception tasks without redesigning control architecture

---

## DDS: The Communication Backbone

ROS 2's middleware layer is built on **DDS** (Data Distribution Service), an OMG standard originally developed for mission-critical systems: defense, air traffic control, financial trading [4][5].

DDS provides:

**Discovery Protocol (SPDP/SEDP):**
Nodes automatically discover each other without central broker. Participants announce their presence and capabilities; the discovery protocol matches publishers to subscribers.

**Wire Protocol (RTPS):**
Real-Time Publish-Subscribe protocol defines message serialization, fragmentation, and transport. Supports UDP multicast, unicast, TCP, and shared memory.

**Quality of Service Policies:**

| Policy | Purpose | Trade-off |
|--------|---------|-----------|
| Reliability | RELIABLE vs BEST_EFFORT | Latency vs guaranteed delivery |
| Durability | TRANSIENT_LOCAL vs VOLATILE | Late-joiner data vs memory |
| History | KEEP_LAST(N) vs KEEP_ALL | Memory vs completeness |
| Deadline | Expected arrival interval | Responsiveness monitoring |
| Liveliness | Publisher health detection | Connection monitoring |

For industrial robotics, key DDS benefits include:

**Deterministic behavior**: Combined with real-time OS and priority configuration, DDS enables bounded latency communication.

**Security**: DDS-Security specification provides authentication, encryption, and access control—essential for robots in enterprise environments.

**Interoperability**: Multiple DDS implementations (CycloneDDS, FastDDS, RTI Connext) interoperate at the wire level, avoiding vendor lock-in.

**Scalability**: DDS efficiently handles hundreds of nodes and thousands of topics through hierarchical discovery and multicast optimization.

---

## Why ROS 2 Instead of ROS 1?

The transition from ROS 1 to ROS 2 addresses fundamental architectural limitations that blocked industrial adoption [7][8]:

| Requirement | ROS 1 Limitation | ROS 2 Solution |
|-------------|------------------|----------------|
| **Real-time** | Non-deterministic callbacks | Executor model with priority support |
| **Reliability** | TCP-only, no QoS | DDS with configurable policies |
| **Security** | None | DDS-Security (SROS2) |
| **Multi-robot** | Single rosmaster | Decentralized discovery |
| **Embedded** | Linux-only, heavyweight | micro-ROS on MCUs |
| **Lifecycle** | No standard state machine | Managed node lifecycle |
| **Parameters** | Global server, no typing | Node-local, strongly typed |
| **Actions** | Custom implementation | Standardized protocol |

For humanoid robotics specifically:

**Real-time control**: ROS 2's executor model allows priority-based callback scheduling when combined with RT-PREEMPT or Xenomai kernels. Critical control loops can preempt perception processing.

**Multi-machine coordination**: DDS handles network discovery and communication across computers without manual configuration. A humanoid's onboard compute (embedded) and offboard compute (workstation) integrate seamlessly.

**Lifecycle management**: Nodes transition through defined states (configure → activate → deactivate → shutdown), enabling coordinated startup/shutdown of complex systems.

**micro-ROS**: Embedded controllers (STM32, ESP32) run native ROS 2 nodes via micro-ROS, eliminating the rosserial translation layer and enabling direct DDS participation.

---

## Visualizing the Architecture

### Diagram 1: Humanoid as a Distributed System

```text
┌─────────────────────────────────────────────────────────────────┐
│            INDUSTRIAL HUMANOID - DISTRIBUTED ARCHITECTURE        │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │                    PERCEPTION CLUSTER                        │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
    │  │ Stereo Cam   │  │   LiDAR      │  │  RGB Cam     │       │
    │  │   Driver     │  │   Driver     │  │   Driver     │       │
    │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
    │         │/camera/stereo   │/scan           │/camera/rgb     │
    │         ▼                 ▼                ▼                │
    │  ┌──────────────────────────────────────────────────┐       │
    │  │              PERCEPTION FUSION                    │       │
    │  │   Object Detection │ Pose Estimation │ SLAM       │       │
    │  └──────────────────────────┬───────────────────────┘       │
    │                             │ /world_model                  │
    └─────────────────────────────┼───────────────────────────────┘
                                  ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    PLANNING CLUSTER                          │
    │  ┌──────────────────────────────────────────────────┐       │
    │  │              TASK PLANNER                         │       │
    │  │   Behavior Trees │ LLM Integration │ Skill Library│       │
    │  └──────────────────────────┬───────────────────────┘       │
    │                             │ /motion_goal (Action)         │
    │  ┌──────────────────────────▼───────────────────────┐       │
    │  │              MOTION PLANNER                       │       │
    │  │   Whole-body IK │ Trajectory Optimization        │       │
    │  └──────────────────────────┬───────────────────────┘       │
    │                             │ /joint_trajectory             │
    └─────────────────────────────┼───────────────────────────────┘
                                  ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    CONTROL CLUSTER (Real-Time)               │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
    │  │  Balance     │  │ Trajectory   │  │   Gripper    │       │
    │  │ Controller   │  │ Controller   │  │ Controller   │       │
    │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
    │         │                 │                 │               │
    │         └────────┬────────┴────────┬────────┘               │
    │                  │ /joint_commands │                        │
    │                  ▼                 ▼                        │
    │  ┌──────────────────────────────────────────────────┐       │
    │  │           HARDWARE INTERFACE (EtherCAT)           │       │
    │  │   40+ Servo Drives │ Force/Torque Sensors        │       │
    │  └──────────────────────────────────────────────────┘       │
    └─────────────────────────────────────────────────────────────┘
```

### Diagram 2: ROS 2 Communication Patterns (Industrial Context)

```text
┌─────────────────────────────────────────────────────────────────┐
│           COMMUNICATION PATTERNS - INDUSTRIAL SEMANTICS          │
└─────────────────────────────────────────────────────────────────┘

    TOPICS - Cyclic Data Exchange (cf. EtherCAT PDO)
    ─────────────────────────────────────────────────
    ┌──────────────┐                    ┌──────────────┐
    │ Joint State  │── /joint_states ──►│ Controller   │
    │ Broadcaster  │       │            │   Manager    │
    │   (1 kHz)    │       │            │              │
    └──────────────┘       │            └──────────────┘
                           │            ┌──────────────┐
                           └───────────►│  Telemetry   │
                                        │   Logging    │
                                        └──────────────┘

    SERVICES - Acyclic Commands (cf. EtherCAT SDO)
    ─────────────────────────────────────────────────
    ┌──────────────┐  /switch_controller  ┌──────────────┐
    │    Task      │ ────────────────────►│ Controller   │
    │  Executor    │ ◄────────────────────│   Manager    │
    └──────────────┘    success/failure   └──────────────┘

    ACTIONS - Supervised Motion (cf. PLC Function Blocks)
    ─────────────────────────────────────────────────
    ┌──────────────┐                      ┌──────────────┐
    │   Motion     │── FollowJointTraj ──►│ Trajectory   │
    │   Planner    │       (Goal)         │ Controller   │
    │              │◄──── Feedback ───────│              │
    │              │◄──── Result ─────────│              │
    └──────────────┘                      └──────────────┘
```

### Diagram 3: Sensor-Perception-Control Loop (Industrial Timing)

```text
┌─────────────────────────────────────────────────────────────────┐
│              REAL-TIME CONTROL ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────────┘

    Non-Real-Time Domain              Real-Time Domain
    (Linux user space)                (RT kernel / FPGA)
           │                                   │
    ┌──────┴──────┐                    ┌───────┴───────┐
    │             │                    │               │
    │  PERCEPTION │     /world_model   │   CONTROL     │
    │   PIPELINE  │ ─────────────────► │    LOOP       │
    │             │     (50 Hz)        │   (1 kHz)     │
    │  - SLAM     │                    │               │
    │  - Detection│     /joint_cmd     │  - Balance    │
    │  - Planning │ ─────────────────► │  - Tracking   │
    │             │     (100 Hz)       │  - Impedance  │
    │             │                    │               │
    └─────────────┘                    └───────┬───────┘
                                               │
                                       ┌───────▼───────┐
                                       │   HARDWARE    │
                                       │   INTERFACE   │
                                       │               │
                                       │  EtherCAT Bus │
                                       │  (sub-ms)     │
                                       └───────────────┘

    Timing Budget:
    ├── Perception: 20ms (50 Hz) - acceptable for navigation
    ├── Planning: 10ms (100 Hz) - trajectory updates
    ├── Control: 1ms (1 kHz) - feedback loops
    └── Hardware: 0.1ms (10 kHz) - current loops on drives
```

---

## Try With AI

Apply your understanding to a realistic industrial scenario. Use this prompt with your AI assistant:

**Prompt:**

```
I'm architecting a ROS 2 system for a humanoid robot performing warehouse
order fulfillment. The robot must:

1. Navigate autonomously between picking stations
2. Identify and localize target items using vision
3. Execute pick-and-place with a dual-arm configuration
4. Handle dynamic obstacles (humans, forklifts)
5. Report task status to a fleet management system

Design the ROS 2 architecture:
1. List the nodes required, specifying which need real-time execution
2. Define the topics for sensor data flow (specify message types)
3. Define services for system queries and configuration
4. Define actions for the primary robot behaviors
5. Identify which nodes should run on which compute platforms
   (embedded MCU, edge GPU, central server)

For each communication channel, specify whether it needs:
- RELIABLE or BEST_EFFORT QoS
- Approximate message frequency
- Latency requirements

Then analyze: What happens if the vision node crashes mid-task?
How should the system handle this gracefully?
```

**Evaluation criteria:**

- Does the architecture separate real-time control from perception/planning?
- Are QoS policies appropriate for each communication type?
- Is there a clear failure recovery strategy?
- Would this architecture scale to multiple robots?

Challenge the AI's response by asking about edge cases: sensor failures, network partitions, compute overload scenarios.

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

[20] Tesla, Inc., "Tesla Optimus: General Purpose Humanoid Robot," tesla.com, 2024. [Online]. Available: https://www.tesla.com/en/optimus

[21] Figure AI, Inc., "Figure 01 and Figure 02 Humanoid Robots," figure.ai, 2024. [Online]. Available: https://www.figure.ai/

[22] Unitree Robotics, "Unitree G1 Humanoid Agent," unitree.com, 2024. [Online]. Available: https://www.unitree.com/g1/

[29] ros2_control maintainers, "ros2_control Documentation," control.ros.org, 2024. [Online]. Available: https://control.ros.org/
