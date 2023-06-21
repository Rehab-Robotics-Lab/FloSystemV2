# tb_ros_common

This repo includes 2 ROS packages:

* **std_msgs**: defined common ROS message/ service / action used in others Ohmnilabs ROS package.

* **ohmnilabs_common**: include some helper functions, used for developing other ROS package for Ohmni bot.

## Usage

To build a custom ROS node to talk to Ohmnilabs robot, first, clone and build the tb_msgs in a catkin workspace

```bash
# if you don’t have a catkin_ws, create one, then clone tb_msgs
> source /opt/ros/<your ROS distro>/setup.bash
> mkdir -p ~/catkin_ws/src
> cd ~/catkin_ws/src
> git clone [this repo]

# Build the tb_msgs
> cd ~/catkin_ws/
> catkin_make -DCATKIN_WHITELIST_PACKAGES="tb_msgs"

#Then if you have other ROS node and want to talk to tb_control, source this workspace before building your node
your node ws> source ~/catkin_ws/devel/setup.bash
your node ws> catkin_make

```
