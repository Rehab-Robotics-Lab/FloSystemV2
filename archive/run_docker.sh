#!/usr/bin/env bash

# 1) Remove old container
docker rm -f flo_v2_container 2>/dev/null || true

# 2) Build Docker image
docker build -t flo_v2_image .

# 3) Enable X server access on host (optional)
xhost +local:root || true

# Then run docker with X11 forwarding + device pass-through
docker run -it --name=flo_v2_container \
  --env="DISPLAY=$DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  -v="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --device=/dev/ttyACM0 \
  --privileged \
  --network host \
  flo_v2_image
