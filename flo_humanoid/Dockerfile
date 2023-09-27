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
# clear cache
RUN apt-get clean
#switch to ohmnidev directory, used for placing code. 
RUN mkdir -p home/git
WORKDIR /home/git/FloSystemV2
RUN git clone https://github.com/Rehab-Robotics-Lab/FloSystemV2.git
RUN git pull
WORKDIR /home/git
RUN mkdir -p catkin_ws
WORKDIR /home/git/catkin_ws
ARG ROS_DISTRO=melodic
ENV ROS_DISTRO="$ROS_DISTRO"
RUN apt-get update && apt-get install -y ros-$ROS_DISTRO-catkin \
#install usb utilities to get info on connected devices - might not be as useful. comment next line if not needed.
#usbutils\
#The following 2 lines download libraries for control of arduino via ros
#ros-$ROS_DISTRO-rosserial \
#ros-$ROS_DISTRO-rosserial-arduino\
#THE following line downloads the dynamixel sdk for ros. 
# ros-melodic-dynamixel-sdk\
#The following line downloads the dynamixel sdk examples for ros.
# ros-melodic-dynamixel-sdk-examples
#Lidar libraries
#RUN git clone https://github.com/Slamtec/rplidar_ros.git
#Build the catkin_ws
RUN catkin_make -j1 -l1
#add as neccessary.




