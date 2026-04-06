FROM ros:noetic-ros-core

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
ENV CATKIN_WS=/catkin_ws

ARG FLO_REPO_URL=https://github.com/Rehab-Robotics-Lab/FloSystemV2.git
ARG FLO_REPO_BRANCH=FloV2_no_grippers

USER root

# Re-register the ROS apt source and key before installing packages.
RUN rm -f /etc/apt/sources.list.d/ros1-latest.list /etc/apt/sources.list.d/ros-latest.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg2 \
        software-properties-common \
    && curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add - \
    && echo "deb http://packages.ros.org/ros/ubuntu focal main" > /etc/apt/sources.list.d/ros-latest.list \
    && add-apt-repository universe \
    && add-apt-repository multiverse

# Install system tools, ROS packages, Gazebo, and utilities needed by the workspace.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        dos2unix \
        ffmpeg \
        gazebo11 \
        gedit \
        git \
        iproute2 \
        iputils-ping \
        libgazebo11-dev \
        lsb-core \
        lsb-release \
        mesa-utils \
        mosquitto \
        mosquitto-clients \
        nano \
        net-tools \
        python3-pip \
        python3-rosdep \
        ros-noetic-apriltag-ros \
        ros-noetic-dynamixel-sdk \
        ros-noetic-dynamixel-sdk-examples \
        ros-noetic-gazebo-ros \
        ros-noetic-gazebo-ros-control \
        ros-noetic-gazebo-ros-pkgs \
        ros-noetic-joint-state-controller \
        ros-noetic-joint-state-publisher-gui \
        ros-noetic-joint-trajectory-controller \
        ros-noetic-moveit \
        ros-noetic-position-controllers \
        ros-noetic-robot-state-publisher \
        ros-noetic-ros-control \
        ros-noetic-ros-controllers \
        ros-noetic-usb-cam \
        ros-noetic-image-view \
        sudo \
        terminator \
        tmux \
        v4l-utils \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies used by the ROS nodes and tooling.
RUN pip3 install --upgrade \
        numpy \
        paho-mqtt \
        pyserial 

# Some legacy scripts still expect /usr/bin/python to exist.
RUN if [ ! -e /usr/bin/python ]; then ln -s /usr/bin/python3 /usr/bin/python; fi

# Create the catkin workspace and clone the project inside the image.
RUN mkdir -p ${CATKIN_WS}/src
WORKDIR ${CATKIN_WS}/src

RUN git clone --depth 1 --single-branch --branch ${FLO_REPO_BRANCH} ${FLO_REPO_URL} FloSystemV2

# Add the top-level catkin workspace file expected by catkin_make.
RUN printf '%s\n' \
    'cmake_minimum_required(VERSION 3.0.2)' \
    'project(flo_v2_workspace)' \
    'find_package(catkin REQUIRED)' \
    'catkin_workspace()' > ${CATKIN_WS}/src/CMakeLists.txt

# Normalize cloned scripts to Unix line endings before dependency resolution and build.
RUN find ${CATKIN_WS} -type f \( -name "*.sh" -o -name "*.py" \) -exec dos2unix {} \;

WORKDIR ${CATKIN_WS}

# Initialize rosdep, install package dependencies, and build the workspace.
RUN if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then rosdep init; fi \
    && rosdep update \
    && rosdep install --from-paths src --ignore-src -r -y --rosdistro noetic || true \
    && source /opt/ros/noetic/setup.bash \
    && catkin_make

# Make script entry points executable and prepare the default shell environment.
RUN chmod +x ${CATKIN_WS}/src/*/scripts/*.py || true \
    && chmod +x ${CATKIN_WS}/src/FloSystemV2/*.sh \
    && echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc \
    && echo "source ${CATKIN_WS}/devel/setup.bash" >> /root/.bashrc \
    && cp ${CATKIN_WS}/src/FloSystemV2/docker_entrypoint.sh /usr/local/bin/flo_entrypoint.sh \
    && chmod +x /usr/local/bin/flo_entrypoint.sh

ENTRYPOINT ["/usr/local/bin/flo_entrypoint.sh"]

# Keep a passwordless sudo-capable user available for interactive work.
RUN adduser --disabled-password --gecos "" user \
    && adduser user sudo \
    && passwd -d user

USER root
