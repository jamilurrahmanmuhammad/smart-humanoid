---
title: "Chapter 2: ROS 2 Architecture & the Conceptual Model of Robot Control"
sidebar_position: 6
safety: none
prerequisites:
  - understanding of embodied intelligence concepts (from Chapter 1)
personaDifficulty: intermediate
learningPath: builder
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

If you have built projects with Arduino or Raspberry Pi, you know the challenge of managing complexity. A simple LED blinker is straightforward—one program, one task. But what happens when you add a temperature sensor, a motor, an LCD display, and WiFi connectivity? Your single program becomes a tangled web of `if` statements, timing delays, and state variables that is difficult to debug and impossible to extend.

Professional embedded developers solve this with **task separation**—breaking the program into independent modules that communicate through well-defined interfaces. The motor controller does not care where its speed commands come from. The display module does not know what generated the data it shows. Each component focuses on its job.

Now scale this to a humanoid robot. Instead of a few peripherals, imagine:
- 6 cameras capturing video at 30 frames per second
- 20+ force/torque sensors in hands and feet
- Inertial measurement units tracking body orientation at 200 Hz
- 40+ motors requiring coordinated position commands
- Microphones processing voice commands
- Speakers providing audio feedback

Could your Arduino sketch handle all of this? Even a Raspberry Pi 5 would struggle to manage this many concurrent data streams with different timing requirements. The camera might need processing at 30 Hz, balance control at 1000 Hz, and voice recognition in real-time bursts. A single program cannot satisfy these conflicting requirements.

This is why serious robotics uses a **distributed architecture**—multiple processes, each handling one aspect of the robot, communicating through standardized middleware. ROS 2 provides this middleware infrastructure.

---

## ROS 2: The Robotic Nervous System

ROS 2 (Robot Operating System 2) is **middleware**, not an operating system. Do not let the name confuse you. ROS 2 runs on top of Linux (or Windows or macOS) and provides the communication infrastructure that lets robot components talk to each other [1].

Think about how you might connect multiple Arduinos to build a complex robot. You could use I2C, SPI, serial communication, or WiFi. Each has different trade-offs for speed, reliability, and complexity. Now imagine managing dozens of connections, each with different data types and timing requirements. The wiring and protocol management alone would be overwhelming.

ROS 2 solves this by providing a standardized way for robot components (called "nodes") to discover each other and exchange data. It handles the networking complexity so you can focus on robot functionality.

The **nervous system metaphor** helps explain how ROS 2 organizes communication:

| Human Nervous System | ROS 2 Equivalent | Maker Analogy |
|---------------------|------------------|---------------|
| Clusters of neurons | **Nodes** | Individual Arduino/RPi programs |
| Neural signals | **Topics** | Serial data streams between boards |
| Reflex pathways | **Services** | I2C request-response queries |
| Goal-driven behaviors | **Actions** | Long-running motor sequences |
| Bloodstream carrying signals | **DDS** | The network layer (WiFi/Ethernet) |

---

## Nodes: Independent Processing Units

If you have built multi-board Arduino projects, you understand the concept of distributed processing. One Arduino handles motor control, another manages sensors, a third handles the display. They communicate over serial or I2C, each running its own program.

ROS 2 **nodes** formalize this pattern. A node is an independent process that:
- Runs its own program loop
- Handles a specific responsibility
- Communicates with other nodes through ROS 2 messaging
- Can be started, stopped, or replaced independently

In a robot built with commodity hardware, nodes might run on:
- A Raspberry Pi handling camera processing
- An Arduino (through rosserial or micro-ROS) managing motor PWM signals
- A Jetson Nano running object detection
- A laptop providing the user interface

Each node handles one job:

| Node | Hardware | Responsibility |
|------|----------|----------------|
| Camera Driver | Raspberry Pi + USB camera | Publish image frames |
| Object Detector | Jetson Nano | Analyze images, publish detected objects |
| Motor Controller | Arduino Mega | Receive velocity commands, output PWM |
| IMU Reader | Arduino Nano + MPU6050 | Publish orientation data |
| Navigation | Laptop | Calculate paths, send motion commands |

The beauty is modularity. If you upgrade from an Arduino Mega to a Teensy for better motor control, you only change that node. If you swap your USB camera for an Intel RealSense, you modify the camera driver node. The rest of the system remains unchanged.

---

## Topics: Continuous Data Streams

When you connect an Arduino sensor to your laptop, you might use `Serial.println()` to stream data continuously. The laptop reads whatever arrives, whenever it arrives. This is the basic idea behind ROS 2 **topics**.

