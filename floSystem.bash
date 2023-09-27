mkdir -p mnt/nvmeStorage
mount dev/block/sda1 mnt/nvmeStorage
image=flosystem/ohmni_ros:ohmni_ros_tbcontrol_0.0.13_mod
docker run -it -d --name flo_system --network host --privileged -v /dev:/dev -v /var/dockerhome:/home/ohmnidev $image