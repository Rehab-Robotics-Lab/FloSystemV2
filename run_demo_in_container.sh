#!/usr/bin/env bash
# ============================================================
# Script to run inside Docker container for demo
# This runs the fake controller demo (visualization only, no hardware)
# ============================================================

echo "=== FLO v2 Demo Launcher ==="
echo ""
echo "This will start:"
echo "  1. ROS Core"
echo "  2. MoveIt demo.launch (fake controller)"
echo "  3. RViz visualization"
echo ""
echo "Press Ctrl+C in any tmux window to stop"
echo ""

# Source ROS environment
source /opt/ros/noetic/setup.bash
source /catkin_ws/devel/setup.bash

# Create tmux session
tmux new-session -d -s flo_demo

# Window 0: ROS Core
tmux rename-window -t "flo_demo:0" "roscore"
tmux send-keys -t "flo_demo:roscore" "source /catkin_ws/devel/setup.bash && roscore" C-m

# Wait for roscore to start
sleep 3

# Window 1: MoveIt demo
tmux new-window -t "flo_demo" -n "moveit"
tmux send-keys -t "flo_demo:moveit" "source /catkin_ws/devel/setup.bash && roslaunch flo_core demo.launch use_rviz:=true moveit_controller_manager:=fake" C-m

# Window 2: Main controller (optional, comment out if not needed)
# tmux new-window -t "flo_demo" -n "controller"
# tmux send-keys -t "flo_demo:controller" "source /catkin_ws/devel/setup.bash && sleep 10 && rosrun flo_core main_controller_clean.py" C-m

# Window 3: Interactive shell
tmux new-window -t "flo_demo" -n "shell"
tmux send-keys -t "flo_demo:shell" "source /catkin_ws/devel/setup.bash" C-m
tmux send-keys -t "flo_demo:shell" "echo 'Interactive shell - you can run ROS commands here'" C-m
tmux send-keys -t "flo_demo:shell" "echo 'Example: rostopic list, rostopic pub /ros/mqtt/movement std_msgs/String \"7\"'" C-m

# Attach to session
echo "Attaching to tmux session 'flo_demo'..."
echo "Use 'Ctrl+B then number' to switch windows"
echo "Use 'Ctrl+B then d' to detach"
sleep 2
tmux attach-session -t flo_demo

