## Architecture Diagrams

- `current_stack_root_issue.drawio`: editable draw.io source
- `current_stack_root_issue.svg`: checked-in vector rendering

The diagram now shows the current working Windows + WSL2 + Docker + ROS + Dynamixel stack:

- `mqtt_control_node.py` receives MQTT movement commands
- `move_group` plans through the simple MoveIt controller manager
- `read_write_arms_node` exposes the hardware `FollowJointTrajectory` action servers
- `read_write_arms_node` owns `/joint_states`
- `robot_state_publisher` derives TF from live hardware feedback

This replaces the older sim-driven architecture where real hardware followed simulated `/joint_states`.