A topic is a named channel for continuous, one-directional data flow using the **publish-subscribe** pattern:

- **Publishers** send data to a topic (like `Serial.println()`)
- **Subscribers** receive data from a topic (like `Serial.read()`)
- Publishers and subscribers are decoupled—they do not know about each other

Think of it like a radio broadcast:
- The weather station (publisher) broadcasts updates on 98.7 FM (topic name)
- Anyone with a radio (subscriber) can tune in and receive updates
- The station does not know or care how many listeners exist
- New listeners can tune in anytime without affecting the broadcast

In a robot built with maker hardware:

```text
┌──────────────────┐         ┌──────────────────┐
│   Arduino Nano   │         │  Raspberry Pi    │
│   + MPU6050      │         │  (Subscriber)    │
│   (Publisher)    │         │                  │
│                  │         │  - Balance Calc  │
│  /imu/data ──────┼────────►│  - Data Logging  │
│                  │         │                  │
└──────────────────┘         └──────────────────┘
                                      │
                                      ▼
                             ┌──────────────────┐
                             │   Laptop         │
                             │   (Subscriber)   │
                             │                  │
                             │  - Visualization │
                             │  - Recording     │
                             └──────────────────┘
```

The Arduino publishes IMU data at 200 Hz. The Raspberry Pi subscribes to calculate balance. The laptop also subscribes to visualize the data. The Arduino does not know (or care) how many devices are receiving its data.

Topics excel at streaming sensor data: camera images, LiDAR scans, IMU readings, joint encoder positions, force sensor measurements. Any continuous data flow that multiple consumers might need belongs on a topic.

---

## Services: Request-Response Queries

Topics handle continuous data, but sometimes you need a one-time answer. When you query an I2C device for its current reading, you send a command and wait for a response. This synchronous request-response pattern is what ROS 2 **services** provide.

A service defines a specific question and answer format. One node offers the service; other nodes can call it and receive a response.

Examples from a maker robot:

| Service | Request | Response | Use Case |
|---------|---------|----------|----------|
| `/get_battery` | (none) | voltage: 11.2V | Dashboard display |
| `/save_map` | filename: "kitchen.yaml" | success: true | Map persistence |
| `/set_led` | color: "red" | previous: "green" | Status indication |
| `/calibrate_imu` | (none) | offset_x: 0.02, offset_y: -0.01 | Sensor setup |

The calling node **blocks** (waits) until the service responds. This is like calling a function—execution pauses until you get the return value.

```text
┌──────────────────┐                    ┌──────────────────┐
│   Main Control   │   "get_battery"   │  Power Monitor   │
│   (Client)       │ ─────────────────►│  Arduino         │
│                  │                    │  (Server)        │
│   [waiting...]   │◄───────────────── │                  │
│                  │   "11.2V"         │  - Reads ADC     │
│   [continues]    │                    │  - Returns value │
└──────────────────┘                    └──────────────────┘
```

Services are perfect for:
- Getting current state (battery level, joint positions, sensor calibration)
- Performing quick calculations (inverse kinematics, collision checks)
- Changing settings (LED color, motor enable/disable)
- One-time operations (save file, load configuration)

Do not use services for long-running operations—the caller is blocked waiting for a response.

---

## Actions: Long-Running Goals

What about tasks that take time? If you have programmed a robot arm to move through waypoints, you know the challenge. The motion takes several seconds, but you do not want your main program frozen during execution. You need:
- A way to start the motion
- Progress updates during execution
- The ability to cancel if needed
- Notification when complete

ROS 2 **actions** provide this pattern. An action represents a goal-oriented task that runs over time with continuous feedback.

Consider a robot arm controlled by Arduino servos:

```text
Timeline:  0s        1s        2s        3s        4s        5s
           │         │         │         │         │         │
Goal ──────┤ "Move to cup position"
           │
Feedback ──┼─────────┤ 20% ────┤ 45% ────┤ 78% ────┤ 95% ────┤
           │         │         │         │         │         │
Result ────┼─────────┼─────────┼─────────┼─────────┼─────────┤ Success!
           │         │         │         │         │         │

Optional:  Cancel ───┤ (at 2s, user changes mind)
                     │
           Result ───┼─── Canceled at 45%
```

The action pattern separates:
- **Goal**: What to achieve ("move arm to position X, Y, Z")
- **Feedback**: Progress updates (percentage complete, current position)
- **Result**: Final outcome (success, failure, or canceled)

This is perfect for:
- Robot navigation (go from point A to point B)
- Manipulation tasks (pick up object, place in bin)
- Scanning operations (rotate LiDAR 360 degrees)
- Homing sequences (find limit switches, zero encoders)

