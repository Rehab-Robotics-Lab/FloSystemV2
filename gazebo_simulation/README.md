# Gazebo Simulation for FLO Robot

This directory contains the necessary files to simulate the FLO robot in Gazebo. This allows for testing and development in a virtual environment.

## description

The flov2tag package stores the model and its physical parameters.

The test_moveit package sets up the ROS controller and MoveIt.


## Usage
Before starting, make sure you are at `FloSystemV2/gazebo_simulation`.

1. Build docker:
    ```sh
    bash build_Docker.sh
2. Run docker with `tmux`:
    ```sh
    bash run_Docker.sh
3. Run Simulation:
    ```sh
    bash run_full_robot_arm_sim.sh

## Example
Below is an example of controlling the robot arm in Gazebo with MoveIt and RViz:
![avart](./image/gazebo-ezgif.com-optimize.gif)

## Issues
Currently, the robot model can only be controlled using RViz.

## Ongoing Improvements and Future Plans

Write code to control the robot model programmatically.
Export data from MoveIt and send it to a real robotic arm for further control.