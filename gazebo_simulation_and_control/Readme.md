## Flo V2 Quickstart Instructions(Tian)

### 1. Build & Run Docker
---------------------
Run the script to build the Docker image and start a new container:
```bash
 ./run_docker.sh
```
This removes any old container named flo_v2_container, builds flo_v2_image, and runs it.

### 2. Run a Demo Action
--------------------
Inside the Docker container, launch the robot demo with a specific action number:
 
```bash
./run_a_demo.sh
```
It will ask you to enter the number.

This starts all necessary ROS nodes and executes action #1.

### 3. Run Additional Actions
-------------------------
If you’d like to run another action without restarting everything, just type:
```bash
rosrun movewithhead run_a_demo.py <action_number>
```

Example:
```bash
rosrun movewithhead run_a_demo.py 2
```
This sends action #2 to the robot.

Done!


## gazebo_simulation_and_control(From Hao) 

This directory contains subdirectories and packages related to the simulation and control of Flo V2.

### camera  
This folder contains the camera model and the code required to create and integrate the camera into the simulation environment.

### flo_humanoid  
This package includes the motor control code. All motor angles must be transmitted to the robot using the code in this package.

### flov2withhead  
This package contains the URDF model of the Flo V2 robot. Use this URDF file for simulation purposes.

### movewithhead  
This package contains the motion control code, which serves as the core of the control program. Key functionalities include:
- Complete motion control code.
- Generating the workspace for the robotic arm.

---

## ROS Version

The code and packages are compatible with **ROS Noetic**.

---

## Usage Instructions

1. Clone this repository into the `src` folder of your ROS workspace:
   ```bash
   cd ~/your_workspace/src
   git clone <repository_url>
   ```

2. Navigate to your workspace root and build the packages:
   ```bash
   cd ~/your_workspace
   catkin_make
   ```

3. Source your workspace before running the simulation:
   ```bash
   source devel/setup.bash
   ```
---

## Notes

- Ensure that **ROS Noetic** is installed and properly configured.
- The `movewithhead` package contains the core control program for Flo V2.
- Camera models are located in the `camera` folder for integration.

---

