# Flo-System-2
This is the master code repository for the second iteration of the Flo system. 
The system is currently in development, all code is subject to change.
## License:

MIT License. 

Copyright 2023 University of Pennsylvania, Rehabilitation Robotics Lab

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Overview:

The Flo V2 system runs on a set of containerized environments with each subsystem running its own docker container. 

This system is intended to run on a development edition ohmni telepresence robot with docker installed but due to the nature of the docker containers 
should be able to run with limited capacity in any system with docker.

This repository contains the following components:

1. Control system of the humanoid robot (Dynamixel motors: 2 XL430-W250-T, 1 XC430-W240-T, 1 XM430-W350-T and 1 RX-64 motor per arm)
2. Control system of the mobile telepresence platform (Ohmni telepresence platform)
3. RGB telepresence and navigation cameras (forwards facing and downwards facing)
4. RGB-D cameras (2 Luxonis Oak-D lite cameras)
5. object localization system (April tag 3)
6. User/Operator interface (web interface)
7. 2 dimensional lidar sensor (rp lidar a1)
8. Obstacle avoidance and autonomous movement systems 

The system is designed to be modular and each component can be run independently, ROS is used as the communication framework between the components.

Each component will be running as a seperate process and interfacing with the ros master remotely.


## Connecting to the Ohmni telepresence robot and running docker
1. Clone this repository using git clone https://github.com/Rehab-Robotics-Lab/Flo-System-2.git 
2. Download the private ssh key from penn box https://upenn.app.box.com/folder/206840565719; contact @anht-nguyen for access if necessary. 
3. ./ohmniConnect.bash - will ssh into the Ohmni telepresence robot (must be on the same local network)
4. ./var/dockerhome/floSystem.bash - to start a docker container running the flo system (will run in detached mode)
5. docker attach flo_system

## Running the motor control nodes 
The motors are intended to be controlled through the web interface but can also be controlled via CLI for testing

## Controlling the ohmni telepresence robot 
References at: https://docs.ohmnilabs.com/

The ohmni base is controlled via the tb control node, this node can take messages via CLI but is also intended to be controlled via the user interface

#Docker Compose

All of the subsystems can be started using '''docker compose up'''

