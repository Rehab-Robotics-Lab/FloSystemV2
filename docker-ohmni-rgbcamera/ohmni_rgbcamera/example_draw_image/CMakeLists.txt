cmake_minimum_required(VERSION 2.8.3)
project(example_draw_image)

## Compile as C++11, supported in ROS Kinetic and newer
#add_compile_options(-std=c++11)

FIND_PACKAGE(OpenCV REQUIRED)
find_package(catkin REQUIRED
  roscpp
  image_transport
  cv_bridge
  )

catkin_package(
  #  INCLUDE_DIRS include
  #  LIBRARIES render_test
  #  CATKIN_DEPENDS other_catkin_pkg
  #  DEPENDS system_lib
  )

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
  )

add_executable(example_draw_image src/example_draw_image.cpp)
target_link_libraries(example_draw_image ${catkin_LIBRARIES} ${OpenCV_LIBS})

