FROM ros:melodic-ros-core-bionic

# install ros packages
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-ros-base=1.4.1-0*

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

COPY launch/* /
COPY ros_launch.sh /
COPY ros_entrypoint.sh /

#Build an example
RUN mkdir -p root/catkin_ws/src
COPY example_draw_image root/catkin_ws/src/example_draw_image
RUN /bin/bash -c ' source /opt/ros/melodic/setup.bash; cd root/catkin_ws\
    ;catkin_make -DCATKIN_WHITELIST_PACKAGES="example_draw_image" -DCMAKE_BUILD_TYPE=Release'
 
#start core nodes
ENTRYPOINT ["./ros_entrypoint.sh"]
CMD ["bash"]
