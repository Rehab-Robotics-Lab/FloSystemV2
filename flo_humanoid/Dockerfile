#base image from ohmnilabsvn/ohmni_ros:ohmni_ros_tbcontrol_0.0.13, preinstalled with ros-melodic + tb control ros packages
FROM ohmnilabsvn/ohmni_ros:ohmni_ros_tbcontrol_0.0.13
#make super user
RUN su
#install essential tools
RUN apt-get update -y && sudo apt-get -y install\
neovim\
tmux\
git
# clear cache
RUN apt-get clean
#switch to ohmnidev directory, used for placing code. 
WORKDIR /home/ohmnidev
RUN git clone https://github.com/Rehab-Robotics-Lab/Flo-System-2
RUN git pull https://github.com/Rehab-Robotics-Lab/Flo-System-2
RUN mkdir -p catkin_ws
WORKDIR /home/ohmnidev/catkin_ws
ARG ROS_DISTRO=melodic
ENV ROS_DISTRO="${ROS_DISTRO}"
RUN apt-get update
RUN apt-get install ros-${ROS_DISTRO}--rosserial-arduino
RUN apt-get install ros-${ROS_DISTRO}--rosserial

#add as neccessary.




