# Flo V2 Control Stack for Aim 1 In-Person Robot AO Experiments

This repository contains the ROS Noetic control stack for the Flo V2 Aim 1 robot configuration without grippers. The supported setup is:

- Windows for Docker Desktop, `usbipd-win`, and the X server
- Ubuntu 24.04 inside WSL2 for Linux device access and all Docker CLI commands
- A Linux Docker container for the ROS, MQTT, Gazebo, and hardware control stack

The most important workflow change is that Docker Desktop should use the WSL2 backend, and Linux hardware services must be run from the WSL Ubuntu environment rather than directly from Windows PowerShell.

## Repository Structure

- `flo_core`: ROS launch files, MQTT bridge, planning config, and simulation entry points
- `flo_humanoid`: Dynamixel hardware bridge and robot-side messages/services
- `flov2_robot_description`: robot URDF and meshes
- `docker-compose.yml`: example Compose service definition
- `Dockerfile`: image build for the Flo V2 ROS workspace
- `docker_entrypoint.sh`: container startup logic with optional auto-bringup

## Recommended Host Setup

### 1. Install WSL2 and Ubuntu 24.04

Run these commands in Windows PowerShell as Administrator:

```powershell
wsl --install
wsl --set-default-version 2
wsl --install -d Ubuntu-24.04
wsl --update
```

Verify the install:

```powershell
wsl -l -v
```

Open the Ubuntu shell:

```powershell
wsl -d Ubuntu-24.04
```

Inside WSL, confirm you are running the expected distro:

```bash
uname -r
cat /etc/os-release
```

Expected result:

- `wsl -l -v` shows `VERSION` = `2`
- `uname -r` includes `microsoft-standard-WSL2`
- `/etc/os-release` shows Ubuntu 24.04

### 2. Install Docker Desktop on Windows

Install Docker Desktop from:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

In Docker Desktop settings, enable:

- `Use the WSL 2 based engine`
- `Integration with my default WSL distro`

After Docker Desktop starts, do Docker build and run commands from the Ubuntu WSL shell, not from Windows PowerShell.

### 3. Install `usbipd-win` for USB pass-through

Run in Windows PowerShell as Administrator:

```powershell
winget install --interactive --exact dorssel.usbipd-win
```

