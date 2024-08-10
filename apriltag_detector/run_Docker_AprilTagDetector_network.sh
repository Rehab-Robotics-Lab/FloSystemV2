#!/bin/bash

# Remove all stopped containers
docker container prune -f

# Allow access to X server
xhost +

# Build the Docker image
docker build -t apriltag_detector .

# Run the Docker container with the specified options and port mapping
docker run -it --rm --name apriltag_detector \
  --device=/dev/ttyUSB0 \
  --net=host \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --privileged \
  -p 1883:1883 \
  apriltag_detector

# Revoke access to X server
xhost -
