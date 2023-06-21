FROM ros:melodic-ros-core-bionic

# install ros packages
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-ros-base=1.4.1-0*

# install ROS essential dependencies
# RUN apt-get update && apt-get install -y \
#     ros-${ROS_DISTRO}-tf2 \
#     ros-${ROS_DISTRO}-tf2-ros \
#     ros-${ROS_DISTRO}-tf2-geometry-msgs && \
#     # clear cache
#     apt-get clean

# install essential tools
RUN apt-get update && apt-get -y install \
    vim \
    net-tools \
    tmux \
    wget \
    htop && \
    # clear cache
    apt-get clean

# OpenCV built default with ROS melodic, version: 3.2.0
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-cv-bridge \
    ros-${ROS_DISTRO}-image-transport \
    ros-${ROS_DISTRO}-image-transport-plugins && \
    # clear cache
    apt-get clean

#for http://wiki.ros.org/usb_cam
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-usb-cam && \
    # clear cache
    apt-get clean

#for http://wiki.ros.org/libuvc_camera
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-libuvc-camera && \
    # clear cache
    apt-get clean

#for http://wiki.ros.org/gscam
RUN apt-get update && apt-get install -y \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-good \
    libgstreamer1.0-dev \ 
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-good1.0-dev  && \
    # clear cache
    apt-get clean

RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-gscam && \
    # clear cache
    apt-get clean

