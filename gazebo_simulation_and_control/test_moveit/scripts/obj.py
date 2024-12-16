#!/usr/bin/env python

import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from geometry_msgs.msg import PoseStamped

def move_group_python_interface_tutorial():


    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_end_effector_forward', anonymous=True)

    #robot = moveit_commander.RobotCommander()
    #scene = moveit_commander.PlanningSceneInterface()
    group_name = "armr"  # 根据您的规划组名称修改
    group = moveit_commander.MoveGroupCommander(group_name)

    #display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)
    
    
    end = group.get_end_effector_link()
    
    reference = "base_link"
    group.set_pose_reference_frame(reference)
    
    group.allow_replanning(True)
    
    group.set_goal_position_tolerance(0.1)
    group.set_goal_orientation_tolerance(0.1)
    current_pose = group.get_current_pose().pose
    print("============ Current pose:")
    print(current_pose)
    target = PoseStamped()
    target.header.frame_id = reference
    target.header.stamp = rospy.Time.now()
    target.pose.position.x = 0.16264199103537122

    target.pose.position.y = 0.03873170425984944

    target.pose.position.z = 0.20977468111406491
    target.pose.orientation.x = 0.5952732678938092

    target.pose.orientation.y = 0.08090676520120177

    target.pose.orientation.z = 0.5889381249131203

    target.pose.orientation.w = 0.5406068043407541
    
    group.set_start_state_to_current_state()
    
    group.set_pose_target(target,end)
    
    plan_success, plan, planning_time, error_code = group.plan()


    group.execute(plan)


   

    rospy.sleep(5)
    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
  try:
    move_group_python_interface_tutorial()
  except rospy.ROSInterruptException:
    pass
