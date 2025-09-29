#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy, sys
import moveit_commander
import paho.mqtt.client as mqtt
from std_msgs.msg import Int32, String
import threading

# Import our motion executor
from robot_motion_executor import RobotMotionExecutor

class FloRobotController:
    """
    Main robot controller - handles MQTT communication, AprilTag data, and delegates motion execution
    """
    
    def __init__(self):
        """Initialize the robot controller system"""
        
        # ==================== MQTT Client Initialization ====================
        self.client = mqtt.Client()
        self.broker_ip = "localhost"
        self.client.connect(self.broker_ip, 1883, 60)
        
        # ==================== Control Variables ====================
        self.mode = "0"  # Current motion command mode
        
        # AprilTag position tracking
        self.apriltag_positions = {
            'position_dbx': 0, 'position_dby': 0,  # Down bell position
            'position_cx': 0, 'position_cy': 0,    # Cup position  
            'position_bx': 0, 'position_by': 0,    # Brush position
            'position_rx': 0, 'position_ry': 0,    # Right arm reference
            'position_lx': 0, 'position_ly': 0     # Left arm reference
        }
        
        # ==================== ROS and MoveIt Initialization ====================
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('flo_robot_controller')
        
        # Initialize gripper publishers
        self.rgripper_pub = rospy.Publisher('/rgripper', Int32, queue_size=10)
        self.lgripper_pub = rospy.Publisher('/lgripper', Int32, queue_size=10)
        
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
            self.rgripper_pub, self.lgripper_pub,
            self.end_effector_link_R, self.end_effector_link_L, self.end_effector_link_D
        )
        
        # ==================== ROS Subscribers ====================
        rospy.Subscriber("/apriltag_info", String, self.apriltag_callback)
        
        # ==================== Start MQTT Client ====================
        mqtt_thread = threading.Thread(target=self.start_mqtt_client)
        mqtt_thread.start()
        
        # ==================== Main Control Loop ====================
        rospy.loginfo("FloRobotController initialized. Waiting for commands...")
        
        while not rospy.is_shutdown():
            if self.mode != "0":
                rospy.loginfo(f"Executing motion command: {self.mode}")
                
                # Update motion executor with latest AprilTag positions
                self.motion_executor.update_apriltag_positions(self.apriltag_positions)
                
                # Execute the motion
                try:
                    self.motion_executor.execute_pose(int(self.mode), reference_frame)
                    rospy.loginfo(f"Motion {self.mode} completed successfully")
                    self.client.publish("ros/mqtt/feedback", "A")  # Success feedback
                except Exception as e:
                    rospy.logerr(f"Motion execution failed: {e}")
                    self.client.publish("ros/mqtt/feedback", "E")  # Error feedback
                
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
            arm.set_goal_position_tolerance(0.001)
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
            rospy.loginfo(f"Received MQTT command: {command}")
            self.mode = command
        
        def on_connect(client, userdata, flags, rc):
            """Handle MQTT connection"""
            if rc == 0:
                rospy.loginfo("Connected to MQTT broker successfully")
            else:
                rospy.logerr(f"Failed to connect to MQTT broker: {rc}")
        
        def on_disconnect(client, userdata, rc):
            """Handle MQTT disconnection"""
            rospy.logwarn("Disconnected from MQTT broker")
        
        # Set up MQTT callbacks
        self.client.on_message = on_message
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        
        # Subscribe to movement commands
        self.client.subscribe("ros/mqtt/movement")
        
        rospy.loginfo("MQTT client started. Waiting for movement commands...")
        self.client.loop_forever()
    
    def apriltag_callback(self, data):
        """Process AprilTag position information"""
        try:
            # Parse AprilTag data
            cleaned_data = data.data.replace('[', '').replace(']', '').strip()
            position_data = cleaned_data.split()
            
            if len(position_data) >= 3:
                tag_id = position_data[0]
                x_pos = float(position_data[1])
                y_pos = float(position_data[2])
                
                # Update positions based on tag ID
                position_mapping = {
                    "0": ('position_dbx', 'position_dby'),  # Down bell
                    "2": ('position_rx', 'position_ry'),    # Right arm reference
                    "3": ('position_cx', 'position_cy'),    # Cup
                    "5": ('position_lx', 'position_ly'),    # Left arm reference  
                    "6": ('position_bx', 'position_by')     # Brush
                }
                
                if tag_id in position_mapping:
                    x_key, y_key = position_mapping[tag_id]
                    self.apriltag_positions[x_key] = x_pos
                    self.apriltag_positions[y_key] = y_pos
                    rospy.logdebug(f"Updated AprilTag {tag_id}: ({x_pos}, {y_pos})")
                    
        except (ValueError, IndexError) as e:
            rospy.logwarn(f"Failed to parse AprilTag data: {e}")

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
