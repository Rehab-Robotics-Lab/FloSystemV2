#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import JointState

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
        self._last_joint_state_stamp = None
        self._stop_requested = False
        self._pose_actions = {
            10: self._execute_left_punch,
            11: self._execute_left_swing_forward,
            12: self._execute_left_swing_lateral,
            13: self._execute_left_raise,
            14: self._execute_left_wave,
            15: self._execute_left_reach_side,
            20: self._execute_right_punch,
            21: self._execute_right_swing_forward,
            22: self._execute_right_swing_lateral,
            23: self._execute_right_raise,
            24: self._execute_right_wave,
            25: self._execute_right_reach_side,
            0:  self._execute_dual_go_to_home,
            30: self._execute_dual_clap,
            31: self._execute_dual_up_down,
            32: self._execute_dual_alternate,
            33: self._execute_dual_punch,
            -1: self.stop,
        }  

    def _sync_start_state(self, group, timeout=0.2, retries=2):
        """
        Ensure the planning start state matches the latest joint state.
        """
        per_attempt_timeout = max(0.05, timeout / max(1, retries))
        for _ in range(max(1, retries)):
            try:
                msg = rospy.wait_for_message('/joint_states', JointState, timeout=per_attempt_timeout)
                if msg.header.stamp and (self._last_joint_state_stamp is None or msg.header.stamp > self._last_joint_state_stamp):
                    self._last_joint_state_stamp = msg.header.stamp
                    break
                rospy.logwarn("Received stale /joint_states, waiting for a newer update.")
            except rospy.ROSException:
                rospy.logwarn("No fresh /joint_states received before planning.")
                break
        group.set_start_state_to_current_state()

    #################################
    ####### Execute Actions #########
    #################################
    def execute_pose(self, pose):
        if pose in self._pose_actions:
            self._pose_actions[pose]()
        elif pose >= 111 and pose <= 115:
            base_pose = pose - 100
            self._execute_repeated(self._pose_actions[base_pose], times=10)
        else:
            rospy.logwarn(f"Unknown pose: {pose}")

    

    def _execute_repeated(self, action_func, times=10):
        """Execute repeated action, can be stopped by user"""
        self._stop_requested = False
        for i in range(times):
            if self._stop_requested:
                rospy.loginfo("Motion stopped by user")
                break
            action_func()
        self._stop_requested = False
    # ==================== Right Arm Motions ====================
    def stop(self):
        """Request to stop the current action and halt robot immediately"""
        self._stop_requested = True
        # Stop all MoveIt groups immediately
        self.arm_R.stop()
        self.arm_L.stop()
        self.arm_D.stop()
        rospy.loginfo("Stop requested - all arms halted")

        
    def _execute_right_wave(self):
        """Right arm waving motion"""
        for i in range(3):
            self.arm_R.set_named_target('R_wave_start')
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
            self.arm_R.set_named_target('R_wave_end')
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
        self.arm_R.set_named_target('Rhome')
        self._sync_start_state(self.arm_R)
        self.arm_R.go()
    
    def _execute_right_punch(self):
        """Right arm punching motion"""
        for i in range(3):
            self.arm_R.set_named_target('R_punch')
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
            self.arm_R.set_named_target('Rhome')
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
    
    def _execute_right_raise(self):
        """Right arm raising motion"""
        for i in range(3):
            self.arm_R.set_named_target('R_raise')
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
            self.arm_R.set_named_target('Rhome')
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
    
    def _execute_right_wave_bell(self):
        """Right arm waving with bell interaction"""
        for i in range(3):
            self.arm_R.set_named_target('R_waveb')
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
            self.arm_R.set_named_target('R_d_bell')
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
        self.arm_R.set_named_target('Rhome')
        self._sync_start_state(self.arm_R)
        self.arm_R.go()
    
    # ==================== Left Arm Motions ====================
    
    def _execute_left_wave(self):
        """Left arm waving motion"""
        for i in range(3):
            self.arm_L.set_named_target('L_wave_start')
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
            self.arm_L.set_named_target('L_wave_end')
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
        self.arm_L.set_named_target('Lhome')
        self._sync_start_state(self.arm_L)
        self.arm_L.go()
    
    def _execute_left_punch(self):
        """Left arm punching motion"""
        for i in range(3):
            self.arm_L.set_named_target('L_punch')
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
            self.arm_L.set_named_target('Lhome')
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
    
    def _execute_left_raise(self):
        """Left arm raising motion"""
        for i in range(3):
            self.arm_L.set_named_target('L_raise')
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
            self.arm_L.set_named_target('Lhome')
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
    
    def _execute_left_wave_bell(self):
        """Left arm waving with bell interaction"""
        for i in range(3):
            self.arm_L.set_named_target('L_waveb')
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
            self.arm_L.set_named_target('L_d_bell')
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
        self.arm_L.set_named_target('Lhome')
        self._sync_start_state(self.arm_L)
        self.arm_L.go()
    
    # ==================== Dual Arm Motions ====================
    
    def _execute_dual_clap(self):
        """Dual arm clapping motion"""
        self.arm_D.set_named_target('clap')
        self._sync_start_state(self.arm_D)
        self.arm_D.go()
        for i in range(3):
            self.arm_D.set_named_target('clap_close')
            self._sync_start_state(self.arm_D)
            self.arm_D.go()
            self.arm_D.set_named_target('clap_open')
            self._sync_start_state(self.arm_D)
            self.arm_D.go()
        self.arm_D.set_named_target('clap')
        self._sync_start_state(self.arm_D)
        self.arm_D.go()
        self.arm_D.set_named_target('D_home')
        self._sync_start_state(self.arm_D)
        self.arm_D.go()
    
    def _execute_dual_up_down(self):
        """Dual arm up-down motion"""
        for i in range(3):
            self.arm_D.set_named_target('D_up')
            self._sync_start_state(self.arm_D)
            self.arm_D.go()
            self.arm_D.set_named_target('D_down')
            self._sync_start_state(self.arm_D)
            self.arm_D.go()
        self.arm_D.set_named_target('D_up')
        self._sync_start_state(self.arm_D)
        self.arm_D.go()
        self.arm_D.set_named_target('D_home')
        self._sync_start_state(self.arm_D)
        self.arm_D.go()
    
    def _execute_dual_alternate(self):
        """Dual arm alternate motion"""
        for i in range(3):
            self.arm_D.set_named_target('L_down_R_up')
            self._sync_start_state(self.arm_D)
            self.arm_D.go()
            self.arm_D.set_named_target('R_down_L_up')
            self._sync_start_state(self.arm_D)
            self.arm_D.go()
        self.arm_D.set_named_target('D_home')
        self._sync_start_state(self.arm_D)
        self.arm_D.go()
    
    def _execute_dual_punch(self):
        """Dual arm punch motion"""
        for i in range(3):
            self.arm_D.set_named_target('d_punch1')
            self._sync_start_state(self.arm_D)
            self.arm_D.go()
            self.arm_D.set_named_target('d_punch2')
            self._sync_start_state(self.arm_D)
            self.arm_D.go()
        
        self.arm_D.set_named_target('D_home')
        self._sync_start_state(self.arm_D)
        self.arm_D.go()
    
    def _execute_dual_go_to_home(self):
        """Dual arm go to home motion"""
        self.arm_D.set_named_target('D_home')
        self._sync_start_state(self.arm_D)
        self.arm_D.go()
        
    # ==================== Swing Motions ====================
    def _execute_right_swing_lateral(self):
        for _ in range(3):
            self.arm_R.set_named_target(f"R_waveb")
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
            # rospy.sleep(2.0)
            self.arm_R.set_named_target(f"R_d_bell")
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
        self.arm_R.set_named_target('Rhome')
        self._sync_start_state(self.arm_R)
        self.arm_R.go()
    
    def _execute_left_swing_lateral(self):
        for _ in range(3):
            self.arm_L.set_named_target(f"L_waveb")
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
            # rospy.sleep(2.0)
            self.arm_L.set_named_target(f"L_d_bell")
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
        self.arm_L.set_named_target('Lhome')
        self._sync_start_state(self.arm_L)
        self.arm_L.go()
    
    def _execute_left_swing_forward(self):
        for _ in range(3):
            self.arm_L.set_named_target(f"L_swing_fwd")
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
            self.arm_L.set_named_target(f"L_swing_bwd")
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
        self.arm_L.set_named_target('Lhome')
        self._sync_start_state(self.arm_L)
        self.arm_L.go()
    
    def _execute_right_swing_forward(self):
        # placeholder: forward/backward swing implementation
        for _ in range(3):
            self.arm_R.set_named_target(f"R_swing_fwd")
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
            self.arm_R.set_named_target(f"R_swing_bwd")
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
        self.arm_R.set_named_target('Rhome')
        self._sync_start_state(self.arm_R)
        self.arm_R.go()


    def _execute_left_reach_side(self):
        for _ in range(3):
            self.arm_L.set_named_target('L_reach_side')
            self._sync_start_state(self.arm_L)
            self.arm_L.go()
            rospy.sleep(2.0)
        self.arm_L.set_named_target('Lhome')
        self._sync_start_state(self.arm_L)
        self.arm_L.go()

    def _execute_right_reach_side(self):
        for _ in range(3):
            self.arm_R.set_named_target('R_reach_side')
            self._sync_start_state(self.arm_R)
            self.arm_R.go()
            rospy.sleep(2.0)
        self.arm_R.set_named_target('Rhome')
        self._sync_start_state(self.arm_R)
        self.arm_R.go()