Inside WSL Ubuntu, install the USB utilities:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y linux-tools-generic hwdata usbutils
sudo update-alternatives --install /usr/local/bin/usbip usbip /usr/lib/linux-tools/*-generic/usbip 20
usbip version
```

### 4. Install VcXsrv on Windows

Install VcXsrv from:

- <https://sourceforge.net/projects/vcxsrv/>

Suggested XLaunch options:

- `Multiple windows`
- `Start no client`
- `Disable access control`

## USB Pass-through: Windows to WSL

From Windows PowerShell as Administrator, inspect attached devices:

```powershell
usbipd list
```

Bind each device you want to share with WSL:

```powershell
usbipd bind --busid <BUSID>
```

Example auto-attach script:

```powershell
usbipd attach --wsl --hardware-id 0403:6014
usbipd attach --wsl --hardware-id 16c0:0483
Start-Job { usbipd attach --wsl --hardware-id 0403:6014 --auto-attach }
Start-Job { usbipd attach --wsl --hardware-id 16c0:0483 --auto-attach }
usbipd list
```

Inside WSL, create stable `udev` aliases so Docker does not depend on `ttyUSB0` or `ttyACM0` numbering:

```bash
sudo cp config/99-flo-usb-devices.rules /etc/udev/rules.d/99-flo-usb-devices.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
ls -l /dev/flo_motors /dev/flo_led
```

Typical hardware mapping:

- `/dev/flo_motors` -> FTDI / U2D2 (`0403:6014`)
- `/dev/flo_led` -> Teensy USB serial (`16c0:0483`)

If you need to confirm the raw kernel-assigned devices too:

```bash
ls /dev/ttyUSB* /dev/ttyACM*
udevadm info --name=/dev/ttyACM0 --attribute-walk | grep -E "idVendor|idProduct"
udevadm info --name=/dev/ttyUSB0 --attribute-walk | grep -E "idVendor|idProduct"
```

## Clone the Repository

Clone the repository into a path that is easy to access from WSL. The current examples assume:

```text
C:\Users\<your-user>\git\FloSystemV2
```

Inside WSL, that path is:

```bash
/mnt/c/Users/<your-user>/git/FloSystemV2
```

## Build the Docker Image

All Docker commands below should be run inside the Ubuntu WSL shell.

```bash
cd /mnt/c/Users/<your-user>/git/FloSystemV2
docker build -t flo_v2_image_aim1 .
```

Notes:

- The image build clones the FloSystemV2 GitHub repository into `/catkin_ws/src/FloSystemV2` inside the container image.
- The local repository is still useful for editing, documentation, and `docker compose`.

## Run with Docker Compose

The default service in [`docker-compose.yml`](docker-compose.yml) is `flo_v2_aim1`.

Bring it up:

```bash
cd /mnt/c/Users/<your-user>/git/FloSystemV2
source ./resolve_flo_devices.sh
docker compose up --build
```

`resolve_flo_devices.sh` waits briefly for newly attached USB devices to settle in WSL before failing. If `usbipd` is especially slow on a given boot, you can increase the wait window with `FLO_DEVICE_RESOLVE_RETRIES` and `FLO_DEVICE_RESOLVE_INTERVAL_SEC`.

Start an already-created container again:

```bash
docker compose start flo_v2_aim1
docker compose attach flo_v2_aim1
```

Stop and remove it:

```bash
docker compose down
```

## Run with `docker run`

If you want to start the container directly instead of using Compose:

```bash
export DISPLAY=$(grep nameserver /etc/resolv.conf | awk '{print $2}'):0
export QT_X11_NO_MITSHM=1
source ./resolve_flo_devices.sh

docker run -it \
  --name flo_v2_aim1 \
  --privileged \
  --device="$FLO_MOTORS_HOST_DEVICE":/dev/flo_motors \
  --device="$FLO_LED_HOST_DEVICE":/dev/flo_led \
  -e DISPLAY=host.docker.internal:0 \
  -e QT_X11_NO_MITSHM=1 \
  -e LIBGL_ALWAYS_INDIRECT=1 \
  -e FLO_MOTORS_SERIAL_PORT=/dev/flo_motors \
  -e LED_SERIAL_PORT=/dev/flo_led \
  -p 1883:1883 \
  -p 11311:11311 \
  -p 8080:8080 \
  flo_v2_image_aim1
```

Re-enter a running container:

```bash
docker exec -it flo_v2_aim1 bash
```

Restart an existing stopped container:

```bash
docker start -ai flo_v2_aim1
```

## Auto Bringup on Container Start

The entrypoint supports automatic execution of `tmux_robot_bringup_legacy.sh` when `AUTO_BRINGUP=true`.

Example with `docker run`:

```bash
source ./resolve_flo_devices.sh
docker run -it \
  --name flo_v2_aim1 \
  --privileged \
  --device="$FLO_MOTORS_HOST_DEVICE":/dev/flo_motors \
  --device="$FLO_LED_HOST_DEVICE":/dev/flo_led \
  -e DISPLAY=host.docker.internal:0 \
  -e QT_X11_NO_MITSHM=1 \
  -e LIBGL_ALWAYS_INDIRECT=1 \
  -e FLO_MOTORS_SERIAL_PORT=/dev/flo_motors \
  -e LED_SERIAL_PORT=/dev/flo_led \
  -e AUTO_BRINGUP=true \
  -p 1883:1883 \
  -p 11311:11311 \
  -p 8080:8080 \
  flo_v2_image_aim1
```

For Compose, edit [`docker-compose.yml`](docker-compose.yml) and set:

```yaml
AUTO_BRINGUP: "true"
```

Then create or restart the service:

```bash
docker compose up --build
```

Or later:

```bash
docker compose start flo_v2_aim1
docker compose attach flo_v2_aim1
```

If `AUTO_BRINGUP` is unset or `false`, the container starts with an interactive shell.

## Inside-the-Container Commands

Source the ROS environment first:

```bash
source /opt/ros/noetic/setup.bash
source /catkin_ws/devel/setup.bash
```

### Test motor communication

```bash
roslaunch flo_humanoid read_write_arms.launch
```

If you see `Failed to open the port!`:

- Confirm `/dev/flo_motors` exists in WSL
- Resolve the raw host device with `source ./resolve_flo_devices.sh && echo "$FLO_MOTORS_HOST_DEVICE"`
- Confirm the container was started with the required `--device` mappings
- Reload `udev` rules with `sudo udevadm control --reload-rules && sudo udevadm trigger`
- Confirm the symlink points to the expected raw device with `ls -l /dev/flo_motors`
- If the aliases appear a moment after `usbipd attach`, retry once or temporarily raise `FLO_DEVICE_RESOLVE_RETRIES=20`

### Start MQTT broker

```bash
mosquitto -v -p 1883
```

### Start ROS core

```bash
roscore
```

### Start MoveIt for hardware bringup

Start the hardware-owned ROS side first:

```bash
roslaunch flo_humanoid dual_arm_hardware.launch
```

Then start the supported MoveIt bringup against the live hardware action servers:

```bash
roslaunch flo_core moveit_bringup.launch moveit_controller_manager:=simple use_rviz:=false load_robot_description:=false
```

This is the same non-Gazebo MoveIt path used by [`tmux_robot_bringup_legacy.sh`](/c:/Users/robor/git/FloSystemV2/tmux_robot_bringup_legacy.sh). `dual_arm_hardware.launch` already owns `robot_description`, `/joint_states`, and the hardware action servers, so the MoveIt launch reuses those instead of loading a separate simulated robot.

### Start simulation

```bash
roslaunch flo_core moveit_gazebo_bringup.launch show_gz_gui:=false show_rviz_gui:=false
```

Use simulation when you specifically want Gazebo-backed controllers instead of the live Dynamixel hardware path above.

If Gazebo or another controller is already publishing `/joint_states`, disable the hardware publisher instead:

```bash
roslaunch flo_humanoid dual_arm_hardware.launch publish_joint_states:=false
```

### Start the MQTT control node

```bash
rosrun flo_core mqtt_control_node.py
```

If you see `Name or service not known`, retry with:

```bash
MQTT_BROKER_HOST=localhost rosrun flo_core mqtt_control_node.py
```

### Send a test MQTT command

```bash
mosquitto_pub -h localhost -t ros/mqtt/movement -m "0"
```

## Test Scripts

MQTT-related test scripts live under:

- `flo_core/scripts/test`

Timing test scripts live under:

- `tests`

## Useful Tips

- Switch to the root shell in the container with `sudo -i`
- Copy files into a container with `docker cp <host_path> <container_name>:<container_path>`
- If you copy scripts from Windows into the container, normalize line endings:

```bash
find /catkin_ws -type f \( -name "*.sh" -o -name "*.py" \) -exec dos2unix {} \;
```

## Main Bringup Script

The primary bringup entry point is:

```bash
/catkin_ws/src/FloSystemV2/tmux_robot_bringup_legacy.sh
```
