#!/bin/bash

#setup connection the the remote roscore using its IP address, make the IP address visible to all the containers, set the IP static if possible, else make it a parameter passed on during the docker run command to all containers.\
#export ROS_MASTER_URI=http://
#export ROS_IP=
#export ROS_HOSTNAME=
tmux new-session -d -s motor_demo
tmux rename-window startup
tmux send-keys 'roscore' Enter
tmux split-window -t motor_demo -h
tmux send-keys 'sleep 5 && source ../../devel/setup.bash && rosrun flo_humanoid read_write_arm_node' Enter
tmux split-window -t motor_demo -v
tmux send-keys 'htop' Enter
tmux split-window -t motor_demo -h
tmux send-keys 'sleep 5 && python3 src/motorControlDemo.py' Enter
tmux attach-session -t motor_demo
