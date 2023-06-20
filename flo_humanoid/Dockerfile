FROM ohmnilabsvn/ohmni_ros:ohmni_ros_tbcontrol_0.0.13
RUN sudo apt-get update -y && sudo apt-get install -y neovim
RUN cd /home/ohmnidev
RUN git clone https://github.com/Rehab-Robotics-Lab/Flo-System-2
RUN mkdir catkin_ws
WORKDIR /home/ohmnidev/catkin_ws
ARG 
RUN sudo apt-get install ros-${ROS_DISTRO}--rosserial-arduino
RUN sudo apt-get install ros-${ROS_DISTRO}--rosserial


