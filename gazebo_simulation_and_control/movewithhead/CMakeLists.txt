cmake_minimum_required(VERSION 3.1.3)
project(movewithhead)

## 找到catkin的包
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  moveit_ros_planning_interface  # <-- Replaces moveit_commander
)


catkin_package()

## 安装launch和config目录
install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN "setup_assistant.launch" EXCLUDE)
install(DIRECTORY config DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

## 安装Python脚本
install(PROGRAMS
  script/test.py
  script/testnew.py
  script/sendJointValue.py
  script/getPosition.py
  script/dualPosition.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


## 确保安装路径中的Python解释器
find_package(PythonInterp 3 REQUIRED)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
## Tian updated
add_executable(dummy_node src/dummy_node.cpp)
target_link_libraries(dummy_node ${catkin_LIBRARIES})

