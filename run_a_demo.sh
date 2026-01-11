#!/usr/bin/env bash

# This script creates a new tmux session with multiple windows to run your commands sequentially.

# 0) Create a new tmux session (detached) called "my_ros_session"
tmux new-session -d -s "my_ros_session"

# 1) Create window[0] for mosquitto broker (must be first so others can connect)
tmux rename-window -t "my_ros_session:0" "mqtt"
tmux send-keys -t "my_ros_session:mqtt" "mosquitto" C-m

# 2) Create a new window for full_robot_arm_sim.launch
tmux new-window -t "my_ros_session" -n "sim"
tmux send-keys -t "my_ros_session:sim" "source devel/setup.bash && roslaunch movewithhead full_robot_arm_sim.launch" C-m

# 3) Create a new window for read_write_arms_node
tmux new-window -t "my_ros_session" -n "read_arms"
tmux send-keys -t "my_ros_session:read_arms" "source devel/setup.bash && rosrun flo_humanoid read_write_arms_node" C-m

# 4) Create a new window for dualPosition.py
tmux new-window -t "my_ros_session" -n "dualPos"
tmux send-keys -t "my_ros_session:dualPos" "source devel/setup.bash && rosrun movewithhead dualPosition.py" C-m

# 5) Wait 5 seconds before creating the next window
sleep 5

# 6) Create a new window for test.py
tmux new-window -t "my_ros_session" -n "test"
tmux send-keys -t "my_ros_session:test" "source devel/setup.bash && rosrun movewithhead test.py" C-m

# 7) Prompt the user for a pose number to pass into run_a_demo.py
read -p "Enter an action number: " poseNumber

# 8) Create a new window for run_a_demo.py (with the user input)
tmux new-window -t "my_ros_session" -n "demo"
tmux send-keys -t "my_ros_session:demo" "source devel/setup.bash && rosrun movewithhead run_a_demo.py ${poseNumber}" C-m

# 9) Attach to the tmux session so you can see everything
tmux attach-session -t "my_ros_session"
