# Research: Module 1 Chapter 3 - URDF Modeling

**Feature**: 006-m1-chapter-3-content
**Date**: 2025-12-02
**Purpose**: Gather IEEE-format citations for all factual claims in Chapter 3

## Research Summary

All technical claims about URDF, TF, kinematic chains, and robot modeling require authoritative citations. This document consolidates research findings organized by topic area.

---

## 1. URDF (Unified Robot Description Format)

### Decision
Use official ROS 2 documentation and the original URDF specification as primary sources for URDF concepts.

### Rationale
URDF is a ROS-specific format maintained by Open Robotics. Official documentation is the authoritative source.

### Sources

[1] Open Robotics, "URDF - Unified Robot Description Format," ROS 2 Documentation, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html

[2] Open Robotics, "Building a Visual Robot Model from Scratch," ROS 2 Documentation, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-with-URDF-from-Scratch.html

[3] D. V. Lu, "URDF XML Specification," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML

---

## 2. Links and Rigid Body Concepts

### Decision
Cite robotics textbooks and ROS documentation for rigid body and link definitions.

### Rationale
Links as rigid bodies is a fundamental robotics concept with established academic sources.

### Sources

[4] B. Siciliano, L. Sciavicco, L. Villani, and G. Oriolo, Robotics: Modelling, Planning and Control. London, UK: Springer, 2009, pp. 1-50.

[5] Open Robotics, "URDF Link Element," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML/link

[6] J. J. Craig, Introduction to Robotics: Mechanics and Control, 4th ed. London, UK: Pearson, 2018, ch. 2.

---

## 3. Joints and Joint Types

### Decision
Use ROS URDF specification and robotics textbooks for joint type definitions.

### Rationale
Joint types (revolute, prismatic, fixed, continuous) are standard robotics terminology with formal definitions.

### Sources

[7] Open Robotics, "URDF Joint Element," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML/joint

[8] M. W. Spong, S. Hutchinson, and M. Vidyasagar, Robot Modeling and Control, 2nd ed. Hoboken, NJ: Wiley, 2020, ch. 3.

[9] R. M. Murray, Z. Li, and S. S. Sastry, A Mathematical Introduction to Robotic Manipulation. Boca Raton, FL: CRC Press, 1994, pp. 19-52.

---

## 4. Kinematic Chains

### Decision
Cite established robotics literature for kinematic chain definitions and forward kinematics concepts.

### Rationale
Kinematic chains are fundamental to robot mechanics with extensive academic literature.

### Sources

[10] B. Siciliano et al., Robotics: Modelling, Planning and Control, ch. 2, "Kinematics," pp. 39-100.

[11] J. J. Craig, Introduction to Robotics, ch. 3, "Forward and Inverse Kinematics."

[12] L. Sciavicco and B. Siciliano, Modelling and Control of Robot Manipulators, 2nd ed. London, UK: Springer, 2000, pp. 15-60.

---

## 5. Transform Tree (TF/TF2)

### Decision
Use official ROS 2 TF2 documentation as the authoritative source.

### Rationale
TF2 is a ROS 2 package with official documentation maintained by Open Robotics.

### Sources

[13] Open Robotics, "tf2 - ROS 2 Documentation," docs.ros.org, 2024. [Online]. Available: https://docs.ros.org/en/humble/Concepts/Intermediate/About-Tf2.html

[14] Open Robotics, "Introduction to tf2," ROS 2 Tutorials, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html

[15] T. Foote, "tf: The Transform Library," in Proc. IEEE Int. Conf. Technologies for Practical Robot Applications (TePRA), Woburn, MA, 2013, pp. 1-6.

---

## 6. Inertial Properties and Mass

### Decision
Cite robotics dynamics literature for mass, center of mass, and inertia concepts.

### Rationale
Physical properties of rigid bodies are foundational mechanics concepts with established sources.

### Sources

[16] R. Featherstone, Rigid Body Dynamics Algorithms. New York, NY: Springer, 2008, ch. 2.

