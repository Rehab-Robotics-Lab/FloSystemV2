# FLOSYSTEMV2:Gazebo Simulation Development Docker Container
# Use ROS Melodic with Ubuntu Bionic as the base image
# Author: Tian Tan & Hao Zhang,tiantan@seas.upenn.edu & shzyh@seas.upenn.edu
FROM ros:melodic-ros-base-bionic

# Install essential tools and dependencies
RUN apt-get update && apt-get install -y \
    python-rosdep \
    python-rosinstall \
    python-rosinstall-generator \
    python-wstool \
    build-essential \
    python-pip \
    git \
    vim \
    wget \
    tmux \
    ros-melodic-tf \
    ros-melodic-tf-conversions \
    ros-melodic-tf2-geometry-msgs \
    ros-melodic-gazebo-ros \
    ros-melodic-gazebo-ros-control \
    ros-melodic-gazebo-ros-pkgs \
    ros-melodic-ros-controllers \
    ros-melodic-joint-state-controller
# Install Python packages
RUN pip install numpy


# Install other necessary ROS packages
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-image-transport \
    ros-${ROS_DISTRO}-image-geometry 

# Setup the catkin workspace
RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; catkin_init_workspace /catkin_ws/src'

# # Copy package.xml files and CMakeLists.txt for dependency installation
# COPY src/test_moveit/package.xml /catkin_ws/src/test_moveit/package.xml
# COPY src/test_moveit/CMakeLists.txt /catkin_ws/src/test_moveit/CMakeLists.txt
# COPY src/flov2/package.xml /catkin_ws/src/flov2/package.xml
# COPY src/flov2/CMakeLists.txt /catkin_ws/src/flov2/CMakeLists.txt
# COPY src/flov2tag/package.xml /catkin_ws/src/flov2tag/package.xml
# COPY src/flov2tag/CMakeLists.txt /catkin_ws/src/flov2tag/CMakeLists.txt

# Copy all the package files
COPY src/ /catkin_ws/src/

COPY run_full_robot_arm_sim.sh /catkin_ws/

# Install ROS dependencies
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash && cd /catkin_ws && rosdep install --from-paths src --ignore-src -r -y"

# Build the package
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd /catkin_ws; catkin_make'

# Source the workspace
RUN echo "source /catkin_ws/devel/setup.bash" >> ~/.bashrc

# Setup the entrypoint
COPY ./ros_entrypoint.sh /
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]

# Expose ports (if necessary, e.g., for web-based visualization tools)
EXPOSE 11311


# Copy the entrypoint script
COPY ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh

# Ensure the user environment is setup
RUN echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc
