echo "checking if external storage is connected"
if test -f dev/block/sda1; then
  echo "Nvme Storage is connected, mounting at mnt/nvmeStorage"
  mkdir -p mnt/nvmeStorage
  mount dev/block/sda1 mnt/nvmeStorage
else
    echo "Nvme Storage is not connected"  
fi
#remove all stopped containers, along with any networks not used by at least one container, all dangling images, and all build cache. 
echo "Pruning docker system"
docker system prune -f
echo "Starting flo_system container"
# image=ohmnilabsvn/ohmni_ros:ohmni_ros_tbcontrol_0.0.13
image=flosystem/ohmni_ros:ohmni_ros_tbcontrol_0.0.13_mod
docker run -it -d --name flo_system --network host --privileged -v /dev:/dev -v /var/dockerhome:/home/ohmnidev $image