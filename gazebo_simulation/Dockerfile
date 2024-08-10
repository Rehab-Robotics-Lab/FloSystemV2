# FLOSYSTEMV2:Gazebo Simulation Development Docker Container
# Use ROS Noetic with Ubuntu Focal as the base image
# Author: Tian Tan & Hao Zhang, tiantan@seas.upenn.edu & shzyh@seas.upenn.edu
FROM ros:noetic-ros-base-focal

# Install essential tools and dependencies
RUN apt-get update && apt-get install -y \
    python3-rosdep \
    python3-rosinstall \
    python3-rosinstall-generator \
    python3-wstool \
    build-essential \
    python3-pip \
    git \
    vim \
    wget \
    tmux \
    python3 \
    ros-noetic-tf \
    ros-noetic-tf-conversions \
    ros-noetic-tf2-geometry-msgs \
    ros-noetic-gazebo-ros \
    ros-noetic-gazebo-ros-control \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-ros-controllers \
    ros-noetic-joint-state-controller \
    python3-tk \
    tk-dev \
    mosquitto \
    mosquitto-clients

# Install Python packages
RUN pip3 install numpy
RUN pip install paho-mqtt==1.5.1
RUN pip3 install paho-mqtt==1.5.1

# Install other necessary ROS packages
RUN apt-get update && apt-get install -y \
    ros-noetic-image-transport \
    ros-noetic-image-geometry 

# Setup the catkin workspace
RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws
RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; catkin_init_workspace /catkin_ws/src'

# Copy all the package files
COPY src/ /catkin_ws/src/

COPY run_full_robot_arm_sim.sh /catkin_ws/

# Install ROS dependencies
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && cd /catkin_ws && rosdep install --from-paths src --ignore-src -r -y"

# Build the package
RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; cd /catkin_ws; catkin_make'

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
