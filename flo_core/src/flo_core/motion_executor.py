#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy

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
        
    
    def execute_pose(self, pose):
        """
        Execute specific movements based on the pose parameter.
        
        :param pose: Integer defining the type of movement to execute.
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
        elif pose == 11:
            self._execute_left_wave()
        elif pose == 12:
            self._execute_left_punch()
        elif pose == 13:
            self._execute_left_raise()
        elif pose == 14:
            self._execute_left_wave_bell()
        elif pose == 21:
            self._execute_dual_clap()
        elif pose == 22:
            self._execute_dual_up_down()
        elif pose == 23:
            self._execute_dual_alternate()
        elif pose == 24:
            self._execute_dual_punch()
        elif pose == 25:
            self._execute_dual_go_to_home()
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
    
    def _execute_dual_go_to_home(self):
        """Pose 25: Dual arm go to home motion"""
        self.arm_D.set_named_target('D_home')
        self.arm_D.go()
