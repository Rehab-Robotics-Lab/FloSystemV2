FROM ros:melodic-robot-bionic
#make super user
RUN su
ARG ROS_DISTRO=melodic
ENV ROS_DISTRO="$ROS_DISTRO"
#install essential tools
RUN apt-get update -y && apt-get install -y \
neovim \
tmux \
git \
ros-$ROS_DISTRO-catkin 

#Build the catkin_ws
# clear cache
RUN apt-get clean
 
RUN mkdir -p home/git
WORKDIR /home/git
RUN git clone https://github.com/Rehab-Robotics-Lab/FloSystemV2.git
WORKDIR /home/git
# RUN mkdir -p catkin_ws
# RUN cp -r /FloSystemV2/flo_humanoid /catkin_ws/src catkin_ws/flo_humanoid
# RUN cp -r /FloSystemV2/flo_humanoid_defs /catkin_ws/src catkin_ws/flo_humanoid_defs
# WORKDIR /home/git/catkin_ws
# RUN catkin_make -j1 -l1

# ENTRYPOINT ["./ros_entrypoint.sh"]
# CMD ["bash"]





