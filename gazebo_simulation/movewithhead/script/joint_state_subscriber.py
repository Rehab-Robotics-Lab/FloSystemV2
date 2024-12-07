#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState

def joint_state_callback(msg):
    rospy.loginfo("Received joint states:")
    for name, position in zip(msg.name, msg.position):
        rospy.loginfo("Joint: %s, Position: %f", name, position)

def main():
    rospy.init_node('joint_state_subscriber', anonymous=True)
    
    rospy.Subscriber('/joint_states', JointState, joint_state_callback)
    
    rospy.loginfo("Joint state subscriber is running...")
    
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass