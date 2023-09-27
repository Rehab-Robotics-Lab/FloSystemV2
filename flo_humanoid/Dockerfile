#base image from ohmnilabsvn/ohmni_ros:ohmni_ros_tbcontrol_0.0.13, preinstalled with ros-melodic + tb control ros packages
# FROM ohmnilabsvn/ohmni_ros:ohmni_ros_tbcontrol_0.0.13
FROM ros:melodic-robot-bionic
#make super user
RUN su
#install essential tools
RUN apt-get update -y && sudo apt-get -y install \
# neovim \
# tmux \
git 
RUN apt-get update && apt-get install -y ros-$ROS_DISTRO-catkin \
#THE following line downloads the dynamixel sdk for ros. 
ros-melodic-dynamixel-sdk\
# The following line downloads the dynamixel sdk examples for ros.
ros-melodic-dynamixel-sdk-examples
#Lidar libraries
#RUN git clone https://github.com/Slamtec/rplidar_ros.git

#Build the catkin_ws
# clear cache
RUN apt-get clean
ARG ROS_DISTRO=melodic
ENV ROS_DISTRO="$ROS_DISTRO"
#switch to ohmnidev directory, used for placing code. 
RUN mkdir -p home/git
WORKDIR /home/git
RUN git clone https://github.com/Rehab-Robotics-Lab/FloSystemV2.git
WORKDIR /home/git
RUN mkdir -p catkin_ws
RUN cp -r /FloSystemV2/flo_humanoid /catkin_ws/src catkin_ws/flo_humanoid
RUN cp -r /FloSystemV2/flo_humanoid_defs /catkin_ws/src catkin_ws/flo_humanoid_defs
WORKDIR /home/git/catkin_ws

RUN catkin_make -j1 -l1
#add as neccessary.




