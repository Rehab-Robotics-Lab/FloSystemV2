#!/bin/bash
#
# Setup a work space called `work`
session="work"

# set up tmux
tmux start-server

# create a new tmux session
tmux new-session -d -s $session -n base
#This will start a new roscore if no remote roscore has been detected
#Ideally we should change the .bashrc file to reflect the IP of the remote master and roscore will connect to remote master
tmux send-keys "roscore" C-m

# launch main front facing camera after sleeping for 20 seconds 
tmux selectp -t 0
tmux splitw -h -p 50
tmux send-keys "sleep 20; roslaunch /maincam_v4l2.launch" C-m


# launch aux downward facing camera after sleeping for 25 seconds
tmux selectp -t 0
tmux splitw -v -p 50
tmux send-keys "sleep 25; roslaunch /auxcam_v4l2.launch" C-m

#open the htop system monitor to show system resource usage
tmux selectp -t 1
tmux splitw -v -p 50
tmux send-keys "htop" C-m
