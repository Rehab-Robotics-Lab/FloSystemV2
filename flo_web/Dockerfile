#use melodic robot bionic base image from ROS foundation 
FROM ros:melodic-robot-bionic

#make super user
RUN su

#set environment variable
ARG ROS_DISTRO=melodic
ENV ROS_DISTRO="$ROS_DISTRO"

#install essential tools
RUN apt-get update -y && apt-get install -y \
neovim \
tmux \
git \
python3 \
python3-catkin-tools \
ros-$ROS_DISTRO-catkin\
ros-$ROS_DISTRO-rosbridge-suite

#clear cache
RUN apt-get clean


ENTRYPOINT ["./ros_entrypoint.sh"]
CMD ["bash"]





