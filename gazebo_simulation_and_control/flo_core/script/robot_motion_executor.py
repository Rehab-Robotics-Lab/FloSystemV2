#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Int32
import math

class RobotMotionExecutor:
    """
    Handles all robot motion execution logic.
    Separates motion planning and execution from the main controller.
    """
    
    def __init__(self, arm_R, arm_L, arm_D, rgripper_pub, lgripper_pub, end_effector_link_R, end_effector_link_L, end_effector_link_D):
        """
        Initialize the motion executor with MoveIt groups and publishers
        """
        self.arm_R = arm_R
        self.arm_L = arm_L
        self.arm_D = arm_D
        self.rgripper_pub = rgripper_pub
        self.lgripper_pub = lgripper_pub
        self.end_effector_link_R = end_effector_link_R
        self.end_effector_link_L = end_effector_link_L
        self.end_effector_link_D = end_effector_link_D
        
        # Gripper control values
        self.gripper_cup_r = 3410
        self.gripper_cup_l = 3710
        self.gripper_off_l = 3700
        self.gripper_brush_l = 3710
        self.gripper_brush_r = 3410
        self.gripper_on = 1300
        self.gripper_off = 3410
        
        # AprilTag position variables (will be updated from main controller)
        self.position_dbx = self.position_dby = 0  # Down bell position
        self.position_cx = self.position_cy = 0    # Cup position
        self.position_bx = self.position_by = 0    # Brush position
        self.position_rx = self.position_ry = 0    # Right arm reference position
        self.position_lx = self.position_ly = 0    # Left arm reference position
    
    def update_apriltag_positions(self, position_data):
        """
        Update AprilTag positions from the main controller
        """
        for key, value in position_data.items():
            setattr(self, key, value)
    
    def execute_pose(self, pose, reference_frame):
        """
        Execute specific movements based on the pose parameter.
        
        :param pose: Integer defining the type of movement to execute.
        :param reference_frame: The reference frame for motion planning.
        """
        rospy.loginfo(f"Executing pose: {pose}")
        
        # Return to home position first (except for dual arm poses)
        if pose < 21:
            if pose <= 10:  # Right arm poses
                self.arm_R.set_named_target('Rhome')
                self.arm_R.go()
            else:  # Left arm poses
                self.arm_L.set_named_target('Lhome')
                self.arm_L.go()
        
        # Execute specific pose
        if pose == 1:
            self._execute_right_wave()
        elif pose == 2:
            self._execute_right_punch()
        elif pose == 3:
            self._execute_right_raise()
        elif pose == 4:
            self._execute_right_wave_bell()
        elif pose == 6:
            self._execute_right_smart_bell(reference_frame)
        elif pose == 7:
            self._execute_right_smart_drink(reference_frame)
        elif pose == 8:
            self._execute_right_smart_brush(reference_frame)
        elif pose == 11:
            self._execute_left_wave()
        elif pose == 12:
            self._execute_left_punch()
        elif pose == 13:
            self._execute_left_raise()
        elif pose == 14:
            self._execute_left_wave_bell()
        elif pose == 16:
            self._execute_left_smart_bell(reference_frame)
        elif pose == 17:
            self._execute_left_smart_drink(reference_frame)
        elif pose == 18:
            self._execute_left_smart_brush(reference_frame)
        elif pose == 21:
            self._execute_dual_clap()
        elif pose == 22:
            self._execute_dual_up_down()
        elif pose == 23:
            self._execute_dual_alternate()
        elif pose == 24:
            self._execute_dual_punch()
        else:
            rospy.logwarn(f"Unknown pose: {pose}")
    
    # ==================== Right Arm Motions ====================
    
    def _execute_right_wave(self):
        """Pose 1: Right arm waving motion"""
        for i in range(3):
            self.arm_R.set_named_target('R_wave_start')
            self.arm_R.go()
            self.arm_R.set_named_target('R_wave_end')
            self.arm_R.go()
        self.arm_R.set_named_target('Rhome')
        self.arm_R.go()
    
    def _execute_right_punch(self):
        """Pose 2: Right arm punching motion"""
        self.rgripper_pub.publish(self.gripper_off)
        rospy.sleep(1)
        for i in range(3):
            self.arm_R.set_named_target('R_punch')
            self.arm_R.go()
            self.arm_R.set_named_target('Rhome')
            self.arm_R.go()
        self.rgripper_pub.publish(self.gripper_on)
        rospy.sleep(1)
    
    def _execute_right_raise(self):
        """Pose 3: Right arm raising motion"""
        for i in range(3):
            self.arm_R.set_named_target('R_raise')
            self.arm_R.go()
            self.arm_R.set_named_target('Rhome')
            self.arm_R.go()
    
    def _execute_right_wave_bell(self):
        """Pose 4: Right arm waving with bell interaction"""
        for i in range(3):
            self.arm_R.set_named_target('R_waveb')
            self.arm_R.go()
            self.arm_R.set_named_target('R_d_bell')
            self.arm_R.go()
        self.arm_R.set_named_target('Rhome')
        self.arm_R.go()
    
    def _execute_right_smart_bell(self, reference_frame):
        """Pose 6: Right arm smart bell interaction using AprilTag"""
        self.arm_R.set_max_acceleration_scaling_factor(1)
        self.arm_R.set_max_velocity_scaling_factor(0.8)
        
        current_posea = self.arm_R.get_current_pose(self.end_effector_link_R).pose
        
        # Calculate target position
        x = current_posea.position.x + self.position_dbx - self.position_rx
        y = current_posea.position.y + (self.position_ry - self.position_dby) - 0.04
        
        # Adjust joint angles
        joint_goal = self.arm_R.get_current_joint_values()
        joint_goal[2] += math.atan((self.position_dbx - self.position_rx) / 
                                  (self.position_ry - self.position_dby + 0.18 - 0.05))
        self.arm_R.go(joint_goal, wait=True)
        
        # Execute motion planning
        target_pose = self._create_target_pose(reference_frame, x, y, 1.04)
        self._execute_motion_plan(self.arm_R, target_pose, self.end_effector_link_R)
        
        # Bell interaction
        self.rgripper_pub.publish(self.gripper_off)
        rospy.sleep(1)
        for i in range(3):
            self.arm_R.set_named_target('R_wave_start')
            self.arm_R.go()
            self.arm_R.set_named_target('R_d_bell')
            self.arm_R.go()
        
        # Return to position and home
        self._execute_motion_plan(self.arm_R, target_pose, self.end_effector_link_R)
        rospy.sleep(1)
        self.rgripper_pub.publish(self.gripper_on)
        rospy.sleep(1)
        self.arm_R.set_named_target('Rhome')
        self.arm_R.go()
        
        # Restore speed settings
        self.arm_R.set_max_acceleration_scaling_factor(0.6)
        self.arm_R.set_max_velocity_scaling_factor(0.5)
    
    def _execute_right_smart_drink(self, reference_frame):
        """Pose 7: Right arm smart drink using AprilTag"""
        current_posea = self.arm_R.get_current_pose(self.end_effector_link_R).pose
        
        # Calculate target position
        x = current_posea.position.x + self.position_cx - self.position_rx - 0.1
        y = current_posea.position.y + (self.position_ry - self.position_cy) + 0.02
        
        # Adjust joint angles
        joint_goal = self.arm_R.get_current_joint_values()
        joint_goal[2] += math.atan((self.position_cx - self.position_rx) / 
                                  (self.position_ry - self.position_cy + 0.18 - 0.05))
        joint_goal[3] += 0.042
        self.arm_R.go(joint_goal, wait=True)
        
        # Execute motion planning
        target_pose = self._create_target_pose(reference_frame, x, y, 1.03)
        self._execute_motion_plan(self.arm_R, target_pose, self.end_effector_link_R)
        rospy.sleep(1)
        
        # Drinking motion
        self.rgripper_pub.publish(self.gripper_cup_r)
        rospy.sleep(1)
        self.arm_R.set_named_target('R_cup_up')
        self.arm_R.go()
        rospy.sleep(1)
        self.arm_R.set_named_target('R_drink')
        self.arm_R.go()
        rospy.sleep(1)
        self.arm_R.set_named_target('R_cup_up')
        self.arm_R.go()
        rospy.sleep(1)
        
        # Return to position and home
        self._execute_motion_plan(self.arm_R, target_pose, self.end_effector_link_R)
        rospy.sleep(1)
        self.rgripper_pub.publish(self.gripper_on)
        rospy.sleep(1)
        self.arm_R.set_named_target('Rhome')
        self.arm_R.go()
    
    def _execute_right_smart_brush(self, reference_frame):
        """Pose 8: Right arm smart brush using AprilTag"""
        current_posea = self.arm_R.get_current_pose(self.end_effector_link_R).pose
        
        # Calculate target position
        x = current_posea.position.x + self.position_bx - self.position_rx
        y = current_posea.position.y + (self.position_ry - self.position_by) - 0.04
        
        # Adjust joint angles
        joint_goal = self.arm_R.get_current_joint_values()
        joint_goal[2] += math.atan((self.position_bx - self.position_rx) / 
                                  (self.position_ry - self.position_by + 0.18 - 0.05))
        self.arm_R.go(joint_goal, wait=True)
        
        # Execute motion planning
        target_pose = self._create_target_pose(reference_frame, x, y, 1.03)
        self._execute_motion_plan(self.arm_R, target_pose, self.end_effector_link_R)
        rospy.sleep(1)
        
        # Brushing motion
        self.rgripper_pub.publish(self.gripper_brush_r)
        rospy.sleep(1)
        for _ in range(3):
            self.arm_R.set_named_target('R_brush')
            self.arm_R.go()
            self.arm_R.set_named_target('R_brush2')
            self.arm_R.go()
        
        # Return to position and home
        self._execute_motion_plan(self.arm_R, target_pose, self.end_effector_link_R)
        rospy.sleep(1)
        self.rgripper_pub.publish(self.gripper_on)
        rospy.sleep(1)
        self.arm_R.set_named_target('Rhome')
        self.arm_R.go()
    
    # ==================== Left Arm Motions ====================
    
    def _execute_left_wave(self):
        """Pose 11: Left arm waving motion"""
        for i in range(3):
            self.arm_L.set_named_target('L_wave_start')
            self.arm_L.go()
            self.arm_L.set_named_target('L_wave_end')
            self.arm_L.go()
        self.arm_L.set_named_target('Lhome')
        self.arm_L.go()
    
    def _execute_left_punch(self):
        """Pose 12: Left arm punching motion"""
        self.lgripper_pub.publish(self.gripper_off_l)
        rospy.sleep(1)
        for i in range(3):
            self.arm_L.set_named_target('L_punch')
            self.arm_L.go()
            self.arm_L.set_named_target('Lhome')
            self.arm_L.go()
        self.lgripper_pub.publish(self.gripper_on)
        rospy.sleep(1)
    
    def _execute_left_raise(self):
        """Pose 13: Left arm raising motion"""
        for i in range(3):
            self.arm_L.set_named_target('L_raise')
            self.arm_L.go()
            self.arm_L.set_named_target('Lhome')
            self.arm_L.go()
    
    def _execute_left_wave_bell(self):
        """Pose 14: Left arm waving with bell interaction"""
        for i in range(3):
            self.arm_L.set_named_target('L_waveb')
            self.arm_L.go()
            self.arm_L.set_named_target('L_d_bell')
            self.arm_L.go()
        self.arm_L.set_named_target('Lhome')
        self.arm_L.go()
    
    def _execute_left_smart_bell(self, reference_frame):
        """Pose 16: Left arm smart bell interaction using AprilTag"""
        self.arm_L.set_max_acceleration_scaling_factor(1.0)
        
        current_posea = self.arm_L.get_current_pose(self.end_effector_link_L).pose
        
        # Calculate target position
        x = current_posea.position.x + self.position_dbx - self.position_lx
        y = current_posea.position.y + (self.position_ly - self.position_dby) - 0.03
        
        # Adjust joint angles
        joint_goal = self.arm_L.get_current_joint_values()
        joint_goal[2] += math.atan((self.position_dbx - self.position_lx) / 
                                  (self.position_ly - self.position_dby + 0.18 - 0.055))
        self.arm_L.go(joint_goal, wait=True)
        
        # Execute motion planning
        target_pose = self._create_target_pose(reference_frame, x, y, 1.04)
        self._execute_motion_plan(self.arm_L, target_pose, self.end_effector_link_L)
        
        # Bell interaction
        self.lgripper_pub.publish(self.gripper_off_l)
        rospy.sleep(1)
        for i in range(3):
            self.arm_L.set_named_target('L_wave_start')
            self.arm_L.go()
            self.arm_L.set_named_target('L_d_bell')
            self.arm_L.go()
        
        self.arm_L.set_named_target('Lhome')
        self.arm_L.go()
        
        # Return to position and home
        self._execute_motion_plan(self.arm_L, target_pose, self.end_effector_link_L)
        rospy.sleep(1)
        self.lgripper_pub.publish(self.gripper_on)
        rospy.sleep(1)
        self.arm_L.set_named_target('Lhome')
        self.arm_L.go()
        self.arm_L.set_max_acceleration_scaling_factor(0.6)
    
    def _execute_left_smart_drink(self, reference_frame):
        """Pose 17: Left arm smart drink using AprilTag"""
        self.arm_L.set_max_acceleration_scaling_factor(0.8)
        
        current_posea = self.arm_L.get_current_pose(self.end_effector_link_L).pose
        
        # Calculate target position
        x = current_posea.position.x + self.position_cx - self.position_lx
        y = current_posea.position.y + (self.position_ly - self.position_cy) - 0.03
        
        # Adjust joint angles
        joint_goal = self.arm_L.get_current_joint_values()
        joint_goal[2] += math.atan((self.position_cx - self.position_lx) / 
                                  (self.position_ly - self.position_cy + 0.18 - 0.055))
        joint_goal[3] += 0.08
        self.arm_L.go(joint_goal, wait=True)
        
        # Execute motion planning
        target_pose = self._create_target_pose(reference_frame, x, y, 1.04)
        self._execute_motion_plan(self.arm_L, target_pose, self.end_effector_link_L)
        rospy.sleep(1)
        
        # Drinking motion
        self.lgripper_pub.publish(self.gripper_cup_l)
        rospy.sleep(3)
        self.arm_L.set_named_target('L_cup_up')
        self.arm_L.go()
        rospy.sleep(1)
        self.arm_L.set_named_target('L_drink')
        self.arm_L.go()
        rospy.sleep(1)
        self.arm_L.set_named_target('L_cup_up')
        self.arm_L.go()
        rospy.sleep(1)
        
        # Return to position and home
        self._execute_motion_plan(self.arm_L, target_pose, self.end_effector_link_L)
        rospy.sleep(1)
        self.lgripper_pub.publish(self.gripper_on)
        rospy.sleep(1)
        self.arm_L.set_named_target('Lhome')
        self.arm_L.go()
        self.arm_L.set_max_acceleration_scaling_factor(0.6)
    
    def _execute_left_smart_brush(self, reference_frame):
        """Pose 18: Left arm smart brush using AprilTag"""
        self.arm_L.set_max_acceleration_scaling_factor(0.8)
        
        current_posea = self.arm_L.get_current_pose(self.end_effector_link_L).pose
        
        # Calculate target position
        x = current_posea.position.x + self.position_bx - self.position_lx
        y = current_posea.position.y + (self.position_ly - self.position_by) - 0.025
        
        # Adjust joint angles
        joint_goal = self.arm_L.get_current_joint_values()
        joint_goal[2] += math.atan((self.position_bx - self.position_lx) / 
                                  (self.position_ly - self.position_by + 0.18 - 0.055))
        joint_goal[3] += 0.04
        self.arm_L.go(joint_goal, wait=True)
        
        # Execute motion planning
        target_pose = self._create_target_pose(reference_frame, x, current_posea.position.y + 0.01, 1.04)
        self._execute_motion_plan(self.arm_L, target_pose, self.end_effector_link_L)
        rospy.sleep(1)
        
        # Brushing motion
        self.lgripper_pub.publish(self.gripper_brush_l)
        rospy.sleep(1)
        for _ in range(3):
            self.arm_L.set_named_target('L_brush')
            self.arm_L.go()
            self.arm_L.set_named_target('L_brush2')
            self.arm_L.go()
        
        rospy.sleep(0.5)
        
        # Return to position and home
        self._execute_motion_plan(self.arm_L, target_pose, self.end_effector_link_L)
        rospy.sleep(1)
        self.lgripper_pub.publish(self.gripper_on)
        rospy.sleep(1)
        self.arm_L.set_named_target('Lhome')
        self.arm_L.go()
        self.arm_L.set_max_acceleration_scaling_factor(0.6)
    
    # ==================== Dual Arm Motions ====================
    
    def _execute_dual_clap(self):
        """Pose 21: Dual arm clapping motion"""
        self.arm_D.set_named_target('clap')
        self.arm_D.go()
        for i in range(3):
            self.arm_D.set_named_target('clap_close')
            self.arm_D.go()
            self.arm_D.set_named_target('clap_open')
            self.arm_D.go()
        self.arm_D.set_named_target('clap')
        self.arm_D.go()
        self.arm_D.set_named_target('D_home')
        self.arm_D.go()
    
    def _execute_dual_up_down(self):
        """Pose 22: Dual arm up-down motion"""
        for i in range(2):
            self.arm_D.set_named_target('D_up')
            self.arm_D.go()
            self.arm_D.set_named_target('D_down')
            self.arm_D.go()
        self.arm_D.set_named_target('D_up')
        self.arm_D.go()
        self.arm_D.set_named_target('D_home')
        self.arm_D.go()
    
    def _execute_dual_alternate(self):
        """Pose 23: Dual arm alternate motion"""
        for i in range(3):
            self.arm_D.set_named_target('L_down_R_up')
            self.arm_D.go()
            self.arm_D.set_named_target('R_down_L_up')
            self.arm_D.go()
        self.arm_D.set_named_target('D_home')
        self.arm_D.go()
    
    def _execute_dual_punch(self):
        """Pose 24: Dual arm punch motion"""
        self.rgripper_pub.publish(self.gripper_off)
        self.lgripper_pub.publish(3780)
        rospy.sleep(1.5)
        
        for i in range(3):
            self.arm_D.set_named_target('d_punch1')
            self.arm_D.go()
            self.arm_D.set_named_target('d_punch2')
            self.arm_D.go()
        
        self.arm_D.set_named_target('D_home')
        self.arm_D.go()
        
        self.lgripper_pub.publish(self.gripper_on)
        rospy.sleep(0.1)
        self.rgripper_pub.publish(self.gripper_on)
    
    # ==================== Helper Methods ====================
    
    def _create_target_pose(self, reference_frame, x, y, z):
        """Create a target pose for motion planning"""
        current_pose = self.arm_R.get_current_pose(self.end_effector_link_R).pose
        target_pose = PoseStamped()
        target_pose.header.frame_id = reference_frame
        target_pose.header.stamp = rospy.Time.now()
        target_pose.pose.position.x = x
        target_pose.pose.position.y = y
        target_pose.pose.position.z = z
        target_pose.pose.orientation = current_pose.orientation
        return target_pose
    
    def _execute_motion_plan(self, arm, target_pose, end_effector_link):
        """Execute motion planning for given arm and target pose"""
        arm.set_start_state_to_current_state()
        arm.set_joint_value_target(target_pose, end_effector_link, True)
        _, traj, _, _ = arm.plan()
        arm.execute(traj)
