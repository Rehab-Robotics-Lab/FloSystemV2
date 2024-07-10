#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from std_msgs.msg import String

def pose_callback(data):
    rospy.loginfo("Received Pose: {}".format(data))

def info_callback(data):
    rospy.loginfo("Received Info: {}".format(data))

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/apriltag_poses', Pose, pose_callback)
    rospy.Subscriber('/apriltag_info', String, info_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
