Flo_vision is the part control the camera and detecting the Apriltag.

The core function here is /script/Apriltag_detect. It mainly publishes these vital ros msg:

* /apriltag_poses: contain **Position** and **Orientation** information(**geometry_msgs/Pose**)
  position:
  x: 0.234
  y: -0.156
  z: 0.892
* /apriltag_info
