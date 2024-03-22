FROM ros:noetic-robot-focal
#make super user (running all commands as root)
#might want to fix that later for security and to make sure we don't mess up the ros user.
RUN su
ARG ROS_DISTRO=noetic
ENV ROS_DISTRO="$ROS_DISTRO"
ARG ROS_USER=flov2_cam
#install essential tools
RUN apt-get update -y && apt-get install -y \
neovim \
tmux \
git \
ros-$ROS_DISTRO-catkin \
#install the depthai ros package for the luxonis oak-d depth camera
ros-<distro>-depthai-ros

#set udev rules for the luxonis oak-d lite depth camera to make it mounts at the correct location.
# we do not need to use the serial number of the actual device as we only plan to use 1 camera.
RUN echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
RUN udevadm control --reload-rules && sudo udevadm trigger


#Build the catkin_ws
# clear cache
RUN apt-get clean
 
RUN mkdir -p home/$ROS_USER/git
WORKDIR  home/$ROS_USER/git
RUN git clone https://github.com/Rehab-Robotics-Lab/FloSystemV2.git
RUN git clone --branch noetic https://github.com/luxonis/depthai-ros.git
WORKDIR /home/git
RUN mkdir -p catkin_ws
RUN cp -r /FloSystemV2/flo_humanoid /catkin_ws/src catkin_ws/flo_humanoid
RUN cp -r /FloSystemV2/flo_humanoid_defs /catkin_ws/src catkin_ws/flo_humanoid_defs

WORKDIR /home/git/catkin_ws
RUN catkin_make -j1 -l1

COPY ros_entrypoint.sh ros_entrypoint.sh

ENTRYPOINT ["./ros_entrypoint.sh"]
CMD ["bash"]