docker container prune -f
xhost +
docker run -it --rm --name  gazebo_simulation --device=/dev/ttyUSB0 --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --privileged  gazebo_simulation tmux
xhost -
