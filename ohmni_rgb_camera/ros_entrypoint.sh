#!/bin/bash
set -e

echo "setup ros environment"
source "/opt/ros/$ROS_DISTRO/setup.bash"

echo "launch basic nodes"
source /ros_launch.sh

#echo "Testing: restarting udev, does it work?"
#service udev reload
#service udev restart

exec "$@"