[17] B. Siciliano et al., Robotics: Modelling, Planning and Control, ch. 7, "Dynamics," pp. 255-320.

[18] Open Robotics, "URDF Inertial Element," ROS Wiki, 2023. [Online]. Available: http://wiki.ros.org/urdf/XML/link#Inertial

---

## 7. Sensor Frames and Coordinate Systems

### Decision
Cite ROS sensor tutorials and coordinate frame conventions.

### Rationale
Sensor frame attachment is documented in ROS sensor integration guides.

### Sources

[19] Open Robotics, "Adding a Camera to a Simulated Robot," ROS 2 Tutorials, 2024. [Online]. Available: https://docs.ros.org/en/humble/Tutorials/Advanced/Simulators/Gazebo/Simulation-Gazebo.html

[20] REP 103, "Standard Units of Measure and Coordinate Conventions," ROS Enhancement Proposals, 2010. [Online]. Available: https://www.ros.org/reps/rep-0103.html

[21] REP 105, "Coordinate Frames for Mobile Platforms," ROS Enhancement Proposals, 2010. [Online]. Available: https://www.ros.org/reps/rep-0105.html

---

## 8. SDF (Simulation Description Format)

### Decision
Use Open Robotics SDF specification for comparison with URDF.

### Rationale
SDF is maintained by Open Robotics alongside Gazebo simulator.

### Sources

[22] Open Source Robotics Foundation, "SDFormat Specification," sdformat.org, 2024. [Online]. Available: http://sdformat.org/spec

[23] Open Robotics, "Gazebo Classic: SDF World and Robot Description," Gazebo Documentation, 2024. [Online]. Available: https://classic.gazebosim.org/tutorials?tut=build_world

---

## 9. Humanoid Robot Examples

### Decision
Cite commercial humanoid robots for real-world examples.

### Rationale
Specific humanoid examples make concepts tangible and connect to industry.

### Sources

[24] Unitree Robotics, "G1 Humanoid Robot," Unitree Documentation, 2024. [Online]. Available: https://www.unitree.com/g1

[25] Boston Dynamics, "Atlas Technical Specifications," Boston Dynamics, 2024. [Online]. Available: https://bostondynamics.com/atlas/

[26] Figure AI, "Figure 01 Humanoid Robot," Figure AI, 2024. [Online]. Available: https://www.figure.ai/

---

## 10. ROS 2 Architecture Reference (Chapter 2 Connection)

### Decision
Reference Chapter 2 content for ROS 2 communication concepts.

### Rationale
Build on prior knowledge established in Chapter 2.

### Sources

[27] S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall, "Robot Operating System 2: Design, architecture, and uses in the wild," Science Robotics, vol. 7, no. 66, May 2022. [Online]. Available: https://www.science.org/doi/10.1126/scirobotics.abm6074

[28] Open Robotics, "ROS 2 Documentation: Humble Hawksbill," docs.ros.org, 2024. [Online]. Available: https://docs.ros.org/en/humble/

---

## Citation Summary by Topic

| Topic | Primary Citations |
|-------|-------------------|
| URDF Basics | [1], [2], [3] |
| Links/Rigid Bodies | [4], [5], [6] |
| Joints | [7], [8], [9] |
| Kinematic Chains | [10], [11], [12] |
| TF/TF2 | [13], [14], [15] |
| Inertial Properties | [16], [17], [18] |
| Sensor Frames | [19], [20], [21] |
| SDF Comparison | [22], [23] |
| Humanoid Examples | [24], [25], [26] |
| ROS 2 Reference | [27], [28] |

---

## Alternatives Considered

### Alternative: Use only academic textbooks
**Rejected because**: URDF and TF are ROS-specific technologies not covered in traditional textbooks. Official ROS documentation is necessary.

### Alternative: Use Wikipedia for definitions
**Rejected because**: Constitution requires Tier 1 authoritative sources. Wikipedia is Tier 3 at best.

### Alternative: Use manufacturer documentation only
**Rejected because**: While useful for examples, manufacturer docs don't cover URDF/TF concepts. Need combination of ROS docs and academic sources.
