## Architecture Diagrams

- `current_stack_root_issue.drawio`: editable draw.io source
- `current_stack_root_issue.svg`: checked-in vector rendering
- `old_vs_new_architecture.md`: short report-ready comparison of the legacy mixed sim/hardware flow vs the current hardware-owned flow

The diagram now shows the current working Windows + WSL2 + Docker + ROS + Dynamixel stack:

- `mqtt_control_node.py` receives MQTT movement commands
- `move_group` plans through the simple MoveIt controller manager
- `read_write_arms_node` exposes the hardware `FollowJointTrajectory` action servers
- `read_write_arms_node` owns `/joint_states`
- `robot_state_publisher` derives TF from live hardware feedback

This replaces the older sim-driven architecture where real hardware followed simulated `/joint_states`.

## Old Vs New Summary

| Area | Older mixed flow | Current supported flow |
| --- | --- | --- |
| Main execution path | `mqtt_control_node.py` -> MoveIt -> Gazebo `ros_control` | `mqtt_control_node.py` -> MoveIt -> hardware action servers |
| State source | Gazebo-owned `/joint_states` in the mixed test flow | Hardware-owned `/joint_states` by default |
| Hardware node role | Ran in parallel, often with `publish_joint_states:=false` | Owns execution, robot description, and live joint state |
| Clock source | Gazebo-backed sim time when that path was used | Optional monotonic `/clock` independent of Gazebo |
| Failure mode | Gazebo stall could freeze sim-driven time/state updates | Less coupled to simulation, fewer moving pieces in the default path |
| Default intent | Mixed simulation and hardware bringup | Direct hardware-backed planning and execution |
