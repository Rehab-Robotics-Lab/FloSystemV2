#!/bin/bash
WSDIR=$PWD
DOCKER_SERVER="baoden/ohmni_rgbcam_ros"

echo  "========= build base image  ========="
cd  $WSDIR/base_ros; ./build.sh c

echo  "========= build rgb ROS image  ========="
cd  $WSDIR/ohmni_rgbcamera; ./build.sh 

sudo docker tag ohmni_rgbcam:base $DOCKER_SERVER:base_ros
sudo docker tag ohmni_rgbcam:launch $DOCKER_SERVER:launch_ros

sudo docker push $DOCKER_SERVER:base_ros
sudo docker push $DOCKER_SERVER:launch_ros