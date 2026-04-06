#!/usr/bin/env bash
# ============================================================
# Starts ROS, MQTT broker, sim, hardware bridge, and control node
# ============================================================

STATUS_DIR="${FLO_STATUS_DIR:-/runtime-status}"
STEP_RUNNER="${FLO_STEP_RUNNER:-/catkin_ws/src/FloSystemV2/docker_status_step.sh}"

mkdir -p "$STATUS_DIR/steps"

json_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

timestamp_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

write_step_status() {
  step="$1"
  state="$2"
  message="$3"
  ts="$(timestamp_utc)"
  escaped_message="$(json_escape "$message")"
  cat > "$STATUS_DIR/steps/${step}.json" <<EOF
{"step":"$step","state":"$state","message":"$escaped_message","timestamp":"$ts"}
EOF
}

write_overall_status() {
  state="$1"
  current_step="$2"
  message="$3"
  ts="$(timestamp_utc)"
  escaped_message="$(json_escape "$message")"
  cat > "$STATUS_DIR/bringup-status.json" <<EOF
{"state":"$state","current_step":"$current_step","message":"$escaped_message","timestamp":"$ts"}
EOF
}

append_event() {
  ts="$(timestamp_utc)"
  printf '%s %s\n' "$ts" "$1" >> "$STATUS_DIR/events.log"
}

mark_step() {
  step="$1"
  state="$2"
  message="$3"
  write_step_status "$step" "$state" "$message"
  write_overall_status "$state" "$step" "$message"
  append_event "[$step] $state - $message"
}

trap 'write_overall_status "stopped" "launcher" "tmux_robot_bringup_legacy.sh exited"; append_event "[launcher] stopped - tmux_robot_bringup_legacy.sh exited"' EXIT

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

write_overall_status "starting" "launcher" "Initializing tmux bringup session"
append_event "[launcher] starting - Initializing tmux bringup session"

# Create tmux session
tmux new-session -d -s "$SESSION_NAME"
tmux set-option -t "$SESSION_NAME" remain-on-exit on

# Window 0: ROS Core
mark_step "roscore" "starting" "Launching roscore"
tmux rename-window -t "${SESSION_NAME}:0" "roscore"
tmux send-keys -t "${SESSION_NAME}:roscore" "\"$STEP_RUNNER\" roscore source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && roscore" C-m

# Wait for roscore to start
sleep 5
write_overall_status "starting" "mqtt" "roscore started; moving to MQTT broker"
append_event "[launcher] starting - roscore started; moving to MQTT broker"

# Window 1: MQTT broker (skip if already running)
if pgrep -x mosquitto >/dev/null 2>&1; then
  echo "mosquitto already running; skipping broker launch"
  mark_step "mqtt" "running" "mosquitto already running; broker launch skipped"
  tmux new-window -t "$SESSION_NAME" -n "mqtt"
  tmux send-keys -t "${SESSION_NAME}:mqtt" "echo 'mosquitto already running; broker launch skipped'" C-m
else
  mark_step "mqtt" "starting" "Launching mosquitto broker"
  tmux new-window -t "$SESSION_NAME" -n "mqtt"
  tmux send-keys -t "${SESSION_NAME}:mqtt" "\"$STEP_RUNNER\" mqtt mosquitto -v -p 1883" C-m
fi
sleep 2
write_overall_status "starting" "moveit" "MQTT broker step launched; moving to MoveIt/sim"
append_event "[launcher] starting - MQTT broker step launched; moving to MoveIt/sim"

# Window 2: Gazebo sim + MoveIt + RViz (GUI off)
mark_step "moveit" "starting" "Launching full_robot_arm_sim.launch"
tmux new-window -t "$SESSION_NAME" -n "Sim+Moveit"
tmux send-keys -t "${SESSION_NAME}:sim" "\"$STEP_RUNNER\" moveit source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && roslaunch flo_core full_robot_arm_sim.launch show_gz_gui:=false show_rviz_gui:=false" C-m
sleep 2
write_overall_status "starting" "hardware" "MoveIt/sim step launched; moving to hardware bridge"
append_event "[launcher] starting - MoveIt/sim step launched; moving to hardware bridge"

# Window 3: Hardware bridge
mark_step "hardware" "starting" "Launching dual_arm_hardware.launch"
tmux new-window -t "$SESSION_NAME" -n "hardware"
tmux send-keys -t "${SESSION_NAME}:hardware" "\"$STEP_RUNNER\" hardware source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && roslaunch flo_humanoid dual_arm_hardware.launch publish_joint_states:=false" C-m

sleep 20
write_overall_status "starting" "controller" "Hardware bridge step launched; moving to controller"
append_event "[launcher] starting - Hardware bridge step launched; moving to controller"

# Window 4: MQTT control node
mark_step "controller" "starting" "Launching mqtt_control_node.py"
tmux new-window -t "$SESSION_NAME" -n "control"
tmux send-keys -t "${SESSION_NAME}:control" "\"$STEP_RUNNER\" controller source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && rosrun flo_core mqtt_control_node.py" C-m

sleep 10

# Window 5: Monitoring panes (timing, queue, runner)
tmux new-window -t "$SESSION_NAME" -n "monitor"
tmux send-keys -t "${SESSION_NAME}:monitor.0" "mosquitto_sub -h localhost -t ros/mqtt/action_time" C-m
tmux split-window -t "${SESSION_NAME}:monitor" -h
tmux send-keys -t "${SESSION_NAME}:monitor.1" "mosquitto_sub -h localhost -t ros/mqtt/queue_state" C-m


# Window 6: Interactive shell
tmux new-window -t "$SESSION_NAME" -n "shell"
tmux send-keys -t "${SESSION_NAME}:shell" "source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\"" C-m
tmux send-keys -t "${SESSION_NAME}:shell" "echo 'Interactive shell - you can run ROS/MQTT commands here'" C-m
tmux send-keys -t "${SESSION_NAME}:shell" "echo 'Example: mosquitto_pub -h localhost -t ros/mqtt/movement -m \"0\"'" C-m

# Attach to session
write_overall_status "ready" "launcher" "All bringup steps launched; attaching to tmux"
append_event "[launcher] ready - All bringup steps launched; attaching to tmux"
echo "Attaching to tmux session '$SESSION_NAME'..."
echo "Use 'Ctrl+B then number' to switch windows"
echo "Use 'Ctrl+B then d' to detach"
sleep 2
tmux attach-session -t "$SESSION_NAME"
