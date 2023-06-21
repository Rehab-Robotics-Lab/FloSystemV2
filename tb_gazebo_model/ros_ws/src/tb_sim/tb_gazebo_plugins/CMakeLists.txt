cmake_minimum_required(VERSION 2.8.3)
project(tb_gazebo_plugins)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  gazebo_dev
  sensor_msgs

#  gazebo_dev
#  message_generation
#  gazebo_msgs
#  roscpp
#  rospy
#  nodelet
#  angles
#  std_srvs
#  geometry_msgs
#  sensor_msgs
#  nav_msgs
#  urdf
#  tf
#  tf2_ros
#  dynamic_reconfigure
#  rosgraph_msgs
#  trajectory_msgs
#  image_transport
#  rosconsole
#  cv_bridge
#  polled_camera
#  diagnostic_updater
#  camera_info_manager
#  std_msgs
  )

find_package(gazebo REQUIRED)

link_directories(${GAZEBO_LIBRARY_DIRS})
include_directories(
  include
  ${Boost_INCLUDE_DIR}
  ${catkin_INCLUDE_DIRS}
  ${GAZEBO_INCLUDE_DIRS})

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES
#  CATKIN_DEPENDS gazebo_ros roscpp
#  DEPENDS system_lib
)

add_library(tb_gazebo_ros_servo_pos_drive src/gazebo_ros_servo_pos_drive.cpp)
target_link_libraries(tb_gazebo_ros_servo_pos_drive ${catkin_LIBRARIES} ${Boost_LIBRARIES})
