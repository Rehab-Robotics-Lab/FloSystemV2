
# FLOSystemV2 Docker Communication Development

This repository contains the necessary files to set up and run Docker containers for communication development in the FLOSystemV2 project. The setup includes two primary containers: `apriltag_detector` for detecting AprilTags and `docker_communication` for subscribing to the published topics.

## Prerequisites

Ensure you have Docker installed on your system. You can follow the official Docker installation guide: [Docker Installation](https://docs.docker.com/get-docker/)

## Setup Instructions

### 1. Run the AprilTag Detector

Navigate to the directory where the `apriltag_detector` is located and run the container. Replace `run_Docker_AprilTagDetector.sh` with `run_Docker_AprilTagDetector_network.sh` as follows:

```bash
bash run_Docker_AprilTagDetector_network.sh
```

### 2. Verify Topics

Open a terminal and use the following command to list the topics to ensure they are being published:

```bash
rostopic list
```

You should see the topics `/apriltag_poses` and `/apriltag_info` listed.

### 3. Navigate to `docker_communication` Directory

Ensure you are in the `FloSystemV2/docker_communication` directory:

```bash
cd ~/Documents/FloSystemV2/docker_communication
```

### 4. Build the Docker Image for `docker_communication`

In another terminal, build the Docker image using the `build_Docker.sh` script:

```bash
bash build_Docker.sh
```

### 5. Run the Docker Communication Container

Use the `run_docker_network.sh` script to start the `docker_communication` container:

```bash
bash run_docker_network.sh
```

### 6. Run the Subscriber Script

Inside the `docker_communication` container, run the `run_subscriber.sh` script:

```bash
bash run_subscriber.sh
```

### 7. View Topic Content

You should now be able to see the content of the topics published by the `apriltag_detector` container in the `docker_communication` container.

## Script Details

### `run_docker_network.sh`

This script stops and removes any existing container with the same name, then runs a new instance of `docker_communication_image`.

```bash
#!/bin/bash

# Stop and remove any existing container
docker stop docker_communication || true
docker rm docker_communication || true

# Run the docker_communication container
docker run -it --name docker_communication --net=host docker_communication_image
```


## Issues and Improvements

- Ensure the correct package names are used in the scripts and commands.
- If you encounter any issues, check the Docker logs for detailed error messages.

## Contact

For any questions or issues, please contact Tian Tan at tiantan@seas.upenn.edu.