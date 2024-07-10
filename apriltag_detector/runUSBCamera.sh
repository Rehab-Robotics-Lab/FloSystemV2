source devel/setup.bash
chmod +x runUSBCamera.sh
rosrun usb_cam usb_cam_node _video_device:=/dev/video0 _pixel_format:=yuyv _image_width:=640 _image_height:=480 _framerate:=30 _io_method:=mmap