---

## Distributed Computing in Humanoid Robots

Now let us see how these patterns combine in a humanoid robot. Even a simple bipedal robot requires careful coordination of multiple subsystems.

Consider a hobby-level humanoid with these components:

**Sensor Array:**
- USB camera on Raspberry Pi
- MPU6050 IMU on Arduino Nano
- Force-sensitive resistors in feet on Arduino
- Joint encoders (potentiometers or hall sensors)

**Actuator Array:**
- 12 servo motors (2 per leg joint, 2 per arm)
- Controlled via PCA9685 PWM driver boards
- I2C communication from Raspberry Pi

**Processing:**
- Raspberry Pi 4 for high-level control
- Arduino Nano for real-time sensor reading
- Arduino Mega for motor PWM generation

Each subsystem becomes a ROS 2 node:

```text
┌─────────────────────────────────────────────────────────────────┐
│              HOBBY HUMANOID - NODE ARCHITECTURE                  │
└─────────────────────────────────────────────────────────────────┘

Raspberry Pi 4                     Arduino Nano              Arduino Mega
├── camera_node                    └── imu_node              └── motor_node
│   └─► /camera/image                 └─► /imu/data             ◄── /joint_cmd
├── balance_node
│   ◄── /imu/data                  Arduino (feet)
│   └─► /balance/correction        └── foot_sensor_node
├── gait_planner                      └─► /foot/pressure
│   ◄── /foot/pressure
│   └─► /joint_cmd
└── navigation_node
    └─► /navigate_to (Action)
```

The key insight: **each node runs at its optimal rate**. The IMU publishes at 200 Hz for accurate orientation tracking. The camera publishes at 30 Hz—fast enough for perception, slow enough to process. The motor controller expects commands at 50 Hz for smooth servo motion. ROS 2 handles the timing differences automatically.

---

## DDS: The Communication Backbone

How does data flow between an Arduino publishing IMU data and a Raspberry Pi running the balance algorithm? This is where **DDS** (Data Distribution Service) comes in [4].

DDS is the underlying transport layer that ROS 2 uses for all communication. Think of it as the "network stack" for your robot—like how WiFi handles the complexity of wireless communication, DDS handles the complexity of routing messages between nodes.

For makers, the key benefits are:

| Feature | What It Means |
|---------|---------------|
| **Auto-discovery** | Nodes find each other automatically on the network |
| **Reliability options** | Choose between "best effort" (fast) or "reliable" (guaranteed) |
| **Multi-host support** | Nodes can run on different computers |
| **Quality of Service** | Configure message queuing, delivery guarantees |

Practical example: You have a Raspberry Pi running navigation and an Arduino running motor control. They connect over USB serial (using micro-ROS). DDS handles:
- Discovering that both nodes exist
- Routing `/joint_cmd` messages from navigation to motors
- Routing `/encoder` messages from motors back to navigation
- Handling message ordering and delivery

You do not need to implement networking protocols—DDS provides the infrastructure.

---

## Why ROS 2 Instead of ROS 1?

If you have seen robotics tutorials online, many reference "ROS" (meaning ROS 1, also called "ROS Melodic" or "ROS Noetic"). ROS 1 was revolutionary but had limitations that matter for makers [7][8]:

| Issue | ROS 1 | ROS 2 |
|-------|-------|-------|
| **Operating System** | Linux only | Linux, Windows, macOS, embedded |
| **Real-time** | No guarantees | Designed for deterministic timing |
| **Microcontrollers** | Limited support (rosserial) | First-class support (micro-ROS) |
| **Network** | Single master required | Decentralized, peer-to-peer |
| **Security** | None | Encryption, authentication |
| **Support** | End of Life: May 2025 | Active development |

For maker projects, the key advantages of ROS 2:

1. **micro-ROS**: Run ROS 2 directly on ESP32, STM32, and other microcontrollers. No separate Arduino protocol needed.

2. **No rosmaster**: ROS 1 required a central "rosmaster" process. If it crashed, everything stopped. ROS 2 is decentralized—nodes discover each other automatically.

3. **Windows support**: Develop on your Windows laptop, deploy to Linux robot. ROS 1 required Linux for everything.

4. **Better embedded support**: The DDS layer is designed for resource-constrained systems.

If you are starting a new robot project, use ROS 2.

---

## Visualizing the Architecture

### Diagram 1: Humanoid as a Distributed System

