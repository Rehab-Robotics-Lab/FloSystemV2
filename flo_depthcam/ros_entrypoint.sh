#setup connection the the remote roscore using its IP address, make the IP address visible to all the containers, set the IP static if possible, else make it a parameter passed on during the docker run command to all containers.\
#export ROS_MASTER_URI=http://
#export ROS_IP=
#export ROS_HOSTNAME=
tmux new -s depthcam
## run roscore if running as a standalone container
#roscore
tmux split-window;                             # split the detached tmux session
tmux send 'command -t' ENTER;                  # send 2nd command 'command' to 2nd pane. I believe there's a `--target` option to target specific pane.
tmux a;                                        # open (attach) tmux session.