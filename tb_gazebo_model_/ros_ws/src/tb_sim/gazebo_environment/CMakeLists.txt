cmake_minimum_required(VERSION 2.8.3)
project(gazebo_environment)

find_package(catkin REQUIRED COMPONENTS
    # rospy
    # std_msgs
  )

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES factory_gazebo
#  CATKIN_DEPENDS other_catkin_pkg
#  DEPENDS system_lib
)

include_directories(
# include
# ${catkin_INCLUDE_DIRS}
)
