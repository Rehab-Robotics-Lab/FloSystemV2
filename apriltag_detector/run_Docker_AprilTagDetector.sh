docker container prune -f
xhost +
docker run -it --rm --name  apriltag_detector --device=/dev/ttyUSB0 --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --privileged  apriltag_detector
xhost -
