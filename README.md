# Flo V2 Control Programs and Models Repository

This repository contains control programs, simulation code, and model files for the Flo V2 robot.

## Repository Structure

```plaintext
gazebo_simulation_and_control/
robot_arm_matlab_simulation/
SIM/
README.md
```

## gazebo_simulation_and_control  
This directory contains all files related to simulation and control of Flo V2. It includes code for testing and verifying the robot's movements in the Gazebo simulation environment.

## robot_arm_matlab_simulation  
This directory contains MATLAB scripts for verifying the DH parameters of the robotic arm.

## SIM  
This directory includes the model files for the Flo V2 robot,Also included here is a tutorial that will show you how to import the model into gazebo in its entirety!.

---

## Prerequisites:

```
sudo apt install mosquitto mosquitto-clients
```

## Installation:

1. Create `~/catkin_ws` workspace and `~/catkin_ws/src` folder

2. Inside `src`, clone this repo and `git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git`

3. Install dependency: `sudo apt install ros-noetic-dynamixel-sdk ros-noetic-dynamixel-sdk-examples`

4. `cd ~/catkin_ws` then `catkin_make`. Make sure the packages are succesfully built.

5. `source devel/setup.bash`

6. `roslaunch movewithhead full_robot_arm_sim.launch`

7. Open another terminal, run `source devel/setup.bash` then `rosrun flo_humanoid read_write_arms_node`. You should see that the robot arms become stiff.

8. Open new terminal and `source devel/setup.bash`. Run `chmod +x /home/anhtn/catkin_ws_2/src/FloSystemV2/gazebo_simulation_and_control/movewithhead/script/dualPosition.py` then run `rosrun movewithhead script/dualPosition.py`

9. Open new terminal and `source devel/setup.bash`. Run `chmod +x /home/anhtn/catkin_ws_2/src/FloSystemV2/gazebo_simulation_and_control/movewithhead/script/test.py` then run