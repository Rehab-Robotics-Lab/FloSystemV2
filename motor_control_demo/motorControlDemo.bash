docker build ./ -t ajyanand/motor_control_demo:latest
docker run -it --privileged --device=/dev/ttyUSB0 --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" ajyanand/motor_control_demo:latest

