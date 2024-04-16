#!/bin/bash

#setup connection the the remote roscore using its IP address, make the IP address visible to all the containers, set the IP static if possible, else make it a parameter passed on during the docker run command to all containers.\
#export ROS_MASTER_URI=http://
#export ROS_IP=
#export ROS_HOSTNAME=
# source ~/.bashrc
# tmux new-session -s -d motor_demo
# tmux split-window -h
# # run roscore if running as a standalone container in the first pane
# tmux send-keys -t 0 'roscore' Enter
# # source the flo2 package environment and run the unilateral arm control node
# tmux send-keys -t 1 'sleep 5 && source ../../devel/setup.bash && roslaunch flo_humanoid read_write_arm_node' Enter 
# tmux split-window -v
# tmux send-keys 'sleep 5 && python3 src/motorControlDemo.py' Enter
# tmux attach-session -t motor_control_demo
# tmux new-session -s -d motor_demo
# tmux send-keys -t "echo hi" Enter

# source ~/.bashrc

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
