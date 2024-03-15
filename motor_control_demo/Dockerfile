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
ros-$ROS_DISTRO-catkin \
ros-$ROS_DISTRO-dynamixel-sdk \
ros-$ROS_DISTRO-dynamixel-sdk-examples \
python3-tk \
python3-pip
RUN apt-get update -y
RUN pip3 install pysimpleGUI

#clear cache
RUN apt-get clean

#build catkin_ws 
RUN mkdir -p home/git
WORKDIR /home/git
#RUN git clone https://github.com/Rehab-Robotics-Lab/FloSystemV2.git
#optional command to clone specific branch, --single-branch used to avoid cloning all branches.
RUN git clone -b 2ArmJointControl --single-branch https://github.com/Rehab-Robotics-Lab/FloSystemV2.git
RUN mkdir -p catkin_ws/src
RUN cp -r FloSystemV2/flo_humanoid catkin_ws/src
RUN cp -r FloSystemV2/motor_control_demo catkin_ws/src
WORKDIR /home/git/catkin_ws

#catkin build options are j1 for single thread and l1 for load average
#this is to avoid memory issues and processor limitations on the 
#ohmni telepresence robot
#RUN catkin build -j1 -l1
RUN /ros_entrypoint.sh catkin build
# RUN catkin build
USER root
RUN head -n -1 /ros_entrypoint.sh > /tmp.sh \
    && mv /tmp.sh /ros_entrypoint.sh \
    && echo 'source "/home/git/catkin_ws/devel/setup.bash"' >> /ros_entrypoint.sh \
    && echo 'exec $@' >> /ros_entrypoint.sh \
    && chmod +x /ros_entrypoint.sh
    
WORKDIR /home/git/catkin_ws
RUN source devel/setup.bash # source the workspace
#setup connection the the remote roscore using its IP address, make the IP address visible to all the containers, set the IP static if possible, else make it a parameter passed on during the docker run command to all containers.\
#export ROS_MASTER_URI=http://
#export ROS_IP=
#export ROS_HOSTNAME=
RUN tmux new -s motor_control_demo
## run roscore if running as a standalone container
RUN roscore
RUN tmux split-window;                               
RUN rosrun flo_humanoid read_write_arm_node       # run the unilateral arm control node
RUN tmux split-window;
RUN rosrun motor_control_demo motor_control_demo_node

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]





