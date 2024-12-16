## flo_humanoid

This package focuses on motor control for the Flo V2 robot, particularly for sending motor positions to the robot.

---

### Key Functionality

- The main file used is `readWriteArms.cpp`.  
  It can simultaneously send data for **10 motors** to the robot based on motor IDs.

- **Communication Flow**:  
  - Subscribes to the topic `/set_arms_joint_positions`, which is published by the control program `dualPosition.py` in the `movewithhead` package.  
  - Uses the `GetArmsJointPositions.srv` service to define the data format sent to the motors.

---

### Nodes

The `flo_humanoid` package provides several ROS nodes for motor control and position management:

| **Node Name**                | **Executable**           | **File**                         | **Description**                          |
|------------------------------|--------------------------|----------------------------------|------------------------------------------|
| `read_write_joint_node`      | `read_write_joint_node`  | `src/readWriteJoint.cpp`         | Reads and writes joint motor positions.  |
| `read_write_arm_node`        | `read_write_arm_node`    | `src/readWriteArm.cpp`           | Reads and writes single arm motor data.  |
| `read_write_arms_node`       | `read_write_arms_node`   | `src/readWriteArms.cpp`          | Controls both arms simultaneously.       |
| `publish_motor_positions`    | `publish_motor_positions`| `src/publish_motor_positions.cpp`| Publishes motor positions for testing.   |
| `subscribe_motor_positions`  | `subscribe_motor_positions`| `src/subscribe_motor_positions.cpp` | Subscribes to motor position data.       |

---

### File Structure

```plaintext
flo_humanoid/
│
├── config/                # Configuration files
├── msg/                   # Custom message definitions
├── srv/                   # Service definitions (e.g., GetArmsJointPositions.srv)
├── src/                   # Source code files
│   ├── publish_motor_positions.cpp       # Publishes motor positions
│   ├── readWriteArm.cpp                  # Reads and writes a single arm's motor data
│   ├── readWriteArms.cpp                 # Reads and writes both arms' motor data
│   ├── readWriteEndEff.cpp               # Controls the end-effector motor data
│   ├── readWriteJoint.cpp                # Reads and writes joint motor positions
│   └── subscribe_motor_positions.cpp     # Subscribes to motor positions
│
├── basicMotorTest.bash     # Script for motor testing
├── CMakeLists.txt          # Build configuration
├── Dockerfile              # Docker container configuration
├── package.xml             # ROS package metadata
└── readme.md               # Package documentation
```

---

### Usage Instructions

1. **Build the Package**:  
   Ensure the package is in your workspace `src` folder, then build it:
   ```bash
   cd ~/your_workspace
   catkin_make
   ```

2. **Run Nodes**: Use `rosrun` to execute the nodes as follows:

   - **Read and Write Joint Motor Positions**:
     ```bash
     rosrun flo_humanoid read_write_joint_node
     ```
   - **Read and Write Single Arm Motor Data**:
     ```bash
     rosrun flo_humanoid read_write_arm_node
     ```
   - **Control Both Arms Simultaneously**:
     ```bash
     rosrun flo_humanoid read_write_arms_node
     ```
   - **Publish Motor Positions for Testing**:
     ```bash
     rosrun flo_humanoid publish_motor_positions
     ```
   - **Subscribe to Motor Position Data**:
     ```bash
     rosrun flo_humanoid subscribe_motor_positions
     ```

3. **Communication**:  
   - The `read_write_arms_node` subscribes to the `/set_arms_joint_positions` topic, which is published by `dualPosition.py` from the `movewithhead` package.  
   - Data format for motor positions is defined in the `GetArmsJointPositions.srv` service.

---

### Notes

- Ensure **ROS Noetic** is installed and configured.  
- The `readWriteArms.cpp` file is critical for controlling multiple motors simultaneously.  
- Use the provided nodes to test and control the robot's motors efficiently.

---

## License

This project is licensed under the [MIT License](LICENSE).
