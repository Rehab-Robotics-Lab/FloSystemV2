#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import threading

import moveit_commander
import paho.mqtt.client as mqtt
import rospy

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from flo_core.led_controller import LedController
from flo_core.motion_executor import RobotMotionExecutor

class FloRobotController:
    """
    Main robot controller - handles MQTT communication and delegates motion execution
    """
    
    def __init__(self):
        """Initialize the robot controller system"""
        
        # ==================== MQTT Client Initialization ====================
        # self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client = mqtt.Client()
        self.broker_host = os.environ.get("MQTT_BROKER_HOST", "host.docker.internal")
        self.broker_port = int(os.environ.get("MQTT_BROKER_PORT", "1883"))
        self.client.connect(self.broker_host, self.broker_port, 60)
        
        # ==================== Control Variables ====================
        self.mode = "0"  # Current motion command mode
        self.topic_movement = "ros/mqtt/movement"
        self.topic_led = "ros/mqtt/led"
        self.topic_feedback = "ros/mqtt/feedback"
        self.topic_action_done = "ros/mqtt/action_done"
        
        
        # ==================== ROS and MoveIt Initialization ====================
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('flo_robot_controller')
        
        # Initialize MoveIt groups
        self.arm_R = moveit_commander.MoveGroupCommander('R')
        self.arm_L = moveit_commander.MoveGroupCommander('L') 
        self.arm_D = moveit_commander.MoveGroupCommander('dual')
        
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
        mqtt_thread = threading.Thread(target=self.start_mqtt_client)
        mqtt_thread.start()
        
        # ==================== Main Control Loop ====================
        rospy.loginfo("FloRobotController initialized. Waiting for commands...")
        
        while not rospy.is_shutdown():
            if self.mode != "0":
                rospy.loginfo(f"Executing motion command: {self.mode}")
                
                # Execute the motion
                try:
                    self.motion_executor.execute_pose(int(self.mode))
                    rospy.loginfo(f"Motion {self.mode} completed successfully")
                    self.client.publish(self.topic_feedback, "A")  # Success feedback
                    self.client.publish(self.topic_action_done, f"done:{self.mode}")
                except Exception as e:
                    rospy.logerr(f"Motion execution failed: {e}")
                    self.client.publish(self.topic_feedback, "E")  # Error feedback
                    self.client.publish(self.topic_action_done, f"error:{self.mode}")
                
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
            arm.set_goal_joint_tolerance(0.02)
            arm.set_goal_position_tolerance(0.005)
            arm.set_goal_orientation_tolerance(1)
            arm.set_max_acceleration_scaling_factor(0.6)
        
        # Set specific velocity scaling
        self.arm_R.set_max_velocity_scaling_factor(0.5)
        self.arm_L.set_max_velocity_scaling_factor(0.5)
        self.arm_D.set_max_velocity_scaling_factor(0.8)
    
    def start_mqtt_client(self):
        """Initialize and start MQTT client for receiving motion commands"""
        
        def on_message(client, userdata, message):
            """Handle incoming MQTT messages"""
            command = message.payload.decode().strip()
            if message.topic == self.topic_movement:
                rospy.loginfo(f"Received motion command: {command}")
                self.mode = command
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
        
        def on_disconnect(client, userdata, reason_code, properties):
            """Handle MQTT disconnection"""
            rospy.logwarn("Disconnected from MQTT broker")
        
        # Set up MQTT callbacks
        self.client.on_message = on_message
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        
        # Subscribe to movement and LED commands
        self.client.subscribe([(self.topic_movement, 0), (self.topic_led, 0)])
        
        rospy.loginfo("MQTT client started. Waiting for movement commands...")
        self.client.loop_forever()

    def _shutdown(self):
        """Cleanup resources on shutdown."""
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
