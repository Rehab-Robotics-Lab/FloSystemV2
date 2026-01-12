cmake_minimum_required(VERSION 3.1.3)
project(flo_core)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  moveit_ros_planning_interface
)

## Use Python setup for proper package install
find_package(PythonInterp 3 REQUIRED)
find_package(PythonLibs 3 REQUIRED)

# Python helper – lets `setup.py` install modules and scripts
catkin_python_setup()

## Declare a catkin package
catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs moveit_ros_planning_interface
)

## Include directories
include_directories(
  ${catkin_INCLUDE_DIRS}
)

## Ensure Python package directory contains __init__.py
# (Make sure src/flo_core/__init__.py exists.)

## Install Python library modules
install(DIRECTORY src/flo_core/
  DESTINATION ${CATKIN_PACKAGE_PYTHON_DESTINATION}/flo_core
  FILES_MATCHING PATTERN "*.py"
)

## Install Python executables
catkin_install_python(PROGRAMS
  scripts/mqtt_control_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

## Install launch and config directories
install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)
install(DIRECTORY config/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/config
)

