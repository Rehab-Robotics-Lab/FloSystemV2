#!/usr/bin/env bash
# ============================================================
# Starts ROS, MQTT broker, MoveIt, hardware controller, and control node
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
echo "  2. Monotonic ROS clock publisher (optional sim time)"
echo "  3. MQTT broker (mosquitto)"
echo "  4. Dynamixel hardware controller"
echo "  5. MoveIt (no Gazebo)"
echo "  6. MQTT control node"
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

source /opt/ros/noetic/setup.sh
source "$WORKSPACE_SETUP"

SESSION_NAME="flo_robot_test"
USE_MONOTONIC_CLOCK="${FLO_USE_MONOTONIC_CLOCK:-false}"
USE_SIM_TIME="false"
CLOCK_MODE_MESSAGE="Clock mode: wall time"

if [ "$USE_MONOTONIC_CLOCK" = "true" ]; then
  USE_SIM_TIME="true"
  CLOCK_MODE_MESSAGE="Clock mode: monotonic /clock with use_sim_time=true"
fi

echo "$CLOCK_MODE_MESSAGE"
append_event "[launcher] info - $CLOCK_MODE_MESSAGE"

write_overall_status "starting" "launcher" "Initializing tmux bringup session"
append_event "[launcher] starting - Initializing tmux bringup session"

tmux new-session -d -s "$SESSION_NAME"
tmux set-option -t "$SESSION_NAME" remain-on-exit on

mark_step "roscore" "starting" "Launching roscore"
tmux rename-window -t "${SESSION_NAME}:0" "roscore"
tmux send-keys -t "${SESSION_NAME}:roscore" "\"$STEP_RUNNER\" roscore source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && roscore" C-m

sleep 5
if [ "$USE_MONOTONIC_CLOCK" = "true" ]; then
  mark_step "clock" "starting" "Enabling /use_sim_time and launching monotonic /clock publisher"
  tmux new-window -t "$SESSION_NAME" -n "clock"
  tmux send-keys -t "${SESSION_NAME}:clock" "\"$STEP_RUNNER\" clock source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && rosparam set /use_sim_time true && roslaunch flo_humanoid monotonic_clock.launch" C-m
  sleep 3
else
  echo "$CLOCK_MODE_MESSAGE"
fi

write_overall_status "starting" "mqtt" "ROS time configuration complete; moving to MQTT broker"
append_event "[launcher] starting - ROS time configuration complete; moving to MQTT broker"

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
write_overall_status "starting" "hardware" "MQTT broker step launched; moving to hardware controller"
append_event "[launcher] starting - MQTT broker step launched; moving to hardware controller"

mark_step "hardware" "starting" "Launching dual_arm_hardware.launch"
tmux new-window -t "$SESSION_NAME" -n "hardware"
tmux send-keys -t "${SESSION_NAME}:hardware" "\"$STEP_RUNNER\" hardware source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && roslaunch flo_humanoid dual_arm_hardware.launch use_sim_time:=$USE_SIM_TIME" C-m

sleep 10
write_overall_status "starting" "moveit" "Hardware controller step launched; moving to MoveIt"
append_event "[launcher] starting - Hardware controller step launched; moving to MoveIt"

mark_step "moveit" "starting" "Launching moveit_bringup.launch against hardware action servers"
tmux new-window -t "$SESSION_NAME" -n "moveit"
tmux send-keys -t "${SESSION_NAME}:moveit" "\"$STEP_RUNNER\" moveit source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && roslaunch flo_core moveit_bringup.launch moveit_controller_manager:=simple use_rviz:=false load_robot_description:=false use_sim_time:=$USE_SIM_TIME" C-m

sleep 10
write_overall_status "starting" "controller" "MoveIt step launched; moving to controller"
append_event "[launcher] starting - MoveIt step launched; moving to controller"

mark_step "controller" "starting" "Launching mqtt_control_node.py"
tmux new-window -t "$SESSION_NAME" -n "control"
tmux send-keys -t "${SESSION_NAME}:control" "\"$STEP_RUNNER\" controller source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\" && rosrun flo_core mqtt_control_node.py" C-m

sleep 10

tmux new-window -t "$SESSION_NAME" -n "monitor"
tmux send-keys -t "${SESSION_NAME}:monitor.0" "mosquitto_sub -h localhost -t ros/mqtt/action_result" C-m
tmux split-window -t "${SESSION_NAME}:monitor" -h
tmux send-keys -t "${SESSION_NAME}:monitor.1" "mosquitto_sub -h localhost -t ros/mqtt/queue_state" C-m

tmux new-window -t "$SESSION_NAME" -n "shell"
tmux send-keys -t "${SESSION_NAME}:shell" "source /opt/ros/noetic/setup.sh && source \"$WORKSPACE_SETUP\"" C-m
tmux send-keys -t "${SESSION_NAME}:shell" "echo '$CLOCK_MODE_MESSAGE'" C-m
tmux send-keys -t "${SESSION_NAME}:shell" "echo 'ROS time health check:'" C-m
tmux send-keys -t "${SESSION_NAME}:shell" "rosparam get /use_sim_time || true" C-m
tmux send-keys -t "${SESSION_NAME}:shell" "timeout 3 rostopic echo -n1 /clock || echo '/clock not published'" C-m
tmux send-keys -t "${SESSION_NAME}:shell" "echo 'Interactive shell - you can run ROS/MQTT commands here'" C-m
tmux send-keys -t "${SESSION_NAME}:shell" "echo 'Example: mosquitto_pub -h localhost -t ros/mqtt/movement -m \"0\"'" C-m

# Keep the session from shrinking to the attaching client size at the end of bringup.
tmux set-option -t "$SESSION_NAME" -g window-size largest

write_overall_status "ready" "launcher" "All bringup steps launched; attaching to tmux"
append_event "[launcher] ready - All bringup steps launched; attaching to tmux"
echo "Attaching to tmux session '$SESSION_NAME'..."
echo "Use 'Ctrl+B then number' to switch windows"
echo "Use 'Ctrl+B then d' to detach"
sleep 2
tmux attach-session -t "$SESSION_NAME"
