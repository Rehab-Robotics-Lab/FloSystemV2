# FLOSYSTEMV2:Docker Commnication Development Docker Container
# Use ROS Melodic with Ubuntu Bionic as the base image
# Author: Tian Tan,tiantan@seas.upenn.edu
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
    ros-melodic-tf2-geometry-msgs 
# Install Python packages
RUN pip install numpy

# Install OpenCV and dependencies for image processing
RUN apt-get update && apt-get install -y \
    python-opencv \
    libopencv-dev 

# Install other necessary ROS packages
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-cv-bridge \
    ros-${ROS_DISTRO}-image-transport \
    ros-${ROS_DISTRO}-image-geometry \
    ros-${ROS_DISTRO}-usb-cam

# Setup the catkin workspace
RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; catkin_init_workspace /catkin_ws/src'

# Copy ROS package into the workspace
COPY . /catkin_ws/src/apriltag_detector

# Copy individual .sh files to their intended locations

COPY run_subscriber.sh /catkin_ws/

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

# Additional dependencies for AprilTag and its Python bindings
RUN pip install apriltag

# Copy the entrypoint script
COPY ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh

# Ensure the user environment is setup
RUN echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc
