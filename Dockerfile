FROM ros:noetic-ros-core

ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update && apt-get install --reinstall ca-certificates

# Fix ROS GPG key issue by removing and re-adding the repository
RUN rm -f /etc/apt/sources.list.d/ros1-latest.list
RUN apt-get update && apt-get install -y curl gnupg2
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN echo "deb http://packages.ros.org/ros/ubuntu focal main" > /etc/apt/sources.list.d/ros-latest.list

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3-pip \
    build-essential \
    cmake \
    mosquitto \
    mosquitto-clients \
    ros-noetic-dynamixel-sdk \
    ros-noetic-dynamixel-sdk-examples \
    ros-noetic-moveit \
    tmux \
    python3-rosdep \
    software-properties-common \
    # ROS Controllers (for joint_state_controller, etc.)
    ros-noetic-ros-control \
    ros-noetic-ros-controllers \
    dos2unix
    # && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y build-essential sudo terminator iproute2 gedit lsb-release lsb-core wget nano iputils-ping net-tools

# Enable universe and multiverse repositories
RUN add-apt-repository universe
RUN add-apt-repository multiverse
RUN apt-get update

# Install Gazebo and gazebo_ros
RUN apt-get update && apt-get install -y \
    gazebo11 \
    libgazebo11-dev \
    ros-noetic-gazebo-ros \
    ros-noetic-gazebo-ros-control \
    ros-noetic-gazebo-ros-pkgs \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install paho-mqtt serial numpy pyserial

# Ensure /usr/bin/python exists
RUN ln -s /usr/bin/python3 /usr/bin/python

# Setup catkin workspace
RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws/src

# # Copy your packages
# COPY flo_humanoid     /catkin_ws/src/flo_humanoid
# COPY flov2_robot_description    /catkin_ws/src/flov2_robot_description
# COPY flo_core    /catkin_ws/src/flo_core
# # COPY flo_vision          /catkin_ws/src/flo_vision

# Clone required repositories
RUN git clone --depth 1 --single-branch --branch FloV2_no_grippers \
    https://github.com/Rehab-Robotics-Lab/FloSystemV2.git

# Add top-level CMakeLists.txt
RUN echo "cmake_minimum_required(VERSION 3.0.2)\nproject(flo_v2_workspace)\nfind_package(catkin REQUIRED)\ncatkin_workspace()" > /catkin_ws/src/CMakeLists.txt
# COPY Readme.md        /catkin_ws/src/Readme.md
# COPY run_a_demo.sh /catkin_ws/run_a_demo.sh
# COPY run_a_demo_outside.sh /catkin_ws/run_a_demo_outside.sh

# Convert all .sh and .py scripts to Unix line endings
RUN find /catkin_ws -type f \( -name "*.sh" -o -name "*.py" \) -exec dos2unix {} \;


# Install workspace dependencies
WORKDIR /catkin_ws
RUN rosdep init && rosdep update

# Manually install missing packages
RUN apt-get update && apt-get install -y \
    ros-noetic-robot-state-publisher \
    ros-noetic-joint-state-publisher-gui \
    && rm -rf /var/lib/apt/lists/*

# Apriltag + camera tools
RUN apt-get update && apt-get install -y \
ros-noetic-usb-cam \
ros-noetic-image-view \
v4l-utils \
ffmpeg \
ros-noetic-apriltag-ros \
mesa-utils \
&& rm -rf /var/lib/apt/lists/*

# Install all dependencies
RUN rosdep install --from-paths src --ignore-src -y --rosdistro noetic || true

# Build workspace
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && catkin_make"

# Make Python scripts executable
RUN chmod +x /catkin_ws/src/*/scripts/*.py || true
RUN chmod +x /catkin_ws/src/FloSystemV2/*.sh

# Source environments
RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc
RUN echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc

# Entry point with optional auto-bringup (use cloned repo file)
RUN cp /catkin_ws/src/FloSystemV2/docker_entrypoint.sh /usr/local/bin/flo_entrypoint.sh \
    && chmod +x /usr/local/bin/flo_entrypoint.sh
ENTRYPOINT ["/usr/local/bin/flo_entrypoint.sh"]

# User Defined
RUN adduser user
RUN adduser user sudo
#remove password
RUN passwd -d user

USER root
