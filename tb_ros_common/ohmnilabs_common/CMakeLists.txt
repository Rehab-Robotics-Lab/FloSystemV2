cmake_minimum_required(VERSION 2.8.3)
project(ohmnilabs_common)
add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  visualization_msgs
  )
catkin_package(
  INCLUDE_DIRS include
  LIBRARIES ohmnilabs_common
  CATKIN_DEPENDS visualization_msgs
#  DEPENDS system_lib
)

set(PROJECT_HELPER_SOURCES
  src/helper/visualization_helper.cpp
  )

include_directories(
 include
 ${catkin_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME} ${PROJECT_HELPER_SOURCES})
target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES})

install(TARGETS
    ${PROJECT_NAME}
    ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
)

install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
)
