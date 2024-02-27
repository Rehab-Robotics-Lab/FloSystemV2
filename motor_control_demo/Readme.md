# Motor Control Demo:

##  General Description:

    This package contains the motor control demo for the flo robot. It runs in concert with the Flo v2 system ROS environment and utilizes the PySimpleGUI package to create a simplified user interface for controlling the robot's motors. 

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