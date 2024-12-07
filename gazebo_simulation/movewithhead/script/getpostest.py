#!/usr/bin/env python

import sys
import rospy
import moveit_commander

import math

class Moveik:
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)

        rospy.init_node('moveitik',anonymous=True)

        arm = moveit_commander.MoveGroupCommander('R')

        arm.set_goal_joint_tolerance(0.001)

        arm.set_max_acceleration_scaling_factor(0.5)
        arm.set_max_velocity_scaling_factor(0.5)

        arm.set_named_target('Rhome')
        arm.go()
        rospy.sleep(1)


        moveit_commander.roscpp_shutdown()
        moveit_commander.os.exit(0)

if __name__ == '__main__':
    try:
        Moveik()
    except rospy.ROSInterruptException:
        pass