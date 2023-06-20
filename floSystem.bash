image=flosystem/ohmni_ros:ohmni_ros_tbcontrol_0.0.13_mod
docker run -it --network host --privileged -v /dev:/dev -v /var/dockerhome:/home/ohmnidev $image