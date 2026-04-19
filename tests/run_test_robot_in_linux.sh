#!/usr/bin/env zsh
# ============================================================
# Script to run on Linux for hardware test
# Starts ROS, MQTT broker, sim, hardware bridge, and control node
# ============================================================

echo "=== FLO v2 Robot Test Launcher ==="
echo ""
echo "This will start:"
echo "  1. ROS Core"
echo "  2. MQTT broker (mosquitto)"
echo "  3. Gazebo sim + MoveIt + RViz (GUI off by default)"
echo "  4. Hardware bridge"
echo "  5. MQTT control node"
echo ""
echo "Press Ctrl+C in any tmux window to stop"
echo ""

if [ ! -f /opt/ros/noetic/setup.sh ]; then
  echo "ROS Noetic not found at /opt/ros/noetic/setup.sh"
  exit 1
fi

if [ -f /catkin_ws/devel/setup.sh ]; then
  WORKSPACE_SETUP="/catkin_ws/devel/setup.sh"
elif [ -f "$HOME/catkin_ws_floV2/devel/setup.sh" ]; then
  WORKSPACE_SETUP="$HOME/catkin_ws_floV2/devel/setup.sh"
elif [ -f "$HOME/catkin_ws/devel/setup.sh" ]; then
  WORKSPACE_SETUP="$HOME/catkin_ws/devel/setup.sh"
else
  echo "Could not find a catkin workspace setup.sh"
  exit 1
fi

# Source ROS environment for this shell
source /opt/ros/noetic/setup.sh
source "$WORKSPACE_SETUP"

SESSION_NAME="flo_robot_test"

# Create tmux session
tmux new-session -d -s "$SESSION_NAME"

# Window 0: ROS Core
tmux rename-window -t "${SESSION_NAME}:0" "roscore"
tmux send-keys -t "${SESSION_NAME}:roscore" "source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && roscore" C-m

# Wait for roscore to start
sleep 3

# Window 1: MQTT broker (skip if already running)
if pgrep -x mosquitto >/dev/null 2>&1; then
  echo "mosquitto already running; skipping broker launch"
  tmux new-window -t "$SESSION_NAME" -n "mqtt"
  tmux send-keys -t "${SESSION_NAME}:mqtt" "echo 'mosquitto already running; broker launch skipped'" C-m
else
  tmux new-window -t "$SESSION_NAME" -n "mqtt"
  tmux send-keys -t "${SESSION_NAME}:mqtt" "mosquitto -v -p 1883" C-m
fi

# Window 2: Gazebo sim + MoveIt + RViz (GUI off)
tmux new-window -t "$SESSION_NAME" -n "sim"
tmux send-keys -t "${SESSION_NAME}:sim" "source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && roslaunch flo_core moveit_gazebo_bringup.launch show_gz_gui:=true show_rviz_gui:=false" C-m

# Window 3: Hardware bridge
tmux new-window -t "$SESSION_NAME" -n "hardware"
tmux send-keys -t "${SESSION_NAME}:hardware" "source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && roslaunch flo_humanoid dual_arm_hardware.launch publish_joint_states:=false" C-m

sleep 10

# Window 4: MQTT control node
tmux new-window -t "$SESSION_NAME" -n "control"
tmux send-keys -t "${SESSION_NAME}:control" "source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && rosrun flo_core mqtt_control_node.py" C-m

sleep 5

# Window 5: Interactive shell
tmux new-window -t "$SESSION_NAME" -n "shell"
tmux send-keys -t "${SESSION_NAME}:shell" "source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\"" C-m
tmux send-keys -t "${SESSION_NAME}:shell" "echo 'Interactive shell - you can run ROS/MQTT commands here'" C-m
tmux send-keys -t "${SESSION_NAME}:shell" "echo 'Example: mosquitto_pub -h localhost -t ros/mqtt/movement -m \"0\"'" C-m

# Attach to session
echo "Attaching to tmux session '$SESSION_NAME'..."
echo "Use 'Ctrl+B then number' to switch windows"
echo "Use 'Ctrl+B then d' to detach"
sleep 2
tmux attach-session -t "$SESSION_NAME"
