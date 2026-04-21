# Old Vs New Architecture

This note summarizes the architectural shift from the older mixed simulation/hardware flow to the current hardware-owned control path.

## At A Glance

| Area | Older mixed flow | Current supported flow |
| --- | --- | --- |
| Planning client | `mqtt_control_node.py` using MoveIt | `mqtt_control_node.py` using MoveIt |
| MoveIt execution target | Gazebo-backed `ros_control` in the mixed test path | Hardware action servers through the simple controller manager |
| Primary `/joint_states` source | Gazebo in the mixed test scripts | `read_write_arms_node` on the hardware side |
| Clock behavior | Sim time could depend on Gazebo progress | Optional monotonic `/clock` independent of Gazebo |
| Robot state ownership | Split between simulation and hardware processes | Hardware stack is the source of truth |
| Default bringup | Mixed sim + hardware launchers existed for testing | Main bringup is hardware-first and does not launch Gazebo |

## Old Mixed Architecture

```text
MQTT commands
    |
    v
mqtt_control_node.py
    |
    v
move_group / MoveIt
    |
    v
Gazebo + ros_control
    |
    +--> /joint_states
    +--> /clock
    +--> simulated controller execution

In parallel:
dual_arm_hardware.launch
    |
    v
read_write_arms_node
    |
    v
Dynamixel hardware
```

Notes:

- The older mixed test scripts launched Gazebo + MoveIt and also launched the hardware node.
- In that setup, hardware joint-state publishing was typically disabled so Gazebo remained the state source.
- If Gazebo stalled while sim time was in use, `/clock` and any time-dependent behavior could appear frozen.

## Current Supported Architecture

```text
MQTT commands
    |
    v
mqtt_control_node.py
    |
    v
move_group / MoveIt
    |
    v
simple MoveIt controller manager
    |
    v
dual_arm_hardware.launch
    |
    v
read_write_arms_node
    |
    +--> left/right FollowJointTrajectory action servers
    +--> /joint_states
    +--> robot_description
    +--> robot_state_publisher
    |
    v
Dynamixel hardware

Optional:
monotonic_clock.py -> /clock
```

Notes:

- The main bringup path is now hardware-first and does not require Gazebo.
- The hardware node publishes live joint state by default, so MoveIt plans from real robot feedback.
- A dedicated monotonic clock can provide `/clock` without relying on Gazebo to keep advancing.

## Why The New Path Is Better

- Fewer components are on the critical path for real-hardware operation.
- The real robot is the default source of truth for joint state.
- Time progression is no longer tied to Gazebo in the main supported bringup.
- Controller ownership is clearer: MoveIt sends trajectories to hardware-owned action servers instead of a parallel simulation controller stack.
