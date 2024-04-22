ARG ROS_DISTRO=melodic
ENV ROS_DISTRO="$ROS_DISTRO"

source /opt/ros/$ROS_DISTRO/setup.bash
roslaunch rosbridge_server rosbridge_websocket.launch