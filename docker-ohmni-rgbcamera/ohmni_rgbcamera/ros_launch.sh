#!/bin/bash
#
# Setup a work space called `work` with two windows
session="work"

# set up tmux
tmux start-server

# create a new tmux session, starting vim from a saved session in the new window
tmux new-session -d -s $session -n base
tmux send-keys "roscore" C-m

tmux selectp -t 0
tmux splitw -h -p 60
tmux send-keys "sleep 5; roslaunch /maincam_v4l2.launch" C-m

tmux selectp -t 0
tmux splitw -v -p 50
tmux send-keys "htop" C-m
