#!/usr/bin/env bash
# ============================================================
# WSL2 Docker startup script with USB device support
# Use this script when running on Windows with WSL2
# ============================================================

echo "=== FLO v2 Docker on WSL2 ==="

# Remove old container
echo "Removing old container..."
docker rm -f flo_v2_container 2>/dev/null || true

# Get Windows host IP for X11 display
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
echo "DISPLAY set to: $DISPLAY"

# Check for USB devices
echo ""
echo "Checking USB devices..."
if [ -e /dev/ttyUSB0 ]; then
    echo "✓ Dynamixel device found: /dev/ttyUSB0"
    DEVICE_USB="--device=/dev/ttyUSB0:/dev/ttyUSB0"
else
    echo "✗ WARNING: /dev/ttyUSB0 not found!"
    echo "  Run in Windows PowerShell (Admin): usbipd attach --wsl --busid <BUSID>"
    DEVICE_USB=""
fi

if [ -e /dev/video0 ]; then
    echo "✓ Camera found: /dev/video0"
    DEVICE_CAM="--device=/dev/video0:/dev/video0"
else
    echo "✗ Camera not found (optional)"
    DEVICE_CAM=""
fi

echo ""
echo "Starting Docker container..."
echo "Press Ctrl+C to stop"
echo ""

# Run container with USB devices
docker run -it --rm \
  --name flo_v2_container \
  --privileged \
  --network host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e LIBGL_ALWAYS_INDIRECT=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  $DEVICE_USB \
  $DEVICE_CAM \
  flo_v2_image

echo ""
echo "Container exited."

