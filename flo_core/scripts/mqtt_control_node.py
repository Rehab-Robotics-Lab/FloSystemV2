#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#mqtt_control_node.py
"""
MQTT Control Node for Flo Robot
This script initializes an MQTT client to receive motion commands and LED control messages,
and executes the corresponding robot motions using MoveIt.
"""
import os
import sys
import threading
import time
from collections import deque

import actionlib
import moveit_commander
import moveit_msgs.msg
import rospy

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from flo_core.mqtt_config import MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_BROKER_CLIENT
from flo_core.led_controller import LedController
from flo_core.motion_executor import RobotMotionExecutor

class FloRobotController:
    """
    Main robot controller - handles MQTT communication and delegates motion execution
    """
    
    def __init__(self):
        """Initialize the robot controller system"""
        
        # ==================== MQTT Client Initialization ====================
        self.client = MQTT_BROKER_CLIENT
        self.broker_host = MQTT_BROKER_HOST
        self.broker_port = MQTT_BROKER_PORT
        print("Connecting to MQTT broker...")
        self.client.connect(self.broker_host, self.broker_port, 60)
        print("MQTT connected.")
        
        # ==================== Control Variables ====================
        self._queue_lock = threading.Lock()
        self._command_queue = deque()
        self.mode = "0"  # Current motion command mode (legacy/diagnostic)
        self.topic_movement = "ros/mqtt/movement"
        self.topic_led = "ros/mqtt/led"
        self.topic_feedback = "ros/mqtt/feedback"
        self.topic_action_done = "ros/mqtt/action_done"
        self.topic_action_time = "ros/mqtt/action_time"
        self.topic_queue_length = "ros/mqtt/queue_length"
        self.topic_queue_state = "ros/mqtt/queue_state"
        
        
        # ==================== ROS and MoveIt Initialization ====================
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('flo_robot_controller')

        # Ensure move_group action server is available before MoveGroupCommander init.
        self._wait_for_move_group_server()
        
        # Initialize MoveIt groups
        self.arm_R = self._create_move_group_commander('R')
        self.arm_L = self._create_move_group_commander('L')
        self.arm_D = self._create_move_group_commander('dual')
        
        # Set reference frame
        reference_frame = 'world'
        self.arm_R.set_pose_reference_frame(reference_frame)
        self.arm_L.set_pose_reference_frame(reference_frame)
        self.arm_D.set_pose_reference_frame(reference_frame)
        
        # Configure motion planning parameters
        self._configure_motion_planning()
        
        # Get end effector links
        self.end_effector_link_R = self.arm_R.get_end_effector_link()
        self.end_effector_link_L = self.arm_L.get_end_effector_link()
        self.end_effector_link_D = self.arm_D.get_end_effector_link()
        
        # ==================== Initialize Motion Executor ====================
        self.motion_executor = RobotMotionExecutor(
            self.arm_R, self.arm_L, self.arm_D,
            self.end_effector_link_R, self.end_effector_link_L, self.end_effector_link_D
        )
        self.led_controller = LedController()
        rospy.on_shutdown(self._shutdown)
        
        
        # ==================== Start MQTT Client ====================
        mqtt_thread = threading.Thread(target=self.start_mqtt_client, daemon=True)
        mqtt_thread.start()
        
        # ==================== Main Control Loop ====================
        rospy.loginfo("FloRobotController initialized. Waiting for commands...")
        
        while not rospy.is_shutdown():
            command_entry = None
            with self._queue_lock:
                if self._command_queue:
                    command_entry = self._command_queue.popleft()
                queue_len = len(self._command_queue)
                queue_state = ",".join(cmd for cmd, _ in self._command_queue)

            if command_entry:
                command, start_time = command_entry
                self.mode = command
                rospy.loginfo(f"Executing motion command: {command}")
                self.client.publish(self.topic_queue_length, str(queue_len))
                self.client.publish(self.topic_queue_state, queue_state)
                
                # Execute the motion
                try:
                    start_time = time.monotonic()
                    self.motion_executor.execute_pose(int(command))
                    rospy.loginfo(f"Motion {command} completed successfully")
                    self.client.publish(self.topic_feedback, "A")  # Success feedback
                    self.client.publish(self.topic_action_done, f"done:{command}")
                except Exception as e:
                    rospy.logerr(f"Motion execution failed: {e}")
                    self.client.publish(self.topic_feedback, "E")  # Error feedback
                    self.client.publish(self.topic_action_done, f"error:{command}")
                finally:
                    elapsed = time.monotonic() - start_time
                    self.client.publish(self.topic_action_time, f"{command},{elapsed:.3f}")
                
                self.mode = "0"  # Reset to idle
            
            rospy.sleep(0.1)  # Small sleep to prevent CPU overload
        
        # ==================== Cleanup ====================
        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)
    
    def _configure_motion_planning(self):
        """Configure motion planning parameters for all arm groups"""
        arms = [self.arm_R, self.arm_L, self.arm_D]
        
        for arm in arms:
            arm.allow_replanning(True)
            arm.set_goal_joint_tolerance(0.1)
            arm.set_goal_position_tolerance(0.1)
            arm.set_goal_orientation_tolerance(0.1)
            arm.set_max_acceleration_scaling_factor(0.6)
        
        # Set specific velocity scaling
        self.arm_R.set_max_velocity_scaling_factor(1.0)
        self.arm_L.set_max_velocity_scaling_factor(1.0)
        self.arm_D.set_max_velocity_scaling_factor(0.8)

    def _wait_for_move_group_server(self):
        """Wait for move_group action server to come up to avoid init-time failures."""
        timeout_s = rospy.get_param("~move_group_wait_seconds", 30.0)
        retries = int(rospy.get_param("~move_group_wait_retries", 3))
        action_name = rospy.get_param("~move_group_action", "/move_group")
        for attempt in range(1, retries + 1):
            client = actionlib.SimpleActionClient(action_name, moveit_msgs.msg.MoveGroupAction)
            rospy.loginfo(
                "Waiting for move_group action server (attempt %d/%d, timeout %.1fs)...",
                attempt,
                retries,
                timeout_s,
            )
            if client.wait_for_server(rospy.Duration(timeout_s)):
                return
            rospy.logwarn("move_group action server not available yet.")
        raise rospy.ROSException("move_group action server not available after retries")

    def _create_move_group_commander(self, group_name):
        """Create MoveGroupCommander with a configurable server wait to avoid 5s init timeouts."""
        if rospy.has_param("~move_group_commander_wait_seconds"):
            timeout_s = float(rospy.get_param("~move_group_commander_wait_seconds"))
        else:
            timeout_s = float(rospy.get_param("~move_group_init_seconds", 0.0))
        ns = rospy.get_param("~move_group_ns", "")
        kwargs = {"wait_for_servers": timeout_s}
        if ns:
            kwargs["ns"] = ns
        try:
            return moveit_commander.MoveGroupCommander(group_name, **kwargs)
        except TypeError:
            if ns:
                try:
                    return moveit_commander.MoveGroupCommander(group_name, ns=ns)
                except TypeError:
                    pass
            return moveit_commander.MoveGroupCommander(group_name)
    
    def start_mqtt_client(self):
        """Initialize and start MQTT client for receiving motion commands"""
        
        def on_message(client, userdata, message):
            """Handle incoming MQTT messages"""
            command = message.payload.decode().strip()
            if message.topic == self.topic_movement:
                rospy.loginfo(f"Received motion command: {command}")
                with self._queue_lock:
                    self._command_queue.append((command, time.monotonic()))
                    queue_len = len(self._command_queue)
                    queue_state = ",".join(cmd for cmd, _ in self._command_queue)
                self.client.publish(self.topic_queue_length, str(queue_len))
                self.client.publish(self.topic_queue_state, queue_state)
            elif message.topic == self.topic_led:
                rospy.loginfo(f"Received LED command: {command}")
                if not self.led_controller.set_led_state(command):
                    rospy.logwarn("LED controller unavailable; ignoring LED command.")
            else:
                rospy.logwarn(f"Ignoring message from unknown topic: {message.topic}")
        
        def on_connect(client, userdata, flags, reason_code, properties):
            """Handle MQTT connection"""
            if reason_code == 0:
                rospy.loginfo("Connected to MQTT broker successfully")
            else:
                rospy.logerr(f"Failed to connect to MQTT broker: {reason_code}")
        
        def on_disconnect(client, userdata, *args, **kwargs):
            """Handle MQTT disconnection (compatible with paho-mqtt v1/v2)."""
            rospy.logwarn("Disconnected from MQTT broker")
        
        # Set up MQTT callbacks
        self.client.on_message = on_message
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        
        # Subscribe to movement and LED commands
        self.client.subscribe([(self.topic_movement, 0), (self.topic_led, 0)])
        
        rospy.loginfo("MQTT client started. Waiting for movement commands...")
        self.client.loop_start()
        while not rospy.is_shutdown():
            rospy.sleep(0.1)

    def _shutdown(self):
        """Cleanup resources on shutdown."""
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except Exception:
            pass
        self.led_controller.close()

def main():
    """Main entry point"""
    try:
        controller = FloRobotController()
    except rospy.ROSInterruptException:
        rospy.loginfo("Robot controller interrupted")
    except KeyboardInterrupt:
        rospy.loginfo("Robot controller stopped by user")
    except Exception as e:
        rospy.logerr(f"Robot controller failed: {e}")

if __name__ == "__main__":
    main()
