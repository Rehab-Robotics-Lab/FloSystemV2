docker build ./ -t ajyanand/motor_control_demo:latest
docker run -it --privileged --device=/dev/ttyUSB0 --net=host --env="DISPLAY" ajyanand/motor_control_demo:latest

