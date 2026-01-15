#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy

class RobotMotionExecutor:
    """
    Handles all robot motion execution logic.
    Separates motion planning and execution from the main controller.
    """
    
    def __init__(self, arm_R, arm_L, arm_D, end_effector_link_R, end_effector_link_L, end_effector_link_D):
        """
        Initialize the motion executor with MoveIt groups and publishers
        """
        self.arm_R = arm_R
        self.arm_L = arm_L
        self.arm_D = arm_D
        self.end_effector_link_R = end_effector_link_R
        self.end_effector_link_L = end_effector_link_L
        self.end_effector_link_D = end_effector_link_D
        
    
    def execute_pose(self, pose):
        """
        Execute specific movements based on the pose parameter.
        
        :param pose: Integer defining the type of movement to execute.
        """
        rospy.loginfo(f"Executing pose: {pose}")
        
        # Return to home position first (except for dual arm poses)
        # if pose < 25:
        #     if pose < 20:  # Right arm poses
        #         self.arm_L.set_named_target('Rhome')
        #         self.arm_L.go()
        #     else:  # Left arm poses
        #         self.arm_R.set_named_target('Lhome')
        #         self.arm_R.go()
        
        # Execute specific pose
        # if pose == 1:
        #     self._execute_right_wave()
        # elif pose == 2:
        #     self._execute_right_punch()
        # elif pose == 3:
        #     self._execute_right_raise()
        # elif pose == 4:
        #     self._execute_right_wave_bell()
        # elif pose == 11:
        #     self._execute_left_wave()
        # elif pose == 12:
        #     self._execute_left_punch()
        # elif pose == 13:
        #     self._execute_left_raise()
        # elif pose == 14:
        #     self._execute_left_wave_bell()
        # elif pose == 21:
        #     self._execute_dual_clap()
        # elif pose == 22:
        #     self._execute_dual_up_down()
        # elif pose == 23:
        #     self._execute_dual_alternate()
        # elif pose == 24:
        #     self._execute_dual_punch()
        # elif pose == 25:
        #     self._execute_dual_go_to_home()
        if pose == 10:
            self._execute_left_punch()
        elif pose == 11:
            self._execute_left_swing_forward()
        elif pose == 12:
            self._execute_left_swing_lateral()
        elif pose == 13:
            self._execute_left_raise()
        elif pose == 14:
            self._execute_left_wave()
        elif pose == 20:
            self._execute_right_punch()
        elif pose == 21:
            self._execute_right_swing_forward()
        elif pose == 22:
            self._execute_right_swing_lateral()
        elif pose == 23:
            self._execute_right_raise()
        elif pose == 24:
            self._execute_right_wave()
        elif pose == 0:
            self._execute_dual_go_to_home()
        else:
            rospy.logwarn(f"Unknown pose: {pose}")
    
    # ==================== Right Arm Motions ====================
    
    def _execute_right_wave(self):
        """Right arm waving motion"""
        for i in range(3):
            self.arm_R.set_named_target('R_wave_start')
            self.arm_R.go()
            self.arm_R.set_named_target('R_wave_end')
            self.arm_R.go()
        self.arm_R.set_named_target('Rhome')
        self.arm_R.go()
    
    def _execute_right_punch(self):
        """Right arm punching motion"""
        for i in range(3):
            self.arm_R.set_named_target('R_punch')
            self.arm_R.go()
            self.arm_R.set_named_target('Rhome')
            self.arm_R.go()
    
    def _execute_right_raise(self):
        """Right arm raising motion"""
        for i in range(3):
            self.arm_R.set_named_target('R_raise')
            self.arm_R.go()
            self.arm_R.set_named_target('Rhome')
            self.arm_R.go()
    
    def _execute_right_wave_bell(self):
        """Right arm waving with bell interaction"""
        for i in range(3):
            self.arm_R.set_named_target('R_waveb')
            self.arm_R.go()
            self.arm_R.set_named_target('R_d_bell')
            self.arm_R.go()
        self.arm_R.set_named_target('Rhome')
        self.arm_R.go()
    
    # ==================== Left Arm Motions ====================
    
    def _execute_left_wave(self):
        """Left arm waving motion"""
        for i in range(3):
            self.arm_L.set_named_target('L_wave_start')
            self.arm_L.go()
            self.arm_L.set_named_target('L_wave_end')
            self.arm_L.go()
        self.arm_L.set_named_target('Lhome')
        self.arm_L.go()
    
    def _execute_left_punch(self):
        """Left arm punching motion"""
        for i in range(3):
            self.arm_L.set_named_target('L_punch')
            self.arm_L.go()
            self.arm_L.set_named_target('Lhome')
            self.arm_L.go()
    
    def _execute_left_raise(self):
        """Left arm raising motion"""
        for i in range(3):
            self.arm_L.set_named_target('L_raise')
            self.arm_L.go()
            self.arm_L.set_named_target('Lhome')
            self.arm_L.go()
    
    def _execute_left_wave_bell(self):
        """Left arm waving with bell interaction"""
        for i in range(3):
            self.arm_L.set_named_target('L_waveb')
            self.arm_L.go()
            self.arm_L.set_named_target('L_d_bell')
            self.arm_L.go()
        self.arm_L.set_named_target('Lhome')
        self.arm_L.go()
    
    # ==================== Dual Arm Motions ====================
    
    def _execute_dual_clap(self):
        """Dual arm clapping motion"""
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
        """Dual arm up-down motion"""
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
        """Dual arm alternate motion"""
        for i in range(3):
            self.arm_D.set_named_target('L_down_R_up')
            self.arm_D.go()
            self.arm_D.set_named_target('R_down_L_up')
            self.arm_D.go()
        self.arm_D.set_named_target('D_home')
        self.arm_D.go()
    
    def _execute_dual_punch(self):
        """Dual arm punch motion"""
        for i in range(3):
            self.arm_D.set_named_target('d_punch1')
            self.arm_D.go()
            self.arm_D.set_named_target('d_punch2')
            self.arm_D.go()
        
        self.arm_D.set_named_target('D_home')
        self.arm_D.go()
    
    def _execute_dual_go_to_home(self):
        """Dual arm go to home motion"""
        self.arm_D.set_named_target('D_home')
        self.arm_D.go()
        
    # ==================== Swing Motions ====================
    def _execute_right_swing_lateral(self):
        for _ in range(3):
            self.arm_R.set_named_target(f"R_waveb")
            self.arm_R.go()
            rospy.sleep(2.0)
            self.arm_R.set_named_target(f"R_d_bell")
            self.arm_R.go()
    
    def _execute_left_swing_lateral(self):
        for _ in range(3):
            self.arm_L.set_named_target(f"L_waveb")
            self.arm_L.go()
            rospy.sleep(2.0)
            self.arm_L.set_named_target(f"L_d_bell")
            self.arm_L.go()
    
    def _execute_left_swing_forward(self):
        for _ in range(3):
            self.arm_L.set_named_target(f"L_swing_fwd")
            self.arm_L.go()
            self.arm_L.set_named_target(f"L_swing_bwd")
            self.arm_L.go()
    
    def _execute_right_swing_forward(self):
        # placeholder: forward/backward swing implementation
        for _ in range(3):
            self.arm_R.set_named_target(f"R_swing_fwd")
            self.arm_R.go()
            self.arm_R.set_named_target(f"R_swing_bwd")
            self.arm_R.go()