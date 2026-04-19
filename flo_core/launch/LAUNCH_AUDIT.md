# FLO Core Launch Audit

Reviewed on 2026-04-19.

This note records which `flo_core/launch` files are currently part of the supported stack, which ones are kept as internal dependencies, and which ones were moved to `launch/archive/` because they appear stale or unused.

## Supported Entry Points

- `moveit_bringup.launch`
  - Official MoveIt bringup entry point for hardware-backed and fake-controller sessions.
  - Referenced by the root `README.md` and `tmux_robot_bringup_legacy.sh`.
- `moveit_gazebo_bringup.launch`
  - Canonical Gazebo + MoveIt bringup path built from `gazebo.launch` plus `moveit_bringup.launch`.
  - Supports the legacy `show_gz_gui` and `show_rviz_gui` flags so older callers can migrate cleanly.
- `full_robot_arm_sim.launch`
  - Legacy compatibility wrapper around `moveit_gazebo_bringup.launch`.
  - Kept temporarily so older external callers do not break.

## Core Include-Only Launch Files

These are not primary user-facing entry points, but they are part of the active stack and should stay under `launch/`.

- `move_group.launch`
- `planning_context.launch`
- `planning_pipeline.launch.xml`
- `trajectory_execution.launch.xml`
- `sensor_manager.launch.xml`
- `moveit_rviz.launch`
- `default_warehouse_db.launch`
- `warehouse.launch`
- `warehouse_settings.launch.xml`
- `fake_moveit_controller_manager.launch.xml`
- `simple_moveit_controller_manager.launch.xml`
- `ros_control_moveit_controller_manager.launch.xml`
- `ompl_planning_pipeline.launch.xml`
- `chomp_planning_pipeline.launch.xml`
- `pilz_industrial_motion_planner_planning_pipeline.launch.xml`
- `gazebo.launch`
- `gazebo_full_system.launch`
- `ros_controllers.launch`
- `moveit.rviz`
- `setup_assistant.launch`

## Archived Files

These files were moved to `launch/archive/` because they had no in-repo callers, were clearly superseded, or appeared broken against the current tree.

- `simonsays_launcher_prod.launch`
  - Launches scripts that are no longer present in the active package.
- `gazebo_basic_sim.launch`
  - Standalone minimal Gazebo helper superseded by richer simulation launchers.
- `joystick_control.launch`
  - Optional MoveIt joystick helper with no current callers.
- `rviz_model_viewer.launch`
  - Standalone visualization helper with no current callers.
- `run_benchmark_ompl.launch`
  - Benchmark-only launcher with no current callers.
- `ompl-chomp_planning_pipeline.launch.xml`
  - Unused combined planning-pipeline helper.
- `stomp_planning_pipeline.launch.xml`
  - Unused STOMP planning-pipeline helper.
- `flov2_robot_description_moveit_sensor_manager.launch.xml`
  - Empty file with no current callers.

## Follow-Up Cleanup Worth Considering

- Once downstream users have migrated, archive `full_robot_arm_sim.launch` and keep `moveit_gazebo_bringup.launch` as the only Gazebo+MoveIt entry point.
- Repair or remove the `debug:=true` path in `move_group.launch`, which references a missing `gdb_settings.gdb` file.
