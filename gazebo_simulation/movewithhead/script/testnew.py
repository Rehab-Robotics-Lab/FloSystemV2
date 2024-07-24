#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Float64MultiArray

class JointAnglesListener:
    def __init__(self):
        # 初始化ROS节点
        rospy.init_node('joint_angles_listener', anonymous=True)
        
        # 订阅/joint_angles话题
        rospy.Subscriber('/joint_angles', Float64MultiArray, self.joint_angles_callback)
        
        rospy.loginfo("Listening to /joint_angles topic...")

    def joint_angles_callback(self, msg):
        # 当接收到/joint_angles消息时的回调函数
        rospy.loginfo(f"Received joint angles: {msg.data}")

if __name__ == "__main__":
    try:
        JointAnglesListener()
        # 保持节点运行，直到手动中断
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
