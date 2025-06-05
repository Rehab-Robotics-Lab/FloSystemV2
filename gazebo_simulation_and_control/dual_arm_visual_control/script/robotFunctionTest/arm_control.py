#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy, sys
import moveit_commander
from geometry_msgs.msg import PoseStamped
import paho.mqtt.client as mqtt
from std_msgs.msg import Int32 , String

import threading


def main():

    mode = "0"



     # 初始化move_group的API
    moveit_commander.roscpp_initialize(sys.argv)
    
    # 初始化ROS节点
    rospy.init_node('moveit_ik_demo')

    self.gripper_pub = rospy.Publisher('/gripper', Int32, queue_size=10)


if __name__ == "__main__":
    main()
