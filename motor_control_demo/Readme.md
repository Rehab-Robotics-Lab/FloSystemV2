# Motor Control Demo:

##  General Description:

This package contains the motor control demo for the flo robot. It runs in concert with the Flo v2 system ROS environment and utilizes the PySimpleGUI package to create a simplified user interface for controlling the robot's motors. 

## Test Goals

The goal of this test is to verify that the motors are able to accurately move the joints of the flo V2 robot, to test the limits of motor torque and to establish joint limits to prevent damage to the humanoid.

 ## General Setup

Testing can be accomplished on a PC running Ubuntu 20.04 with ROS Noetic installed. Alternatively, the demo can be run inside a docker container either on the Ohmni telepresence robot or on a PC. Start ros using the roscore command, then rosrun the read_write_arm node or the read_write_arms node. Finally,run either the MotorControlDemo.py or BiMotorControlDemo.py script to open the GUI window. Use the Sliders to control the motors; be careful during testing as the motors or the links can be damaged if they are moved too quickly or too far. 

A simplified testing pipeline has been created with extensive use of bash scripts to allow for easy testing of the motor control system.
To test the motor control system, run the following commands in the terminal:
```bash buildDocerMotorDemo.sh```
```bash runDockerMotorDemo.sh```
This will open a new docker container using the image we have just created, all the required libraries will have been prebuild inside the container.
Inside the docker container run the following commands to start the motor control demo:
1. for unilateral motor testing:
```bash unilateralMotorDemo.bash```
2. for bilateral motor testing:
```bash bilateralMotorDemo.bash```

In case of errors running the bash scripts, read on to the subsections below for more detailed instructions on how to run the motor control demo for unilateral and bilateral motor control.

## Troubleshooting:
    In case the bash scripts to run each of the motor demos is not working as expected, the following commands can be used to run the motor control demos manually:
    1. create a new tmux session inside the docker container:
    ```tmux new -s motorControlDemo```
    2. start the ros environment:
    ```roscore```
    3. split the tmux window horizontally and start the read_write_arm node:
    ```rosrun flo_humanoid read_write_arm```
    4. split the tmux window horizontally and run either of the 2 commands for unilateral and bilateral demos respoectively:
    ```python3 motorControlDemo.py```
    ```python3 biMotorControlDemo.py```

After each time the motor is disassemble and reassembled, the motor limits and defaults need to be reset. failure to do this may cause damage to the robot and/or the motors.    

## Unilateral Arm Motor Control:

### Description

This is a demo of the motor control system. It is a python script that will open a GUI window with sliders that will allow you to control the 4 motors present in the arm of the flo robot. The source code is located in the motorControlDemo.py file. 

### Setup

The read_write_arm node needs to be running for this to work as it publishes messages to the /set_joint_positions topic
Remember to add execute permission to the python executable before being able to run it (to add exucutable permissions to the file, run the command `chmod +x motorControlDemo.py` in the terminal)

## Bilateral Arm Motor Control:

### Description

This is a demo of the motor control system. It is a python script that will open a GUI window with sliders that will allow you to control the 8 motors present in the arms of the flo robot. The source code is located in the biMotorControlDemo.py file. 

### Setup

The read_write_arms node needs to be running for this to work as it publishes messages to the /set_arms_joint_positions topic
Remember to add execute permission to the python executable before being able to run it (to add exucutable permissions to the file, run the command `chmod +x biMotorControlDemo.py` in the terminal)



