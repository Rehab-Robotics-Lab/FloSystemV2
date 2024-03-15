docker build ./ -t ajyanand/motor_control_demo:latest
docker run -it --privileged --device=/dev/ttyUSB0 ajyanand/motor_control_demo:latest
# --net=host --env="DISPLAY" 