```text
┌─────────────────────────────────────────────────────────────────┐
│           HUMANOID ROBOT - MAKER HARDWARE EDITION                │
└─────────────────────────────────────────────────────────────────┘

        ┌────────────────┐
        │   USB Camera   │
        │   (RPi)        │
        └───────┬────────┘
                │ /camera/image
                ▼
        ┌────────────────┐
        │   OpenCV       │
        │  Processing    │
        │   (RPi)        │
        └───────┬────────┘
                │ /detected_objects
                ▼
        ┌────────────────┐        ┌────────────────┐
        │   Gait         │◄───────┤   IMU Node     │
        │  Planner       │        │  (Arduino)     │
        │   (RPi)        │        │  /imu/data     │
        └───────┬────────┘        └────────────────┘
                │ /joint_commands
                ▼
        ┌────────────────┐        ┌────────────────┐
        │   Motor        │◄───────┤  Foot Sensors  │
        │  Controller    │        │  (Arduino)     │
        │   (Arduino)    │        │ /foot/pressure │
        └───────┬────────┘        └────────────────┘
                │ PWM Signals
                ▼
        ┌────────────────┐
        │   Servos       │
        │  (Dynamixel/   │
        │   Hobby)       │
        └────────────────┘
```

### Diagram 2: ROS 2 Communication Patterns

```text
┌─────────────────────────────────────────────────────────────────┐
│              COMMUNICATION PATTERNS FOR MAKERS                   │
└─────────────────────────────────────────────────────────────────┘

    TOPICS - Like Serial.println() broadcasting
    ─────────────────────────────────────────────
    ┌──────────┐                    ┌──────────┐
    │ MPU6050  │ ── /imu/data ────► │ Balance  │
    │  Node    │         │          │  Calc    │
    └──────────┘         │          └──────────┘
                         │          ┌──────────┐
                         └────────► │  Logger  │
                                    └──────────┘

    SERVICES - Like I2C register read
    ─────────────────────────────────────────────
    ┌──────────┐    "get_battery"   ┌──────────┐
    │  Main    │ ─────────────────► │   ADC    │
    │ Control  │ ◄───────────────── │  Reader  │
    └──────────┘    "11.2V"         └──────────┘

    ACTIONS - Like servo.write() with feedback
    ─────────────────────────────────────────────
    ┌──────────┐      Goal          ┌──────────┐
    │  User    │ ── "Go to (1,2)" ─►│   Nav    │
    │   App    │ ◄── "50% done" ─── │  Stack   │
    └──────────┘ ◄── "Arrived!" ─── └──────────┘
```

### Diagram 3: Sensor-Perception-Control Loop

```text
┌─────────────────────────────────────────────────────────────────┐
│                CONTINUOUS CONTROL LOOP                           │
└─────────────────────────────────────────────────────────────────┘

        Sensors                Process                  Actuate
    ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
    │ ○ Camera    │        │             │        │             │
    │ ○ IMU       │───────►│  Raspberry  │───────►│   Servos    │
    │ ○ Encoders  │        │     Pi      │        │   Motors    │
    │ ○ FSRs      │        │             │        │             │
    └─────────────┘        └─────────────┘        └──────┬──────┘
          ▲                                              │
          │              Physical World                  │
          └──────────────────────────────────────────────┘

    Loop Rate Examples:
    ├── IMU reading:     200 Hz (every 5ms)
    ├── Balance calc:    100 Hz (every 10ms)
    ├── Motor commands:   50 Hz (every 20ms)
    └── Camera process:   30 Hz (every 33ms)
```

---

## Try With AI

Test your understanding with this hands-on exercise. Use your AI assistant (ChatGPT, Claude, etc.) with this prompt:

**Prompt:**

```
I'm building a small bipedal robot with:
- Raspberry Pi 4 as main controller
- Arduino Nano reading MPU6050 IMU
- Arduino Mega controlling 12 servo motors via PCA9685
- USB camera for basic obstacle detection

Help me design the ROS 2 node architecture by identifying:
1. What nodes should I create?
2. What topics should connect them?
3. What services might be useful?
4. What actions would handle long-running tasks?

For each, explain whether it should use Topic, Service, or Action and why.

Then give me a scenario: "The robot sees an obstacle and needs to stop and plan
a new path." Walk me through which nodes communicate and how.
```

**What to evaluate in the response:**
- Does each sensor get its own publisher node?
- Do topics handle continuous data (IMU, camera)?
- Do services handle one-time queries (battery, calibration)?
- Do actions handle motion sequences (navigation, walking)?

Compare the AI's architecture suggestions with the patterns in this chapter. Ask follow-up questions about any differences.

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
