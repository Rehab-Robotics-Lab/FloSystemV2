#!/bin/bash
IMAGE_NAME="flo_dev_system"
IMAGE_TAG="latest"
echo "build flo_dev_system:latest image"
sudo docker build --tag $IMAGE_NAME:$IMAGE_TAG .
