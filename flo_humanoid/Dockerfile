FROM ros:melodic-robot-bionic
#make super user
RUN su
ARG ROS_DISTRO=melodic
ENV ROS_DISTRO="$ROS_DISTRO"
#install essential tools
RUN apt-get update -y && apt-get install -y \
neovim nano \
tmux \
git \
ros-$ROS_DISTRO-catkin \
ros-$ROS_DISTRO-dynamixel-sdk \
ros-$ROS_DISTRO-dynamixel-sdk-examples

#Lidar libraries
#RUN git clone https://github.com/Slamtec/rplidar_ros.git

#Build the catkin_ws
# clear cache
RUN apt-get clean
RUN mkdir -p home/git
WORKDIR /home/git
RUN git clone https://github.com/Rehab-Robotics-Lab/FloSystemV2.git -b anh-testmotor
WORKDIR /home/git
RUN mkdir -p catkin_ws

WORKDIR /home/git/catkin_ws
RUN mkdir -p src
RUN mkdir -p flo_humanoid
RUN mkdir -p flo_humanoid_defs
RUN /ros_entrypoint.sh catkin_make

# WORKDIR /home/git/catkin_ws/src
# RUN git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
# WORKDIR /home/git/catkin_ws
# RUN /ros_entrypoint.sh catkin_make

WORKDIR /home/git
RUN cp -r FloSystemV2/flo_humanoid catkin_ws/src 
RUN cp -r FloSystemV2/flo_humanoid catkin_ws
RUN cp -r FloSystemV2/motor_control_demo catkin_ws/src

#RUN cp -r FloSystemV2/flo_humanoid_defs catkin_ws/src catkin_ws/flo_humanoid_defs
WORKDIR /home/git/catkin_ws
RUN /ros_entrypoint.sh  catkin_make -j1 -l1

USER root
RUN head -n -1 /ros_entrypoint.sh > /tmp.sh \
    && mv /tmp.sh /ros_entrypoint.sh \
    && echo 'source "/home/git/catkin_ws/devel/setup.bash"' >> /ros_entrypoint.sh \
    && echo 'exec $@' >> /ros_entrypoint.sh \
    && chmod +x /ros_entrypoint.sh

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]