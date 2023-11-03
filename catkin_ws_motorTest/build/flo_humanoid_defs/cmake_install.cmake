# Install script for directory: /home/ajay/catkin_ws_motorTest/src/flo_humanoid_defs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/ajay/catkin_ws_motorTest/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/flo_humanoid_defs/msg" TYPE FILE FILES
    "/home/ajay/catkin_ws_motorTest/src/flo_humanoid_defs/msg/SetJointPosition.msg"
    "/home/ajay/catkin_ws_motorTest/src/flo_humanoid_defs/msg/SetJointPositions.msg"
    "/home/ajay/catkin_ws_motorTest/src/flo_humanoid_defs/msg/SetJointVelocity.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/flo_humanoid_defs/srv" TYPE FILE FILES
    "/home/ajay/catkin_ws_motorTest/src/flo_humanoid_defs/srv/GetJointPosition.srv"
    "/home/ajay/catkin_ws_motorTest/src/flo_humanoid_defs/srv/GetJointPositions.srv"
    "/home/ajay/catkin_ws_motorTest/src/flo_humanoid_defs/srv/GetJointVelocity.srv"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/flo_humanoid_defs/cmake" TYPE FILE FILES "/home/ajay/catkin_ws_motorTest/build/flo_humanoid_defs/catkin_generated/installspace/flo_humanoid_defs-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/ajay/catkin_ws_motorTest/devel/include/flo_humanoid_defs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/ajay/catkin_ws_motorTest/devel/share/roseus/ros/flo_humanoid_defs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/ajay/catkin_ws_motorTest/devel/share/common-lisp/ros/flo_humanoid_defs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/ajay/catkin_ws_motorTest/devel/share/gennodejs/ros/flo_humanoid_defs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/ajay/catkin_ws_motorTest/devel/lib/python3/dist-packages/flo_humanoid_defs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/ajay/catkin_ws_motorTest/devel/lib/python3/dist-packages/flo_humanoid_defs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/ajay/catkin_ws_motorTest/build/flo_humanoid_defs/catkin_generated/installspace/flo_humanoid_defs.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/flo_humanoid_defs/cmake" TYPE FILE FILES "/home/ajay/catkin_ws_motorTest/build/flo_humanoid_defs/catkin_generated/installspace/flo_humanoid_defs-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/flo_humanoid_defs/cmake" TYPE FILE FILES
    "/home/ajay/catkin_ws_motorTest/build/flo_humanoid_defs/catkin_generated/installspace/flo_humanoid_defsConfig.cmake"
    "/home/ajay/catkin_ws_motorTest/build/flo_humanoid_defs/catkin_generated/installspace/flo_humanoid_defsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/flo_humanoid_defs" TYPE FILE FILES "/home/ajay/catkin_ws_motorTest/src/flo_humanoid_defs/package.xml")
endif()

