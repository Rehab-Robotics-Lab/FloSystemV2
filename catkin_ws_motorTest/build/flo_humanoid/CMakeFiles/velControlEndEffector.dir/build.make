# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ajay/catkin_ws_motorTest/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ajay/catkin_ws_motorTest/build

# Include any dependencies generated for this target.
include flo_humanoid/CMakeFiles/velControlEndEffector.dir/depend.make

# Include the progress variables for this target.
include flo_humanoid/CMakeFiles/velControlEndEffector.dir/progress.make

# Include the compile flags for this target's objects.
include flo_humanoid/CMakeFiles/velControlEndEffector.dir/flags.make

flo_humanoid/CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.o: flo_humanoid/CMakeFiles/velControlEndEffector.dir/flags.make
flo_humanoid/CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.o: /home/ajay/catkin_ws_motorTest/src/flo_humanoid/src/velControlEndEffector.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ajay/catkin_ws_motorTest/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object flo_humanoid/CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.o"
	cd /home/ajay/catkin_ws_motorTest/build/flo_humanoid && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.o -c /home/ajay/catkin_ws_motorTest/src/flo_humanoid/src/velControlEndEffector.cpp

flo_humanoid/CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.i"
	cd /home/ajay/catkin_ws_motorTest/build/flo_humanoid && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ajay/catkin_ws_motorTest/src/flo_humanoid/src/velControlEndEffector.cpp > CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.i

flo_humanoid/CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.s"
	cd /home/ajay/catkin_ws_motorTest/build/flo_humanoid && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ajay/catkin_ws_motorTest/src/flo_humanoid/src/velControlEndEffector.cpp -o CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.s

# Object files for target velControlEndEffector
velControlEndEffector_OBJECTS = \
"CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.o"

# External object files for target velControlEndEffector
velControlEndEffector_EXTERNAL_OBJECTS =

/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: flo_humanoid/CMakeFiles/velControlEndEffector.dir/src/velControlEndEffector.cpp.o
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: flo_humanoid/CMakeFiles/velControlEndEffector.dir/build.make
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /opt/ros/noetic/lib/libdynamixel_sdk.so
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /opt/ros/noetic/lib/libroscpp.so
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /usr/lib/x86_64-linux-gnu/libpthread.so
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /usr/lib/x86_64-linux-gnu/libboost_chrono.so.1.71.0
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.71.0
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /opt/ros/noetic/lib/librosconsole.so
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /opt/ros/noetic/lib/librosconsole_log4cxx.so
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /opt/ros/noetic/lib/librosconsole_backend_interface.so
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /usr/lib/x86_64-linux-gnu/liblog4cxx.so
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /usr/lib/x86_64-linux-gnu/libboost_regex.so.1.71.0
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /opt/ros/noetic/lib/libroscpp_serialization.so
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /opt/ros/noetic/lib/libxmlrpcpp.so
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /opt/ros/noetic/lib/librostime.so
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /usr/lib/x86_64-linux-gnu/libboost_date_time.so.1.71.0
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /opt/ros/noetic/lib/libcpp_common.so
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /usr/lib/x86_64-linux-gnu/libboost_system.so.1.71.0
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /usr/lib/x86_64-linux-gnu/libboost_thread.so.1.71.0
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: /usr/lib/x86_64-linux-gnu/libconsole_bridge.so.0.4
/home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector: flo_humanoid/CMakeFiles/velControlEndEffector.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ajay/catkin_ws_motorTest/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable /home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector"
	cd /home/ajay/catkin_ws_motorTest/build/flo_humanoid && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/velControlEndEffector.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
flo_humanoid/CMakeFiles/velControlEndEffector.dir/build: /home/ajay/catkin_ws_motorTest/devel/lib/flo_humanoid/velControlEndEffector

.PHONY : flo_humanoid/CMakeFiles/velControlEndEffector.dir/build

flo_humanoid/CMakeFiles/velControlEndEffector.dir/clean:
	cd /home/ajay/catkin_ws_motorTest/build/flo_humanoid && $(CMAKE_COMMAND) -P CMakeFiles/velControlEndEffector.dir/cmake_clean.cmake
.PHONY : flo_humanoid/CMakeFiles/velControlEndEffector.dir/clean

flo_humanoid/CMakeFiles/velControlEndEffector.dir/depend:
	cd /home/ajay/catkin_ws_motorTest/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ajay/catkin_ws_motorTest/src /home/ajay/catkin_ws_motorTest/src/flo_humanoid /home/ajay/catkin_ws_motorTest/build /home/ajay/catkin_ws_motorTest/build/flo_humanoid /home/ajay/catkin_ws_motorTest/build/flo_humanoid/CMakeFiles/velControlEndEffector.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : flo_humanoid/CMakeFiles/velControlEndEffector.dir/depend

