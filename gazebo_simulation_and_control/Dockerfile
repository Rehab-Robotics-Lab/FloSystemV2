FROM ros:noetic-ros-core

ENV DEBIAN_FRONTEND=noninteractive

USER root



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

RUN apt-get install -y build-essential sudo terminator iproute2 gedit lsb-release lsb-core wget nano

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
RUN pip3 install paho-mqtt

# Ensure /usr/bin/python exists
RUN ln -s /usr/bin/python3 /usr/bin/python

# Setup catkin workspace
RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws/src

# Copy your packages
COPY flo_humanoid     /catkin_ws/src/flo_humanoid
COPY flov2withhead    /catkin_ws/src/flov2withhead
COPY movewithhead     /catkin_ws/src/movewithhead
COPY camera           /catkin_ws/src/camera

# Add top-level CMakeLists.txt
RUN echo "cmake_minimum_required(VERSION 3.0.2)\nproject(flo_v2_workspace)\nfind_package(catkin REQUIRED)\ncatkin_workspace()" > /catkin_ws/src/CMakeLists.txt
COPY Readme.md        /catkin_ws/src/Readme.md
COPY run_a_demo.sh /catkin_ws/run_a_demo.sh
COPY run_a_demo_outside.sh /catkin_ws/run_a_demo_outside.sh

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

# Install all dependencies
RUN rosdep install --from-paths src --ignore-src -y --rosdistro noetic || true

# Build workspace
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && catkin_make"

# Make Python scripts executable
RUN chmod +x /catkin_ws/src/*/script/*.py || true

# Source environments
RUN echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc
RUN echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc

# Default command
CMD ["/bin/bash", "-c", "source /opt/ros/noetic/setup.bash && source /catkin_ws/devel/setup.bash && /bin/bash"]

# User Defined
RUN adduser user
RUN adduser user sudo
#remove password
RUN passwd -d user

USER user