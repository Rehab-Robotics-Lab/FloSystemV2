#!/bin/bash
# container default set to bash, maybe change that 

#This script still has issues, do not use
"""
source ~/.bashrc

tmux new-session -d -s flo
tmux rename-window startup
tmux send-keys 'connect_to_robot 0 && roscore' Enter
tmux split-window -t flo -h


tmux split-window -t flo
tmux send-keys 'mkdir -p ~/flo_data && connect_to_robot 0 && roslaunch --wait flo_core podium_bringup.launch' Enter # it is just more stable..

tmux rotate-window -t flo

tmux split-window -t flo -h
tmux send-keys 'sleep 5 && connect_to_robot 0 && roslaunch --wait flo_telepresence realsense-sp-1.launch platform:=podium' Enter # it is just more stable..

tmux split-window -t flo
tmux send-keys 'sleep 10 && connect_to_robot 0 && roslaunch --wait flo_telepresence realsense-sp-2.launch platform:=podium' Enter # it is just more stable..
"""

#source the workspace
#setup connection the the remote roscore using its IP address, make the IP address visible to all the containers, set the IP static if possible, else make it a parameter passed on during the docker run command to all containers.\
#export ROS_MASTER_URI=http://
#export ROS_IP=
#export ROS_HOSTNAME=
tmux new -d -s motor_control_demo;
tmux rename-window roscore;
tmux attach -t motor_control_demo;
# run roscore if running as a standalone container
tmux send-keys 'roscore' ENTER;
# if running as part of system connected to remote ROS master, check connection status.
tmux split-window;    
tmux send-keys 'source ../../devel/setup.bash' ENTER;
tmux send-keys 'rosrun flo_humanoid read_write_arm_node' ENTER;       # run the unilateral arm control node
tmux split-window;
tmux send-keys 'python3 src/motorControlDemo.py' ENTER;               # run the motor control demo
tmux detach;