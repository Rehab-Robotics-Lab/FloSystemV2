## Architecture Diagrams

- `current_stack_root_issue.drawio`: editable draw.io source
- `current_stack_root_issue.svg`: checked-in vector rendering

The diagram shows the current Windows + WSL2 + Docker + ROS + Dynamixel stack and highlights the root issue:

- real hardware is driven from simulated `/joint_states`
- there is no deterministic hardware trajectory controller between `MoveIt` and the Dynamixel bus
