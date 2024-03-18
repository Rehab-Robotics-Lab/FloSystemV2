 FROM ros:melodic-robot-bionic

#This is bad practice (can lead to security vulnerabilities and dependancy issues)
#changed shell to bash where required in entrypoint or cmd.
#SHELL ["/bin/bash", "-c"]

#Make super user 
#This is also bad practice, replace once docker compose setup is complete
RUN su


#these argscome in from docker compose.yml, defined by the corresponding variables in the host env.
ARG ROS_USER=floV2
ENV ROS_USER="${ROS_USER}"

# ARG R_GID
# ENV R_GID="${R_GID}"
# ARG R_UID
# ENV R_UID="${R_UID}"

# RUN echo "$ROS_USER"    

# RUN useradd -m $ROS_USER && \
#         echo "$ROS_USER:$ROS_USER" | chpasswd && \
#         usermod --shell /bin/bash $ROS_USER && \
#         usermod -aG sudo $ROS_USER && \
#         echo "$ROS_USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$ROS_USER && \
#         chmod 0440 /etc/sudoers.d/$ROS_USER && \
#         # Replace 1000 with your user/group id
#         usermod  --uid $R_UID $ROS_USER && \
#         groupmod --gid $R_GID $ROS_USER

#set environment variable for ROS distro
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
ros-$ROS_DISTRO-rospy \
python3-tk \
python3-pip \
python3-rospkg
RUN apt-get update -y
RUN pip3 install pysimpleGUI

#clear cache
RUN apt-get clean

#build catkin_ws
RUN mkdir /home/$ROS_USER/catkin_ws/src -p
# RUN chown -R $ROS_USER /home/$ROS_USER

# USER $ROS_USER

WORKDIR /home/$ROS_USER
#RUN git clone https://github.com/Rehab-Robotics-Lab/FloSystemV2.git
#optional command to clone specific branch, --single-branch used to avoid cloning all branches.
RUN git clone -b 2ArmJointControl --single-branch https://github.com/Rehab-Robotics-Lab/FloSystemV2.git
WORKDIR /home/$ROS_USER/FloSystemV2
RUN git pull
WORKDIR /home/$ROS_USER
RUN cp -r FloSystemV2/flo_humanoid catkin_ws/src
RUN cp -r FloSystemV2/motor_control_demo catkin_ws/src
WORKDIR /home/$ROS_USER/catkin_ws

#catkin build options are j1 for single thread and l1 for load average
#this is to avoid memory issues and processor limitations on the 
#ohmni telepresence robot
#RUN catkin build -j1 -l1
RUN /ros_entrypoint.sh catkin build
# RUN catkin build
USER root
RUN head -n -1 /ros_entrypoint.sh > /tmp.sh \
    && mv /tmp.sh /ros_entrypoint.sh \
    && echo 'source "/home/$ROS_USER/catkin_ws/devel/setup.bash"' >> /ros_entrypoint.sh \
    && echo 'exec $@' >> /ros_entrypoint.sh \
    && chmod +x /ros_entrypoint.sh

RUN su

#USER $ROS_USER
WORKDIR /home/$ROS_USER/catkin_ws/src/motor_control_demo
# RUN ./runMotorDemo.bash

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]





