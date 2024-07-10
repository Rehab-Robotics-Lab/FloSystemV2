#!/bin/bash
set -e

# Source the ROS environment
source "/opt/ros/$ROS_DISTRO/setup.bash"
source "/catkin_ws/devel/setup.bash"

# Execute the command provided as arguments to this script
exec "$@"
