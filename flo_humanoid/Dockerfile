#base image from ohmnilabsvn/ohmni_ros:ohmni_ros_tbcontrol_0.0.13, preinstalled with ros-melodic + tb control ros packages
FROM ohmnilabsvn/ohmni_ros:ohmni_ros_tbcontrol_0.0.13
#make super user
RUN su
#install essential tools
RUN apt-get update -y && sudo apt-get -y install \
neovim \
tmux \
git 
# clear cache
RUN apt-get clean
#switch to ohmnidev directory, used for placing code. 
WORKDIR /home/ohmnidev
RUN git clone https://github.com/Rehab-Robotics-Lab/FloSystemV2.git
WORKDIR /home/ohmnidev/FloSystemV2
RUN git pull
WORKDIR /home/ohmnidev
RUN mkdir -p catkin_ws
WORKDIR /home/ohmnidev/catkin_ws
ARG ROS_DISTRO=melodic
ENV ROS_DISTRO="$ROS_DISTRO"
RUN apt-get update && apt-get install -y ros-$ROS_DISTRO-catkin \
ros-$ROS_DISTRO-rosserial \
ros-$ROS_DISTRO-rosserial-arduino
#RUN git clone https://github.com/Slamtec/rplidar_ros.git
#RUN catkin_make -j1 -l1


#add as neccessary.




