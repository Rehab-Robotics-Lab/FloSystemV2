#!/usr/bin/env python

import sys
import rospy
import moveit_commander
from sensor_msgs.msg import JointState

class Moveik:
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('moveitik', anonymous=True)

        self.arm = moveit_commander.MoveGroupCommander('R')

        self.arm.set_goal_joint_tolerance(0.001)
        self.arm.set_max_acceleration_scaling_factor(0.5)
        self.arm.set_max_velocity_scaling_factor(0.5)

        self.joint_state_publisher = rospy.Publisher('/joint_states', JointState, queue_size=10)

        self.arm.set_named_target('Rhome')
        self.plan_and_execute()

    def plan_and_execute(self):
        plan = self.arm.plan()
        self.arm.execute(plan, wait=True)
        rospy.sleep(1)

        joint_states = self.arm.get_current_joint_values()
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = rospy.Time.now()
        joint_state_msg.name = self.arm.get_active_joints()
        joint_state_msg.position = joint_states

        self.joint_state_publisher.publish(joint_state_msg)

        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

if __name__ == '__main__':
    try:
        Moveik()
    except rospy.ROSInterruptException:
        pass