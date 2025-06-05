#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy, sys
import moveit_commander
from geometry_msgs.msg import PoseStamped
import paho.mqtt.client as mqtt
from std_msgs.msg import Int32 , String

import math
import threading



class MoveItIkDemo:
    def __init__(self):
        """
        Initialize the MoveItIkDemo class, setting up the MQTT client, ROS node,
        MoveIt groups for robotic arms, gripper control, and planning settings.
        """
        # ==================== MQTT Client Initialization ====================
        self.client = mqtt.Client()
        self.broker_ip = "localhost"  # Broker listens on all available network interfaces
        self.client.connect(self.broker_ip, 1883, 60)  # Connect to MQTT broker on port 1883
        # MQTT is used to receive motion commands and send feedback to external clients.

        # ==================== Gripper Control Values ====================
        # Predefined positions for gripper control (right and left hands)
        self.gripper_cup_r = 3410  # Gripper position to hold a cup (right)
        self.gripper_cup_l = 3710  # Gripper position to hold a cup (left)
        self.gripper_off_l = 3700  # Gripper release position (left)
        self.gripper_brush_l = 3710  # Gripper for holding a brush (left)
        self.gripper_brush_r = 3410  # Gripper for holding a brush (right)

        self.gripper_on = 1300  # Gripper closed position
        self.gripper_off = 3410  # Gripper open position

        # ==================== Default Mode and Position Parameters ====================
        self.mode = "0"  # Default mode; "0" indicates idle state

        # Arm length and predefined coordinates for different object positions
        self.arm_len = 150  # Arm length in millimeters
        self.arm_x = 0.09909856  # Default X-coordinate for the arm
        self.arm_y = -0.00930597  # Default Y-coordinate for the arm

        # Initial positions for detected objects (e.g., cup, brush, and bell)
        self.position_dbx = self.position_dby = 0  # Down bell position
        self.position_cx = self.position_cy = 0    # Cup position
        self.position_bx = self.position_by = 0    # Brush position
        self.position_rx = self.position_ry = 0    # Right arm reference position
        self.position_lx = self.position_ly = 0    # Left arm reference position

        # ==================== ROS and MoveIt Initialization ====================
        # Initialize the MoveIt Commander API
        moveit_commander.roscpp_initialize(sys.argv)

        # Initialize the ROS node
        rospy.init_node('moveit_ik_demo')

        # Publishers for right and left grippers
        self.rgripper_pub = rospy.Publisher('/rgripper', Int32, queue_size=10)
        self.lgripper_pub = rospy.Publisher('/lgripper', Int32, queue_size=10)

        # Initialize MoveIt groups for right arm, left arm, and dual arms
        self.arm_R = moveit_commander.MoveGroupCommander('R')  # Right arm group
        self.arm_L = moveit_commander.MoveGroupCommander('L')  # Left arm group
        self.arm_D = moveit_commander.MoveGroupCommander('dual')  # Dual arm group

        # ==================== Reference Frames and End Effectors ====================
        # Retrieve the end-effector links for all arms
        self.end_effector_link_R = self.arm_R.get_end_effector_link()
        self.end_effector_link_L = self.arm_L.get_end_effector_link()
        self.end_effector_link_D = self.arm_D.get_end_effector_link()

        # Set the reference coordinate frame for all motion
        reference_frame = 'world'
        self.arm_R.set_pose_reference_frame(reference_frame)
        self.arm_L.set_pose_reference_frame(reference_frame)
        self.arm_D.set_pose_reference_frame(reference_frame)

        # ==================== Motion Planning Settings ====================
        # Allow replanning if the motion plan fails
        self.arm_R.allow_replanning(True)
        self.arm_L.allow_replanning(True)
        self.arm_D.allow_replanning(True)

        # Set position and orientation tolerance for motion planning
        self.arm_R.set_goal_position_tolerance(0.001)
        self.arm_R.set_goal_orientation_tolerance(1)
        self.arm_L.set_goal_position_tolerance(0.001)
        self.arm_L.set_goal_orientation_tolerance(1)
        self.arm_D.set_goal_position_tolerance(0.001)
        self.arm_D.set_goal_orientation_tolerance(1)

        # Set the maximum velocity and acceleration scaling factors for the arms
        self.arm_R.set_max_acceleration_scaling_factor(0.6)
        self.arm_R.set_max_velocity_scaling_factor(0.5)
        self.arm_L.set_max_acceleration_scaling_factor(0.6)
        self.arm_L.set_max_velocity_scaling_factor(0.5)
        self.arm_D.set_max_acceleration_scaling_factor(0.6)
        self.arm_D.set_max_velocity_scaling_factor(0.8)

        # ==================== ROS Subscriber for AprilTag Information ====================
        # Subscribe to the topic that provides AprilTag positional information
        rospy.Subscriber("/apriltag_info", String, self.callback)

        # ==================== Start MQTT Client in a Separate Thread ====================
        # Start the MQTT client in a background thread to listen for incoming messages
        mqtt_thread = threading.Thread(target=self.start_mqtt_client)
        mqtt_thread.start()

        # ==================== Main Execution Loop ====================
        # Main loop: Wait for motion commands and execute them
        while not rospy.is_shutdown():
            if self.mode != "0":  # If a new mode (motion command) is received
                self.move(int(self.mode), reference_frame)  # Execute the move function
                self.mode = "0"  # Reset mode to idle after execution
                self.client.publish("ros/mqtt/feedback", "A")  # Publish feedback to MQTT
            rospy.sleep(1)  # Prevent CPU overutilization with sleep

        # ==================== Shutdown MoveIt Commander ====================
        moveit_commander.roscpp_shutdown()  # Shutdown MoveIt API
        moveit_commander.os._exit(0)        # Exit the program safely

    

    def start_mqtt_client(self):
        """
        Initializes and starts the MQTT client to listen for motion commands.
        Subscribes to the MQTT topic 'ros/mqtt/movement' and processes received messages.
        """

        # ==================== Define Callback for Incoming Messages ====================
        def on_message(client, userdata, message):
            """
            Callback function to handle incoming MQTT messages.
            :param client: The MQTT client instance.
            :param userdata: User data (not used here).
            :param message: The MQTT message containing the payload.
            """
            print(f"Received message: {message.payload.decode()}")  # Log the received message
            self.mode = str(message.payload.decode())  # Update the mode based on the received message

        # ==================== Set Up Callback ====================
        # Assign the callback function for incoming messages
        self.client.on_message = on_message

        # ==================== Subscribe to Topic ====================
        # Subscribe to the MQTT topic where motion commands will be received
        self.client.subscribe("ros/mqtt/movement")

        # ==================== Start MQTT Client Loop ====================
        # Start the MQTT client loop to continuously listen for messages
        print("Waiting for messages...")  # Inform the user that the client is ready
        self.client.loop_forever()  # Run the client in an infinite loop to wait for incoming messages


    def callback(self, data):
        """
        Callback function to process position information received from the AprilTag detection topic.
        Updates the positions of detected objects (e.g., bell, cup, brush) based on the received data.

        :param data: ROS message containing position information as a string.
        """
        # ==================== Process Received Data ====================
        # rospy.loginfo("Received AprilTag position: %s", data.data)  # Debug log for received data (optional)
        
        # Clean the string data by removing square brackets and extra spaces
        cleaned_data = data.data.replace('[', '').replace(']', '').strip()
        
        # Split the cleaned string into a list of values
        self.position = [x for x in cleaned_data.split()]
        
        # ==================== Update Object Positions ====================
        # Update specific object positions based on the first value (ID) in the data
        if self.position[0] == "0":  # ID "0" represents the down bell
            self.position_dbx = float(self.position[1])  # Update X-coordinate
            self.position_dby = float(self.position[2])  # Update Y-coordinate
        elif self.position[0] == "3":  # ID "3" represents the cup
            self.position_cx = float(self.position[1])  # Update X-coordinate
            self.position_cy = float(self.position[2])  # Update Y-coordinate
        elif self.position[0] == "2":  # ID "2" represents the right arm reference
            self.position_rx = float(self.position[1])  # Update X-coordinate
            self.position_ry = float(self.position[2])  # Update Y-coordinate
        elif self.position[0] == "5":  # ID "5" represents the left arm reference
            self.position_lx = float(self.position[1])  # Update X-coordinate
            self.position_ly = float(self.position[2])  # Update Y-coordinate
        elif self.position[0] == "6":  # ID "6" represents the brush
            self.position_bx = float(self.position[1])  # Update X-coordinate
            self.position_by = float(self.position[2])  # Update Y-coordinate


    
    def move(self, pose, reference_frame):
        """
        Executes specific movements for the right arm based on the pose parameter.
        Controls gripper states and uses MoveIt motion planning for smooth arm transitions.
        
        :param pose: Integer defining the type of movement to execute.
        :param reference_frame: The reference frame for motion planning.
        """
        # ==================== Return to Home Position ====================
        # Move the right arm to its home (default) position
        self.arm_R.set_named_target('Rhome')
        self.arm_R.go()

        # ==================== Perform Movements Based on Pose ====================

        # Pose 1: Perform a waving motion
        if pose == 1:
            for i in range(3):  # Repeat waving motion 3 times
                self.arm_R.set_named_target('R_wave_start')  # Move to wave start position
                self.arm_R.go()
                self.arm_R.set_named_target('R_wave_end')  # Move to wave end position
                self.arm_R.go()
            self.arm_R.set_named_target('Rhome')  # Return to home position
            self.arm_R.go()

        # Pose 2: Perform a punching motion
        elif pose == 2:
            self.rgripper_pub.publish(self.gripper_off)  # Open the gripper
            rospy.sleep(1)  # Wait for gripper to open
            for i in range(3):  # Repeat punching motion 3 times
                self.arm_R.set_named_target('R_punch')  # Move to punch position
                self.arm_R.go()
                self.arm_R.set_named_target('Rhome')  # Return to home position
                self.arm_R.go()
            self.rgripper_pub.publish(self.gripper_on)  # Close the gripper
            rospy.sleep(1)

        # Pose 3: Perform a raising motion
        elif pose == 3:
            for i in range(3):  # Repeat raising motion 3 times
                self.arm_R.set_named_target('R_raise')  # Move to raise position
                self.arm_R.go()
                self.arm_R.set_named_target('Rhome')  # Return to home position
                self.arm_R.go()

        # Pose 4: Perform a waving motion with a bell interaction
        elif pose == 4:
            for i in range(3):  # Repeat the motion 3 times
                self.arm_R.set_named_target('R_waveb')  # Move to wave with bell position
                self.arm_R.go()
                self.arm_R.set_named_target('R_d_bell')  # Interact with the bell
                self.arm_R.go()
            self.arm_R.set_named_target('Rhome')  # Return to home position
            self.arm_R.go()

        # Pose 6: Move towards a target position and interact with a bell
        elif pose == 6:
            # Increase speed for this movement
            self.arm_R.set_max_acceleration_scaling_factor(1)
            self.arm_R.set_max_velocity_scaling_factor(0.8)

            # Get the current position of the end-effector
            current_posea = self.arm_R.get_current_pose(self.end_effector_link_R).pose

            # Calculate the target position relative to the detected down bell
            x = current_posea.position.x + self.position_dbx - self.position_rx
            y = current_posea.position.y + (self.position_ry - self.position_dby) - 0.04

            # Adjust joint angles for the calculated target position
            joint_goal = self.arm_R.get_current_joint_values()
            joint_goal[2] += math.atan(
                (self.position_dbx - self.position_rx) /
                (self.position_ry - self.position_dby + 0.18 - 0.05)
            )
            self.arm_R.go(joint_goal, wait=True)

            # Define the target pose for motion planning
            current_pose = self.arm_R.get_current_pose(self.end_effector_link_R).pose
            target_pose = PoseStamped()
            target_pose.header.frame_id = reference_frame
            target_pose.header.stamp = rospy.Time.now()
            target_pose.pose.position.x = x
            target_pose.pose.position.y = y
            target_pose.pose.position.z = 1.04
            target_pose.pose.orientation = current_pose.orientation

            # Set the current state and target pose for planning
            self.arm_R.set_start_state_to_current_state()
            self.arm_R.set_joint_value_target(target_pose, self.end_effector_link_R, True)

            # Plan and execute the motion
            _, traj, _, _ = self.arm_R.plan()
            self.arm_R.execute(traj)

            # Interact with the bell
            self.rgripper_pub.publish(self.gripper_off)  # Open the gripper
            rospy.sleep(1)
            for i in range(3):  # Repeat bell interaction motion 3 times
                self.arm_R.set_named_target('R_wave_start')  # Start wave motion
                self.arm_R.go()
                self.arm_R.set_named_target('R_d_bell')  # Interact with the bell
                self.arm_R.go()

            # Return to the original position and complete interaction
            self.arm_R.set_start_state_to_current_state()
            self.arm_R.set_joint_value_target(target_pose, self.end_effector_link_R, True)
            _, traj, _, _ = self.arm_R.plan()
            self.arm_R.execute(traj)
            rospy.sleep(1)

            # Close the gripper and return to home position
            self.rgripper_pub.publish(self.gripper_on)
            rospy.sleep(1)
            self.arm_R.set_named_target('Rhome')
            self.arm_R.go()

            # Restore original speed settings
            self.arm_R.set_max_acceleration_scaling_factor(0.6)
        


        elif pose == 7:
            """
            Pose 7: Move the right arm towards the detected cup and perform a drinking motion.
            """
            # Get the current position of the right arm's end effector
            current_posea = self.arm_R.get_current_pose(self.end_effector_link_R).pose

            # Calculate the target position relative to the detected cup
            x = current_posea.position.x + self.position_cx - self.position_rx
            y = current_posea.position.y + (self.position_ry - self.position_cy) - 0.04

            # Adjust the joint angles based on the target position
            joint_goal = self.arm_R.get_current_joint_values()
            joint_goal[2] += math.atan((self.position_cx - self.position_rx) / (self.position_cy - self.position_cy + 0.18 - 0.05))
            joint_goal[3] += 0.042

            # Execute the adjusted joint angles
            self.arm_R.go(joint_goal, wait=True)

            # Define the target pose for motion planning
            current_pose = self.arm_R.get_current_pose(self.end_effector_link_R).pose
            target_pose = PoseStamped()
            target_pose.header.frame_id = reference_frame
            target_pose.header.stamp = rospy.Time.now()
            target_pose.pose.position.x = x
            target_pose.pose.position.y = y
            target_pose.pose.position.z = 1.03
            target_pose.pose.orientation = current_pose.orientation

            # Set and execute the motion plan
            self.arm_R.set_start_state_to_current_state()
            self.arm_R.set_joint_value_target(target_pose, self.end_effector_link_R, True)
            _, traj, _, _ = self.arm_R.plan()
            self.arm_R.execute(traj)
            rospy.sleep(1)

            # Simulate a drinking motion
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

            # Return to the original position and reset the gripper
            self.arm_R.set_start_state_to_current_state()
            self.arm_R.set_joint_value_target(target_pose, self.end_effector_link_R, True)
            _, traj, _, _ = self.arm_R.plan()
            self.arm_R.execute(traj)
            rospy.sleep(1)
            self.rgripper_pub.publish(self.gripper_on)
            rospy.sleep(1)
            self.arm_R.set_named_target('Rhome')
            self.arm_R.go()
            self.arm_R.set_max_acceleration_scaling_factor(0.6)


        elif pose == 8:
            """
            Pose 8: Move the right arm towards the detected brush and perform a brushing motion.
            """
            self.arm_R.set_max_acceleration_scaling_factor(0.6)

            # Get the current position of the right arm's end effector
            current_posea = self.arm_R.get_current_pose(self.end_effector_link_R).pose

            # Calculate the target position relative to the detected brush
            x = current_posea.position.x + self.position_bx - self.position_rx
            y = current_posea.position.y + (self.position_ry - self.position_by) - 0.04

            # Adjust the joint angles based on the target position
            joint_goal = self.arm_R.get_current_joint_values()
            joint_goal[2] += math.atan((self.position_bx - self.position_rx) / (self.position_ry - self.position_by + 0.18 - 0.05))
            self.arm_R.go(joint_goal, wait=True)

            # Define the target pose for motion planning
            current_pose = self.arm_R.get_current_pose(self.end_effector_link_R).pose
            target_pose = PoseStamped()
            target_pose.header.frame_id = reference_frame
            target_pose.header.stamp = rospy.Time.now()
            target_pose.pose.position.x = x
            target_pose.pose.position.y = y
            target_pose.pose.position.z = 1.03
            target_pose.pose.orientation = current_pose.orientation

            # Set and execute the motion plan
            self.arm_R.set_start_state_to_current_state()
            self.arm_R.set_joint_value_target(target_pose, self.end_effector_link_R, True)
            _, traj, _, _ = self.arm_R.plan()
            self.arm_R.execute(traj)
            rospy.sleep(1)

            # Simulate brushing motion
            self.rgripper_pub.publish(self.gripper_brush_r)
            rospy.sleep(1)
            for _ in range(3):
                self.arm_R.set_named_target('R_brush')
                self.arm_R.go()
                self.arm_R.set_named_target('R_brush2')
                self.arm_R.go()

            # Return to the original position and reset the gripper
            self.arm_R.set_start_state_to_current_state()
            self.arm_R.set_joint_value_target(target_pose, self.end_effector_link_R, True)
            _, traj, _, _ = self.arm_R.plan()
            self.arm_R.execute(traj)
            rospy.sleep(1)
            self.rgripper_pub.publish(self.gripper_on)
            rospy.sleep(1)
            self.arm_R.set_named_target('Rhome')
            self.arm_R.go()
            self.arm_R.set_max_acceleration_scaling_factor(0.6)


            self.arm_R.set_max_acceleration_scaling_factor(0.6)


            current_posea = self.arm_R.get_current_pose(self.end_effector_link_R).pose

            # # # 提取位姿中的位置部分
            # x = current_posea.position.x
            # y = current_posea.position.y
            # z = current_posea.position.z


            # rospy.loginfo(f"Current Position: x={x}, y={y}, z={z}  ")

            # # x = self.position_dbx
            # # y = -self.position_dby
            # # z = 1.03

            x = current_posea.position.x + self.position_bx - self.position_rx
            y = current_posea.position.y + (self.position_ry-self.position_by)-0.04

            #z = 1.03
            joint_goal = self.arm_R.get_current_joint_values()
            rospy.loginfo(f"{joint_goal[2]}")
            joint_goal[2] += math.atan( (self.position_bx - self.position_rx ) / (self.position_ry-self.position_by + 0.18-0.05))

            rospy.loginfo(f"{joint_goal[2]}  ")

            self.arm_R.go(joint_goal, wait=True) 

            current_pose = self.arm_R.get_current_pose(self.end_effector_link_R).pose
            target_pose = PoseStamped()
            target_pose.header.frame_id = reference_frame
            target_pose.header.stamp = rospy.Time.now()     
            target_pose.pose.position.x = x
            target_pose.pose.position.y = y
            target_pose.pose.position.z = 1.03
            target_pose.pose.orientation = current_pose.orientation

            # 设置机器臂当前的状态作为运动初始状态
            self.arm_R.set_start_state_to_current_state()
            
            # 设置机械臂终端运动的目标位姿
            self.arm_R.set_joint_value_target(target_pose, self.end_effector_link_R, True)
            
            # 规划运动路径
            _, traj, _, _ = self.arm_R.plan()

            # 按照规划的运动路径控制机械臂运动
            self.arm_R.execute(traj)
            rospy.sleep(1)

            

            self.rgripper_pub.publish(self.gripper_brush_r)

            rospy.sleep(1)

            self.arm_R.set_named_target('R_brush')
            self.arm_R.go()
            self.arm_R.set_named_target('R_brush2')
            self.arm_R.go()
            self.arm_R.set_named_target('R_brush')
            self.arm_R.go()
            self.arm_R.set_named_target('R_brush2')
            self.arm_R.go()
            self.arm_R.set_named_target('R_brush')
            self.arm_R.go()    

            # self.arm_L.set_named_target('R_drink')
            # self.arm_L.go()
            rospy.sleep(0.5)
            # 设置机器臂当前的状态作为运动初始状态
            self.arm_R.set_start_state_to_current_state()
            
            # 设置机械臂终端运动的目标位姿
            self.arm_R.set_joint_value_target(target_pose, self.end_effector_link_R, True)
            
            # 规划运动路径
            _, traj, _, _ = self.arm_R.plan()

            # 按照规划的运动路径控制机械臂运动
            self.arm_R.execute(traj)
            rospy.sleep(1)


            self.rgripper_pub.publish(self.gripper_on)
            rospy.sleep(1)
            self.arm_R.set_named_target('Rhome')
            self.arm_R.go()
            self.arm_R.set_max_acceleration_scaling_factor(0.6)

    
        elif pose == 11:
            for i in range(3):
                self.arm_L.set_named_target('L_wave_start')
                self.arm_L.go()

                self.arm_L.set_named_target('L_wave_end')
                self.arm_L.go()

            self.arm_L.set_named_target('Lhome')
            self.arm_L.go()

        elif pose == 12:
            self.lgripper_pub.publish(self.gripper_off_l)
            rospy.sleep(1)
            for i in range(3):
                self.arm_L.set_named_target('L_punch')
                self.arm_L.go()


                self.arm_L.set_named_target('Lhome')
                self.arm_L.go()        
            self.lgripper_pub.publish(self.gripper_on)
            rospy.sleep(1)
        elif pose == 13:
            for i in range(3):
                self.arm_L.set_named_target('L_raise')
                self.arm_L.go()

                self.arm_L.set_named_target('Lhome')
                self.arm_L.go()  

        elif pose == 14:
            for i in range(3):
                self.arm_L.set_named_target('L_waveb')
                self.arm_L.go()

                self.arm_L.set_named_target('L_d_bell')
                self.arm_L.go()
            self.arm_L.set_named_target('Lhome')
            self.arm_L.go() 

        # elif pose == 15:
      
        #     for i in range(3):
        #         self.arm_L.set_named_target('L_wave_f')
        #         self.arm_L.go()

        #         self.arm_L.set_named_target('L_wave_b')
        #         self.arm_L.go()
        #     self.arm_L.set_named_target('L_wave_f')
        #     self.arm_L.go()
        #     self.arm_L.set_named_target('Lhome')
        #     self.arm_L.go()  


        elif pose == 16:
            self.arm_L.set_max_acceleration_scaling_factor(1.0)
            z = 1.03


            current_posea = self.arm_L.get_current_pose(self.end_effector_link_L).pose

            # # # 提取位姿中的位置部分
            # x = current_posea.position.x
            # y = current_posea.position.y
            # z = current_posea.position.z


            # rospy.loginfo(f"Current Position: x={x}, y={y}, z={z}  ")

            # # x = self.position_dbx
            # # y = -self.position_dby
            # # z = 1.03

            x = current_posea.position.x + self.position_dbx - self.position_lx
            y = current_posea.position.y + (self.position_ly-self.position_dby)-0.03

            #z = 1.03
            joint_goal = self.arm_L.get_current_joint_values()
            rospy.loginfo(f"{joint_goal[2]}")
            joint_goal[2] += math.atan( (self.position_dbx - self.position_lx ) / (self.position_ly-self.position_dby + 0.18-0.055))

            rospy.loginfo(f"{joint_goal[2]}  ")

            self.arm_L.go(joint_goal, wait=True) 

            current_pose = self.arm_L.get_current_pose(self.end_effector_link_L).pose
            target_pose = PoseStamped()
            target_pose.header.frame_id = reference_frame
            target_pose.header.stamp = rospy.Time.now()     
            target_pose.pose.position.x = x
            target_pose.pose.position.y = y
            target_pose.pose.position.z = 1.04
            target_pose.pose.orientation = current_pose.orientation






            # 设置机器臂当前的状态作为运动初始状态
            self.arm_L.set_start_state_to_current_state()
            
            # 设置机械臂终端运动的目标位姿
            self.arm_L.set_joint_value_target(target_pose, self.end_effector_link_L, True)
            
            # 规划运动路径
            _, traj, _, _ = self.arm_L.plan()

            # 按照规划的运动路径控制机械臂运动
            self.arm_L.execute(traj)
            rospy.sleep(1)

            

            self.lgripper_pub.publish(self.gripper_off_l)

            rospy.sleep(1)

            self.arm_L.set_named_target('L_wave_start')
            self.arm_L.go()

            self.arm_L.set_named_target('L_d_bell')
            self.arm_L.go()

            self.arm_L.set_named_target('L_wave_start')
            self.arm_L.go()

            self.arm_L.set_named_target('L_d_bell')
            self.arm_L.go()

            self.arm_L.set_named_target('L_wave_start')
            self.arm_L.go()

            self.arm_L.set_named_target('Lhome')
            self.arm_L.go()

            # 设置机器臂当前的状态作为运动初始状态
            self.arm_L.set_start_state_to_current_state()
            
            # 设置机械臂终端运动的目标位姿
            self.arm_L.set_joint_value_target(target_pose, self.end_effector_link_L, True)
            
            # 规划运动路径
            _, traj, _, _ = self.arm_L.plan()

            # 按照规划的运动路径控制机械臂运动
            self.arm_L.execute(traj)
            rospy.sleep(1)


            self.lgripper_pub.publish(self.gripper_on)
            rospy.sleep(1)
            self.arm_L.set_named_target('Lhome')
            self.arm_L.go()
            self.arm_L.set_max_acceleration_scaling_factor(0.6)


        elif pose == 17:
            self.arm_L.set_max_acceleration_scaling_factor(0.8)

            z = 1.04


            current_posea = self.arm_L.get_current_pose(self.end_effector_link_L).pose


            x = current_posea.position.x + self.position_cx - self.position_lx
            y = current_posea.position.y + (self.position_ly-self.position_cy)-0.03

            #z = 1.03
            joint_goal = self.arm_L.get_current_joint_values()
            rospy.loginfo(f"{joint_goal[2]}")
            joint_goal[2] += math.atan( (self.position_cx - self.position_lx ) / (self.position_ly-self.position_cy + 0.18-0.055))



            
            rospy.loginfo(f"{joint_goal[3]}")
            joint_goal[3] += 0.08

            rospy.loginfo(f"{joint_goal[3]}  ")

            self.arm_L.go(joint_goal, wait=True) 


 
            current_pose = self.arm_L.get_current_pose(self.end_effector_link_L).pose
            target_pose = PoseStamped()
            target_pose.header.frame_id = reference_frame
            target_pose.header.stamp = rospy.Time.now()     
            target_pose.pose.position.x = x
            target_pose.pose.position.y = y
            target_pose.pose.position.z = z
            target_pose.pose.orientation = current_pose.orientation

            self.arm_L.set_start_state_to_current_state()
            

            self.arm_L.set_joint_value_target(target_pose, self.end_effector_link_L, True)
            

            _, traj, _, _ = self.arm_L.plan()


            self.arm_L.execute(traj)
            rospy.sleep(1)

            

            self.lgripper_pub.publish(self.gripper_cup_l)

            rospy.sleep(3)

            self.arm_L.set_named_target('L_cup_up')
            self.arm_L.go()
            rospy.sleep(1)
            # self.arm_L.set_named_target('L_cup_down')
            # self.arm_L.go()

            # self.arm_L.set_named_target('L_cup_up')
            # self.arm_L.go()

            # self.arm_L.set_named_target('L_cup_down')
            # self.arm_L.go()

            # self.arm_L.set_named_target('L_cup_up')
            # self.arm_L.go()

            # self.arm_L.set_named_target('L_cup_down')
            self.arm_L.go()

            self.arm_L.set_named_target('L_drink')
            self.arm_L.go()

            rospy.sleep(1)
            self.arm_L.set_named_target('L_cup_up')
            self.arm_L.go()
            rospy.sleep(1)

            self.arm_L.set_start_state_to_current_state()
            

            self.arm_L.set_joint_value_target(target_pose, self.end_effector_link_L, True)
            

            _, traj, _, _ = self.arm_L.plan()

            self.arm_L.execute(traj)
            rospy.sleep(1)


            self.lgripper_pub.publish(self.gripper_on)
            rospy.sleep(1)
            self.arm_L.set_named_target('Lhome')
            self.arm_L.go()
            self.arm_L.set_max_acceleration_scaling_factor(0.6)

        elif pose == 18:

            self.arm_L.set_max_acceleration_scaling_factor(0.8)
            z = 1.04


            current_posea = self.arm_L.get_current_pose(self.end_effector_link_L).pose



            x = current_posea.position.x + self.position_bx - self.position_lx
            y = current_posea.position.y + (self.position_ly-self.position_by)-0.025

            #z = 1.03
            joint_goal = self.arm_L.get_current_joint_values()
            rospy.loginfo(f"{joint_goal[2]}")
            joint_goal[2] += math.atan( (self.position_bx - self.position_lx ) / (self.position_ly-self.position_by + 0.18-0.055))

            rospy.loginfo(f"{joint_goal[2]}  ")
            joint_goal[3] += 0.04
            self.arm_L.go(joint_goal, wait=True) 


            current_pose = self.arm_L.get_current_pose(self.end_effector_link_L).pose
            target_pose = PoseStamped()
            target_pose.header.frame_id = reference_frame
            target_pose.header.stamp = rospy.Time.now()     
            target_pose.pose.position.x = x
            target_pose.pose.position.y = current_pose.position.y+0.01
            target_pose.pose.position.z = z
            target_pose.pose.orientation = current_pose.orientation


            self.arm_L.set_start_state_to_current_state()
            

            self.arm_L.set_joint_value_target(target_pose, self.end_effector_link_L, True)
            

            _, traj, _, _ = self.arm_L.plan()


            self.arm_L.execute(traj)
            rospy.sleep(1)

            

            self.lgripper_pub.publish(self.gripper_brush_l)

            rospy.sleep(1)

            self.arm_L.set_named_target('L_brush')
            self.arm_L.go()
            self.arm_L.set_named_target('L_brush2')
            self.arm_L.go()
            self.arm_L.set_named_target('L_brush')
            self.arm_L.go()
            self.arm_L.set_named_target('L_brush2')
            self.arm_L.go()
            self.arm_L.set_named_target('L_brush')
            self.arm_L.go()    

            # self.arm_L.set_named_target('R_drink')
            # self.arm_L.go()
            rospy.sleep(0.5)

            self.arm_L.set_start_state_to_current_state()
            

            self.arm_L.set_joint_value_target(target_pose, self.end_effector_link_L, True)
            

            _, traj, _, _ = self.arm_L.plan()


            self.arm_L.execute(traj)
            rospy.sleep(1)


            self.lgripper_pub.publish(self.gripper_on)
            rospy.sleep(1)
            self.arm_L.set_named_target('Lhome')
            self.arm_L.go()
            self.arm_L.set_max_acceleration_scaling_factor(0.6)


        elif pose == 21:
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

        elif pose == 22:
    
            for i in range(2):
                self.arm_D.set_named_target('D_up')
                self.arm_D.go()

                self.arm_D.set_named_target('D_down')
                self.arm_D.go()
            self.arm_D.set_named_target('D_up')
            self.arm_D.go()
            self.arm_D.set_named_target('D_home')
            self.arm_D.go()  

        elif pose == 23:

            for i in range(3):
                self.arm_D.set_named_target('L_down_R_up')
                self.arm_D.go()

                self.arm_D.set_named_target('R_down_L_up')
                self.arm_D.go()

            self.arm_D.set_named_target('D_home')
            self.arm_D.go()   
        elif pose == 24: # 
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



if __name__ == "__main__":
    MoveItIkDemo()
