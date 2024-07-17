docker container prune -f
xhost +
docker run -it --rm --name  docker_communication  --device=/dev/ttyUSB0 --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --privileged  docker_communication  tmux
xhost -
