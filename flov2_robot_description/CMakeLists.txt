cmake_minimum_required(VERSION 2.8.12)

project(flov2_robot_description)



find_package(catkin REQUIRED COMPONENTS
    message_generation
    roscpp
    rospy
    std_msgs
    geometry_msgs
    urdf
    xacro
    robot_state_publisher
    joint_state_publisher
    joint_state_publisher_gui
    rviz
	roslaunch
	gazebo_ros
	tf
	controller_manager
)

catkin_package(CATKIN_DEPENDS
    geometry_msgs
    roscpp
    rospy
    std_msgs
    robot_state_publisher
    joint_state_publisher
    rviz
    joint_state_publisher_gui
)

foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)
