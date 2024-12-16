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

        self.client = mqtt.Client()
        # 设置MQTT Broker的IP地址（通常为本机地址）
        self.broker_ip = "0.0.0.0"  # 使用 "0.0.0.0" 监听所有可用的网络接口，或使用 "127.0.0.1" 监听本地
        self.client.connect(self.broker_ip, 1883, 60)
        # 创建MQTT客户端

        self.gripper_cup_r = 3410
        self.gripper_cup_l = 3710
        self.gripper_off_l = 3700
        self.gripper_brush_l = 3710
        self.gripper_brush_r = 3410

        self.gripper_on = 1300
        self.gripper_off = 3410


        self.mode = "0"

        self.arm_len = 150 # mm
        self.arm_x = 0.09909856
        self.arm_y = -0.00930597

        self.position_dbx = 0  # down bell
        self.position_dby = 0



        self.position_cx = 0   # cup 
        self.position_cy = 0

        self.position_bx = 0   # brush 
        self.position_by = 0

        self.position_rx = 0
        self.position_ry = 0

        self.position_lx = 0
        self.position_ly = 0


        # 初始化move_group的API
        moveit_commander.roscpp_initialize(sys.argv)
        
        # 初始化ROS节点
        rospy.init_node('moveit_ik_demo')

        self.rgripper_pub = rospy.Publisher('/rgripper', Int32, queue_size=10)
        self.lgripper_pub = rospy.Publisher('/lgripper', Int32, queue_size=10)        

        # 初始化需要使用move group控制的机械臂中的arm group
        self.arm_R = moveit_commander.MoveGroupCommander('R')
        self.arm_L = moveit_commander.MoveGroupCommander('L')
        self.arm_D = moveit_commander.MoveGroupCommander('dual')  
                
        # 获取终端link的名称
        self.end_effector_link_R = self.arm_R.get_end_effector_link()
        self.end_effector_link_L = self.arm_L.get_end_effector_link()
        self.end_effector_link_D = self.arm_D.get_end_effector_link()                
        # 设置目标位置所使用的参考坐标系
        reference_frame = 'world'

        self.arm_R.set_pose_reference_frame(reference_frame)
        self.arm_L.set_pose_reference_frame(reference_frame)
        self.arm_D.set_pose_reference_frame(reference_frame)


        # 当运动规划失败后，允许重新规划
        self.arm_R.allow_replanning(True)
        self.arm_L.allow_replanning(True)
        self.arm_D.allow_replanning(True)


        # 设置位置(单位：米)和姿态（单位：弧度）的允许误差
        self.arm_R.set_goal_position_tolerance(0.001)
        self.arm_R.set_goal_orientation_tolerance(1)

        self.arm_L.set_goal_position_tolerance(0.001)
        self.arm_L.set_goal_orientation_tolerance(1)

        self.arm_D.set_goal_position_tolerance(0.001)
        self.arm_D.set_goal_orientation_tolerance(1)

        # 设置允许的最大速度和加速度
        self.arm_R.set_max_acceleration_scaling_factor(0.6)
        self.arm_R.set_max_velocity_scaling_factor(0.5)


        self.arm_L.set_max_acceleration_scaling_factor(0.6)
        self.arm_L.set_max_velocity_scaling_factor(0.5)

        self.arm_D.set_max_acceleration_scaling_factor(0.6)
        self.arm_D.set_max_velocity_scaling_factor(0.8)
        rospy.Subscriber("/apriltag_info", String, self.callback)

        #Start MQTT client in a separate thread
        mqtt_thread = threading.Thread(target=self.start_mqtt_client)
        mqtt_thread.start()

        # # # 获取末端执行器的当前位姿
        # current_pose = self.arm_R.get_current_pose(self.end_effector_link_R).pose

        # # # 提取位姿中的位置部分
        # x = current_pose.position.x
        # y = current_pose.position.y
        # z = current_pose.position.z

        # rospy.loginfo(f"Current Position: x={x}, y={y}, z={z}  ")
        # # rospy.loginfo(f"Current Position: x={self.position[0]}, y={self.position[1]}, z={self.position[2]}  ")

        #rospy.sleep(5)
        # self.move(17, reference_frame)

        while not rospy.is_shutdown():
            if self.mode != "0":
                self.move(int(self.mode), reference_frame)
                self.mode = "0"
                self.client.publish("ros/mqtt/feedback", "A")
            rospy.sleep(1)

        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

    

    def start_mqtt_client(self):


        

        # 定义当收到消息时的回调函数
        def on_message(client, userdata, message):
            print(f"Received message: {message.payload.decode()}")
            self.mode = str(message.payload.decode())
        # 设置回调函数
        self.client.on_message = on_message
        # 连接到Broker

        # 订阅主题
        self.client.subscribe("ros/mqtt/movement")
        # 开始循环，等待消息
        print("Waiting for messages...")
        self.client.loop_forever()

    def callback(self,data):
    # 打印接收到的位置信息
        #rospy.loginfo("Received AprilTag position: %s", data.data)
        cleaned_data = data.data.replace('[', '').replace(']', '').strip()
        # 将字符串拆分成浮点数列表
        # 解析数据为浮点数数组
        self.position = [x for x in cleaned_data.split()]
        
        if self.position[0] == "0":
            self.position_dbx = float(self.position[1])
            self.position_dby = float(self.position[2])
        elif self.position[0] == "3":
            self.position_cx = float(self.position[1])
            self.position_cy = float(self.position[2])   
        elif self.position[0] == "2":
            self.position_rx = float(self.position[1])
            self.position_ry = float(self.position[2]) 
        elif self.position[0] == "5":
            self.position_lx = float(self.position[1])
            self.position_ly = float(self.position[2]) 
        elif self.position[0] == "6":
            self.position_bx = float(self.position[1])
            self.position_by = float(self.position[2])   

    
    def move(self, pose, reference_frame):
        # 控制机械臂先回到初始化位置
        self.arm_R.set_named_target('Rhome')
        self.arm_R.go()

        if pose == 1:
            for i in range(3):
                self.arm_R.set_named_target('R_wave_start')
                self.arm_R.go()

                self.arm_R.set_named_target('R_wave_end')
                self.arm_R.go()

            self.arm_R.set_named_target('Rhome')
            self.arm_R.go()

        elif pose == 2:
            self.rgripper_pub.publish(self.gripper_off)
            rospy.sleep(1)
            for i in range(3):
                self.arm_R.set_named_target('R_punch')
                self.arm_R.go()

                self.arm_R.set_named_target('Rhome')
                self.arm_R.go() 
            self.rgripper_pub.publish(self.gripper_on)
            rospy.sleep(1)
             

        elif pose == 3:
            for i in range(3):
                self.arm_R.set_named_target('R_raise')
                self.arm_R.go()

                self.arm_R.set_named_target('Rhome')
                self.arm_R.go()

        elif pose == 4:
            for i in range(3):
                self.arm_R.set_named_target('R_waveb')
                self.arm_R.go()
                self.arm_R.set_named_target('R_d_bell')
                self.arm_R.go()          
            self.arm_R.set_named_target('Rhome')
            self.arm_R.go() 


        
        # elif pose == 5:
         
        #     for i in range(3):
        #         self.arm_R.set_named_target('R_wave_f')
        #         self.arm_R.go()

        #         self.arm_R.set_named_target('R_wave_b')
        #         self.arm_R.go()
        #     self.arm_R.set_named_target('R_wave_f')
        #     self.arm_R.go()
        #     self.arm_R.set_named_target('Rhome')
        #     self.arm_R.go()    






        elif pose == 6:
            self.arm_R.set_max_acceleration_scaling_factor(1)
            self.arm_R.set_max_velocity_scaling_factor(0.8)

            current_posea = self.arm_R.get_current_pose(self.end_effector_link_R).pose

            # # # 提取位姿中的位置部分
            # x = current_posea.position.x
            # y = current_posea.position.y
            # z = current_posea.position.z


            # rospy.loginfo(f"Current Position: x={x}, y={y}, z={z}  ")

            # # x = self.position_dbx
            # # y = -self.position_dby
            # # z = 1.03

            x = current_posea.position.x + self.position_dbx - self.position_rx
            y = current_posea.position.y + (self.position_ry-self.position_dby)-0.04

            #z = 1.03
            joint_goal = self.arm_R.get_current_joint_values()
            rospy.loginfo(f"{joint_goal[2]}")
            joint_goal[2] += math.atan( (self.position_dbx - self.position_rx ) / (self.position_ry-self.position_dby + 0.18-0.05))

            rospy.loginfo(f"{joint_goal[2]}  ")

            self.arm_R.go(joint_goal, wait=True) 

 
            current_pose = self.arm_R.get_current_pose(self.end_effector_link_R).pose
            target_pose = PoseStamped()
            target_pose.header.frame_id = reference_frame
            target_pose.header.stamp = rospy.Time.now()     
            target_pose.pose.position.x = x
            target_pose.pose.position.y = y
            target_pose.pose.position.z = 1.04
            target_pose.pose.orientation = current_pose.orientation

            # 设置机器臂当前的状态作为运动初始状态
            self.arm_R.set_start_state_to_current_state()
            
            # 设置机械臂终端运动的目标位姿
            self.arm_R.set_joint_value_target(target_pose, self.end_effector_link_R, True)
            
            # 规划运动路径
            _, traj, _, _ = self.arm_R.plan()

            # 按照规划的运动路径控制机械臂运动
            self.arm_R.execute(traj)

            

            self.rgripper_pub.publish(self.gripper_off)

            rospy.sleep(1)

            self.arm_R.set_named_target('R_wave_start')
            self.arm_R.go()

            self.arm_R.set_named_target('R_d_bell')
            self.arm_R.go()

            self.arm_R.set_named_target('R_wave_start')
            self.arm_R.go()

            self.arm_R.set_named_target('R_d_bell')
            self.arm_R.go()

            self.arm_R.set_named_target('R_wave_start')
            self.arm_R.go()

            # self.arm_R.set_named_target('Rhome')
            # self.arm_R.go()

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
        

        # elif pose == 7:
        #     self.arm_R.set_max_acceleration_scaling_factor(0.6)

        #     current_posea = self.arm_R.get_current_pose(self.end_effector_link_R).pose

        #     # # # 提取位姿中的位置部分
        #     # x = current_posea.position.x
        #     # y = current_posea.position.y
        #     # z = current_posea.position.z


        #     # rospy.loginfo(f"Current Position: x={x}, y={y}, z={z}  ")

        #     # # x = self.position_dbx
        #     # # y = -self.position_dby
        #     # # z = 1.03

        #     x = current_posea.position.x + self.position_cx - self.position_rx
        #     y = current_posea.position.y + (self.position_ry-self.position_cy)-0.05

        #     #z = 1.03
        #     joint_goal = self.arm_R.get_current_joint_values()
        #     rospy.loginfo(f"{joint_goal[2]}")
        #     joint_goal[2] += math.atan( (self.position_cx - self.position_rx ) / (self.position_ry-self.position_cy + 0.18-0.05))

        #     rospy.loginfo(f"{joint_goal[2]}  ")

        #     self.arm_R.go(joint_goal, wait=True) 

        #     # current_posea = self.arm_R.get_current_pose(self.end_effector_link_R).pose

        #     # # # # 提取位姿中的位置部分
        #     # x = current_posea.position.x
        #     # y = current_posea.position.y
        #     # z = 1.03

 
        #     current_pose = self.arm_R.get_current_pose(self.end_effector_link_R).pose
        #     target_pose = PoseStamped()
        #     target_pose.header.frame_id = reference_frame
        #     target_pose.header.stamp = rospy.Time.now()     
        #     target_pose.pose.position.x = x
        #     target_pose.pose.position.y = y
        #     target_pose.pose.position.z = 1.04
        #     target_pose.pose.orientation = current_pose.orientation

        #     # 设置机器臂当前的状态作为运动初始状态
        #     self.arm_R.set_start_state_to_current_state()
            
        #     # 设置机械臂终端运动的目标位姿
        #     self.arm_R.set_joint_value_target(target_pose, self.end_effector_link_R, True)
            
        #     # 规划运动路径
        #     _, traj, _, _ = self.arm_R.plan()

        #     # 按照规划的运动路径控制机械臂运动
        #     self.arm_R.execute(traj)
        #     rospy.sleep(1)

            

        #     self.rgripper_pub.publish(self.gripper_off)

        #     rospy.sleep(3)

        #     self.arm_R.set_named_target('R_cup_up')
        #     self.arm_R.go()

        #     self.arm_R.set_named_target('R_cup_down')
        #     self.arm_R.go()

        #     self.arm_R.set_named_target('R_cup_up')
        #     self.arm_R.go()

        #     self.arm_R.set_named_target('R_cup_down')
        #     self.arm_R.go()

        #     self.arm_R.set_named_target('R_cup_up')
        #     self.arm_R.go()

        #     self.arm_R.set_named_target('R_cup_down')
        #     self.arm_R.go()

        #     self.arm_R.set_named_target('R_drink')
        #     self.arm_R.go()

        #     # 设置机器臂当前的状态作为运动初始状态
        #     self.arm_R.set_start_state_to_current_state()
            
        #     # 设置机械臂终端运动的目标位姿
        #     self.arm_R.set_joint_value_target(target_pose, self.end_effector_link_R, True)
            
        #     # 规划运动路径
        #     _, traj, _, _ = self.arm_R.plan()

        #     # 按照规划的运动路径控制机械臂运动
        #     self.arm_R.execute(traj)
        #     rospy.sleep(1)


        #     self.rgripper_pub.publish(self.gripper_on)
        #     rospy.sleep(1)
        #     self.arm_R.set_named_target('Rhome')
        #     self.arm_R.go()
        #     self.arm_R.set_max_acceleration_scaling_factor(0.6)
        elif pose == 7:
            current_posea = self.arm_R.get_current_pose(self.end_effector_link_R).pose

            # # # 提取位姿中的位置部分
            # x = current_posea.position.x
            # y = current_posea.position.y
            # z = current_posea.position.z


            # rospy.loginfo(f"Current Position: x={x}, y={y}, z={z}  ")

            # # x = self.position_dbx
            # # y = -self.position_dby
            # # z = 1.03

            x = current_posea.position.x + self.position_cx - self.position_rx
            y = current_posea.position.y + (self.position_ry-self.position_cy)-0.04

            #z = 1.03
            joint_goal = self.arm_R.get_current_joint_values()
            rospy.loginfo(f"{joint_goal[2]}")
            joint_goal[2] += math.atan( (self.position_cx - self.position_rx ) / (self.position_cy-self.position_cy + 0.18-0.05))

            rospy.loginfo(f"{joint_goal[2]}  ")


            joint_goal[3] += 0.042

            rospy.loginfo(f"{joint_goal[3]}  ")

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

            

            self.rgripper_pub.publish(self.gripper_cup_r)

            rospy.sleep(1)

            self.arm_R.set_named_target('R_cup_up')
            self.arm_R.go()
            rospy.sleep(1)
            # self.arm_R.set_named_target('R_cup_down')
            # self.arm_R.go()

            # self.arm_R.set_named_target('R_cup_up')
            # self.arm_R.go()

            # self.arm_R.set_named_target('R_cup_down')
            # self.arm_R.go()

            # self.arm_R.set_named_target('R_cup_up')
            # self.arm_R.go()

            # self.arm_R.set_named_target('R_cup_down')
            # self.arm_R.go()

            self.arm_R.set_named_target('R_drink')
            self.arm_R.go()
            rospy.sleep(1)
            self.arm_R.set_named_target('R_cup_up')
            self.arm_R.go()
            rospy.sleep(1)
            
            self.arm_R.set_start_state_to_current_state()
            

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

        elif pose == 8:

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

        # elif pose == 17:
        #     self.arm_L.set_max_acceleration_scaling_factor(0.4)

        #     current_posea = self.arm_L.get_current_pose(self.end_effector_link_L).pose

        #     # # # 提取位姿中的位置部分
        #     # x = current_posea.position.x
        #     # y = current_posea.position.y
        #     # z = current_posea.position.z


        #     # rospy.loginfo(f"Current Position: x={x}, y={y}, z={z}  ")

        #     # # x = self.position_dbx
        #     # # y = -self.position_dby
        #     # # z = 1.03

        #     x = current_posea.position.x  + self.position_cx - self.position_lx
        #     y = current_posea.position.y  + (self.position_ly-self.position_cy)-0.03

        #     z = 1.03
        #     joint_goal = self.arm_L.get_current_joint_values()
        #     rospy.loginfo(f"{joint_goal[2]}")
        #     joint_goal[2] += math.atan( (self.position_cx - self.position_lx ) / (self.position_ly-self.position_cy + 0.125))

        #     rospy.loginfo(f"{joint_goal[2]}  ")

        #     self.arm_L.go(joint_goal, wait=True) 



 
        #     current_pose = self.arm_L.get_current_pose(self.end_effector_link_L).pose
        #     target_pose = PoseStamped()
        #     target_pose.header.frame_id = reference_frame
        #     target_pose.header.stamp = rospy.Time.now()     
        #     target_pose.pose.position.x = x
        #     target_pose.pose.position.y = y
        #     target_pose.pose.position.z = 1.04
        #     target_pose.pose.orientation = current_pose.orientation

        #     # 设置机器臂当前的状态作为运动初始状态
        #     self.arm_L.set_start_state_to_current_state()
            
        #     # 设置机械臂终端运动的目标位姿
        #     self.arm_L.set_joint_value_target(target_pose, self.end_effector_link_L, True)
            
        #     # 规划运动路径
        #     _, traj, _, _ = self.arm_L.plan()

        #     # 按照规划的运动路径控制机械臂运动
        #     self.arm_L.execute(traj)
        #     rospy.sleep(1)

            

        #     self.lgripper_pub.publish(self.gripper_off)

        #     rospy.sleep(3)

        #     self.arm_L.set_named_target('L_cup_up')
        #     self.arm_L.go()

        #     self.arm_L.set_named_target('L_cup_down')
        #     self.arm_L.go()

        #     self.arm_L.set_named_target('L_cup_up')
        #     self.arm_L.go()

        #     self.arm_L.set_named_target('L_cup_down')
        #     self.arm_L.go()

        #     self.arm_L.set_named_target('L_cup_up')
        #     self.arm_L.go()

        #     self.arm_L.set_named_target('L_cup_down')
        #     self.arm_L.go()

        #     self.arm_L.set_named_target('L_drink')
        #     self.arm_L.go()

        #     # 设置机器臂当前的状态作为运动初始状态
        #     self.arm_L.set_start_state_to_current_state()
            
        #     # 设置机械臂终端运动的目标位姿
        #     self.arm_L.set_joint_value_target(target_pose, self.end_effector_link_L, True)
            
        #     # 规划运动路径
        #     _, traj, _, _ = self.arm_L.plan()

        #     # 按照规划的运动路径控制机械臂运动
        #     self.arm_L.execute(traj)
        #     rospy.sleep(1)


        #     self.lgripper_pub.publish(self.gripper_on)
        #     rospy.sleep(1)
        #     self.arm_L.set_named_target('Lhome')
        #     self.arm_L.go()
        #     self.arm_L.set_max_acceleration_scaling_factor(0.6)
        elif pose == 17:
            self.arm_L.set_max_acceleration_scaling_factor(0.8)

            z = 1.04


            current_posea = self.arm_L.get_current_pose(self.end_effector_link_L).pose

            # # # 提取位姿中的位置部分
            # x = current_posea.position.x
            # y = current_posea.position.y
            # z = current_posea.position.z


            # rospy.loginfo(f"Current Position: x={x}, y={y}, z={z}  ")

            # # x = self.position_dbx
            # # y = -self.position_dby
            # # z = 1.03

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

            # 设置机器臂当前的状态作为运动初始状态
            self.arm_L.set_start_state_to_current_state()
            
            # 设置机械臂终端运动的目标位姿
            self.arm_L.set_joint_value_target(target_pose, self.end_effector_link_L, True)
            
            # 规划运动路径
            _, traj, _, _ = self.arm_L.plan()

            # 按照规划的运动路径控制机械臂运动
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

        elif pose == 18:

            self.arm_L.set_max_acceleration_scaling_factor(0.8)
            z = 1.04


            current_posea = self.arm_L.get_current_pose(self.end_effector_link_L).pose

            # # # 提取位姿中的位置部分
            # x = current_posea.position.x
            # y = current_posea.position.y
            # z = current_posea.position.z


            # rospy.loginfo(f"Current Position: x={x}, y={y}, z={z}  ")

            # # x = self.position_dbx
            # # y = -self.position_dby
            # # z = 1.03

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

            # 设置机器臂当前的状态作为运动初始状态
            self.arm_L.set_start_state_to_current_state()
            
            # 设置机械臂终端运动的目标位姿
            self.arm_L.set_joint_value_target(target_pose, self.end_effector_link_L, True)
            
            # 规划运动路径
            _, traj, _, _ = self.arm_L.plan()

            # 按照规划的运动路径控制机械臂运动
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
