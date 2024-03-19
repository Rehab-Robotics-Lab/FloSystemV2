docker container prune -f
xhost +
docker run -it --privileged --name flo_v2_motor_control_demo --device=/dev/ttyUSB0 --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ajyanand/motor_control_demo:latest
xhost -
