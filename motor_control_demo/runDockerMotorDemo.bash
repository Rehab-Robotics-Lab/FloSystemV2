docker build ./ -t ajyanand/motor_control_demo:latest
docker container prune -f
xhost +
docker run -it --privileged --name flo_v2_motor_control_demo --device=/dev/ttyUSB0 --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ajyanand/motor_control_demo:latest
xhost -
### error trackback 
# File "/usr/lib/python3.6/tkinter/__init__.py", line 2023, in __init__
#     self.tk = _tkinter.create(screenName, baseName, className, interactive, wantobjects, useTk, sync, use)
# _tkinter.TclError: no display name and no $DISPLAY environment variable
###