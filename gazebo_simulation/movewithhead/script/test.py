#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy, sys
import moveit_commander
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64MultiArray, Int32

class MoveItIkDemo:
    def __init__(self):
        # 初始化move_group的API
        moveit_commander.roscpp_initialize(sys.argv)
        
        # 初始化ROS节点
        rospy.init_node('moveit_ik_demo')

        self.left_arm_joint_angles_pub = rospy.Publisher('/joint_angles', Float64MultiArray, queue_size=10)
        self.gripper_pub = rospy.Publisher('/gripper', Int32, queue_size=10)


        # 初始化需要使用move group控制的机械臂中的arm group
        self.arm = moveit_commander.MoveGroupCommander('R')
                
        # 获取终端link的名称
        self.end_effector_link = self.arm.get_end_effector_link()
                        
        # 设置目标位置所使用的参考坐标系
        reference_frame = 'world'
        self.arm.set_pose_reference_frame(reference_frame)
                
        # 当运动规划失败后，允许重新规划
        self.arm.allow_replanning(True)
        
        # 设置位置(单位：米)和姿态（单位：弧度）的允许误差
        self.arm.set_goal_position_tolerance(0.001)
        self.arm.set_goal_orientation_tolerance(1)
       
        # 设置允许的最大速度和加速度
        self.arm.set_max_acceleration_scaling_factor(0.5)
        self.arm.set_max_velocity_scaling_factor(0.3)

        # 控制机械臂先回到初始化位置
        self.arm.set_named_target('Rhome')
        self.arm.go()

        self.arm.set_named_target('R_wave_start')
        self.arm.go()

        self.arm.set_named_target('R_wave_end')
        self.arm.go()

        self.arm.set_named_target('R_wave_start')
        self.arm.go()

        self.arm.set_named_target('R_wave_end')
        self.arm.go()

        self.arm.set_named_target('R_wave_start')
        self.arm.go()

        self.arm.set_named_target('Rhome')
        self.arm.go()
        
        """
        
        
        
        x = 0.09
        y = 0.17
        z = 1.03

        self.print_current_pose()
        current_pose = self.arm.get_current_pose(self.end_effector_link).pose
        target_pose = PoseStamped()
        target_pose.header.frame_id = reference_frame
        target_pose.header.stamp = rospy.Time.now()     
        target_pose.pose.position.x = x
        target_pose.pose.position.y = y
        target_pose.pose.position.z = z
        #target_pose.pose.orientation.x = current_pose.orientation
        target_pose.pose.orientation.x = -0.50
        target_pose.pose.orientation.y = -0.50
        target_pose.pose.orientation.z = -0.50
        target_pose.pose.orientation.w =  0.50

        # 设置机器臂当前的状态作为运动初始状态
        self.arm.set_start_state_to_current_state()
        
        # 设置机械臂终端运动的目标位姿
        self.arm.set_joint_value_target(target_pose, self.end_effector_link, True)
        
        # 规划运动路径
        _, traj, _, _ = self.arm.plan()

        joint_angles_pub = self.left_arm_joint_angles_pub

        # 提取规划路径中的关节角度
        joint_angle_sequences = []
        for point in traj.joint_trajectory.points:
            joint_angle_sequences.append(point.positions)

        # 发布关节角度序列
        joint_angle_array = Float64MultiArray()
        for joint_angles in joint_angle_sequences:
            joint_angle_array.data.extend(joint_angles)
        joint_angles_pub.publish(joint_angle_array)

        # 按照规划的运动路径控制机械臂运动
        self.arm.execute(traj)
        rospy.sleep(1)
        self.print_current_pose()

        
        gripper_angle = 3982  # 示例角度值，根据需求调整
        self.gripper_pub.publish(gripper_angle)
        """

        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

    def print_current_pose(self):
        current_pose = self.arm.get_current_pose(self.end_effector_link).pose
        rospy.loginfo(f"Current Pose: {current_pose}")

    

if __name__ == "__main__":
    MoveItIkDemo()
