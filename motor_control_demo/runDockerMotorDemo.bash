docker build ./ -t ajyanand/motor_control_demo:latest
docker run -it --privileged --device=/dev/ttyUSB0 --net=host -e DISPLAY=:1 -v /tmp/.X11-unix:/tmp/.X11-unix:rw ajyanand/motor_control_demo:latest

