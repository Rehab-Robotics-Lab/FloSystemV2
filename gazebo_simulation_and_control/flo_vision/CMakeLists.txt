cmake_minimum_required(VERSION 2.8.3)

project(flo_vision)

find_package(catkin REQUIRED)

catkin_package()

find_package(roslaunch)

# Install Python scripts
catkin_install_python(PROGRAMS
  scripts/Apriltag_detect.py
  test/apriltag_pose_subscriber.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)
