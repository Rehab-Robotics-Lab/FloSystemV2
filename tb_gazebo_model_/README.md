# tb-simulation
This is a workspace for Ohmnilabs robot simulation. This simulation built to support the development of the Ohmnilabs autonomy stack
![tb-simulation](docs/figures/tb_simulation.png)

Currently, in this simulation includes:
* KOLVN office model with texture and material for RGB camera. This model is constructed by Sketchup, adding material and texture mapping using Blender
* Sensor plugins: depth camera, navigation camera, telepresence camera, IMU, laser range sensor
* Actuator plugins: differential drive, neck servo

## Prerequisites
* Ubuntu 18.04
* [ROS Melodic](http://wiki.ros.org/melodic/Installation/Ubuntu) : recommend install ros-melodic-desktop-full
* [Gazebo 9.10.0](http://gazebosim.org/tutorials?tut=install_ubuntu&cat=install#Defaultinstallation:one-liner): Or you could use the default installed version (9.0.0) with the above ROS install. 
There was an issue make me update to Gazebo 9.10.0, but I forgot why @@. Let me know if you could run this simulation on the default version.
* A graphics card to support graphic rendering. I use NVIDIA Quadro M2200, enough to run this simulation smoothly

Will port to Ubuntu 16 if requested

## Installation
Open terminal and clone package

```
~..$  git clone https://gitlab.com/ohmni-sdk/tb_gazebo_model.git tb-simulation
```
Install with catkin_make
```
~..$ cd tb-simulation/ros_ws
~../tb-simulation/ros_ws$ catkin_make 
```

Note that, during installation, these are some errors caused by missing packages, please install it with **apt** and report the issue [here](https://gitlab.com/ohmni-sdk/tb_gazebo_model/-/issues) if you found any. 
Potential missing packages:
```
~$ sudo apt install ros-melodic-gazebo-plugins ros-melodic-rqt-robot-steering ros-melodic-rviz-imu-plugin ros-melodic-joint-state-publisher-gui
```
## Basic Usage
Run the visualization Rviz to display the ohmnibots model
```
~../tb-simulation/ros_ws$ source devel/setup.bash
~../tb-simulation/ros_ws$ roslaunch tb_description test_tb_rviz.launch
```

Run full simulation environment
```
~../tb-simulation/ros_ws$ source devel/setup.bash
~../tb-simulation/ros_ws$ roslaunch gazebo_environment empty.launch
### or run with office models 
~../tb-simulation/ros_ws$ roslaunch gazebo_environment testbed_kolvn_office.launch
~../tb-simulation/ros_ws$ roslaunch gazebo_environment willowgarage.launch
```
Using Rviz to visualize sensor data. Control robot speed (linear and angular) with /tb_cmd_vel, robot neck position with /tb_sim/cmd_pos

## Improvement
Note that this package is under development. Improvement:
* Simplify mesh file to make this simulation lighter
* Tunning texture, material, light sources to make it more realistic
* Correcting link inertia tensor: using 3rd software such as Meshlab, Soilworks, Fusion360 by adding correct material density. Currently, I estimate it bases on the mass and size of each link
* Tunning sensor model to get nearly matching with real-hardware
* Adding skin for robot
* Add charging dock, more furniture, landmark

