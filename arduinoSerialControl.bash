#!/bin/bash
source ~/.bashrc
tmux new-session -d -s flo
#angle=10
#device=ACM0
#start RosCore
tmux rename-window startup
tmux send-keys 'roscore' Enter
#new terminal
rosrun rosserial_python serial_node.py /dev/$device
#in a new terminal window
rostopic pub servo std_msgs/UInt16  $angle