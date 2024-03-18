#!/bin/bash
# container default set to bash, maybe change that 
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
source devel/setup.bash 
#setup connection the the remote roscore using its IP address, make the IP address visible to all the containers, set the IP static if possible, else make it a parameter passed on during the docker run command to all containers.\
#export ROS_MASTER_URI=http://
#export ROS_IP=
#export ROS_HOSTNAME=
tmux new -s motor_control_demo;
tmux attach -t motor_control_demo;

# run roscore if running as a standalone container
tmux send-keys 'roscore' ENTER;
tmux split-window;                               
tmux send 'rosrun flo_humanoid read_write_arm_node';       # run the unilateral arm control node
tmux split-window;
tmux send 'rosrun motor_control_demo motor_control_demo_node';
tmux detach;