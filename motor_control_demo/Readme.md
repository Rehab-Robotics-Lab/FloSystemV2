# Motor Control Demo:

##  General Description:

This package contains the motor control demo for the flo robot. It runs in concert with the Flo v2 system ROS environment and utilizes the PySimpleGUI package to create a simplified user interface for controlling the robot's motors. 

 ## General Setup

Testing can be accomplished on a PC running Ubuntu 20.04 with ROS Noetic installed. Alternatively, the demo can be run inside a docker container either on the Ohmni telepresence robot or on a PC. Start ros using the roscore command, then rosrun the read_write_arm node or the read_write_arms node. Finally,run either the MotorControlDemo.py or BiMotorControlDemo.py script to open the GUI window. Use the Sliders to control the motors; be careful during testing as the motors or the links can be damaged if they are moved too quickly or too far. 

## Test Goals

The goal of this test is to verify that the motors are able to accurately move the joints of the flo V2 robot and to establish joint limits to prevent damage to the humanoid.

## Unilateral Arm Motor Control:

### Description

This is a demo of the motor control system. It is a python script that will open a GUI window with sliders that will allow you to control the 4 motors present in the arm of the flo robot. The source code is located in the MotorControlDemo.py file. 

### Setup

The read_write_arm node needs to be running for this to work as it publishes messages to the /set_joint_positions topic
Remember to add execute permission to the python executable before being able to run it (to add exucutable permissions to the file, run the command `chmod +x MotorControlDemo.py` in the terminal)


## TODO
## Bilateral Arm Motor Control:

### Description

This is a demo of the motor control system. It is a python script that will open a GUI window with sliders that will allow you to control the 8 motors present in the arms of the flo robot. The source code is located in the BiMotorControlDemo.py file. 

### Setup

The read_write_arms node needs to be running for this to work as it publishes messages to the /set_arms_joint_positions topic
Remember to add execute permission to the python executable before being able to run it (to add exucutable permissions to the file, run the command `chmod +x BiMotorControlDemo.py` in the terminal)