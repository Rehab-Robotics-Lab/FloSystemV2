source devel/setup.bash 
#setup connection the the remote roscore using its IP address, make the IP address visible to all the containers, set the IP static if possible, else make it a parameter passed on during the docker run command to all containers.\
#export ROS_MASTER_URI=http://
#export ROS_IP=
#export ROS_HOSTNAME=
tmux new -s motor_control_demo
## run roscore if running as a standalone container
roscore
tmux split-window;                               
rosrun flo_humanoid read_write_arm_node       # run the unilateral arm control node
tmux split-window;
rosrun motor_control_demo motor_control_demo_node