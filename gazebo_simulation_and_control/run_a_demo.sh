#!/usr/bin/env bash

# This script creates a new tmux session with multiple windows to run your commands sequentially.

# 1) Create a new tmux session (detached) called "my_ros_session"
tmux new-session -d -s "my_ros_session"

# Window 0 (automatically created by tmux): Run full_robot_arm_sim.launch
tmux send-keys -t "my_ros_session:0" "roslaunch movewithhead full_robot_arm_sim.launch" C-m

# 2) Create a new window for read_write_arms_node
tmux new-window -t "my_ros_session" -n "read_arms"
tmux send-keys -t "my_ros_session:read_arms" "rosrun flo_humanoid read_write_arms_node" C-m

# 3) Create a new window for dualPosition.py
tmux new-window -t "my_ros_session" -n "dualPos"
tmux send-keys -t "my_ros_session:dualPos" "rosrun movewithhead dualPosition.py" C-m

# ** Wait 5 seconds before creating the next window **
sleep 5

# 4) Create a new window for test.py
tmux new-window -t "my_ros_session" -n "test"
tmux send-keys -t "my_ros_session:test" "rosrun movewithhead test.py" C-m

# 5) Prompt the user for a pose number to pass into run_a_demo.py
read -p "Enter an action number: " poseNumber

# 6) Create a new window for run_a_demo.py (with the user input)
tmux new-window -t "my_ros_session" -n "demo"
tmux send-keys -t "my_ros_session:demo" "rosrun movewithhead run_a_demo.py ${poseNumber}" C-m

# Finally, attach to the tmux session so you can see everything
tmux attach-session -t "my_ros_session"
