################################################################################
# Set minimum required version of cmake, project name and compile options
################################################################################
cmake_minimum_required(VERSION 2.8.12)
project(flo_humanoid)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)

################################################################################
# Find catkin packages and libraries for catkin and system dependencies
################################################################################
find_package(catkin REQUIRED
  COMPONENTS
    actionlib
    actionlib_msgs
    control_msgs
    dynamixel_sdk
    message_generation
    message_runtime
    roscpp
    rospack
    sensor_msgs
    std_msgs
    trajectory_msgs
)

################################################################################
# Declare ROS messages, services and actions
################################################################################
add_message_files(
  FILES
    SetJointPosition.msg
    SetJointPositions.msg
    SetArmsJointPositions.msg
)

add_service_files(
  FILES
    GetJointPosition.srv
    GetJointPositions.srv
    GetArmsJointPositions.srv
)

generate_messages(
  DEPENDENCIES
    actionlib_msgs
    sensor_msgs
    std_msgs
    trajectory_msgs
)

################################################################################
# Declare catkin specific configuration to be passed to dependent projects
################################################################################
catkin_package(
  CATKIN_DEPENDS
    actionlib
    actionlib_msgs
    control_msgs
    dynamixel_sdk
    message_generation
    message_runtime
    roscpp
    sensor_msgs
    std_msgs
    trajectory_msgs
)

################################################################################
# Build
################################################################################
include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(read_write_arms_node src/readWriteArms.cpp)
add_dependencies(read_write_arms_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(read_write_arms_node ${catkin_LIBRARIES})

################################################################################
# Install
################################################################################
install(TARGETS
  read_write_arms_node
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(PROGRAMS
  scripts/joint_state_to_dual_arm_motors.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
