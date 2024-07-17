#!/usr/bin/env python
import rospy
import tf
from geometry_msgs.msg import Pose
from std_msgs.msg import String

def pose_callback(data):
    br = tf.TransformBroadcaster()
    br.sendTransform((data.position.x, data.position.y, data.position.z),
                     (data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w),
                     rospy.Time.now(),
                     "apriltag",  # child frame
                     "world")    # parent frame
    rospy.loginfo("Published Pose to TF: {}".format(data))

def info_callback(data):
    rospy.loginfo("Received Info: {}".format(data))

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/apriltag_poses', Pose, pose_callback)
    rospy.Subscriber('/apriltag_info', String, info_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
