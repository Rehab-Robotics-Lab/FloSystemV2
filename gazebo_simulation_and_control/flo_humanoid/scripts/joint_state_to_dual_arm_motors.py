#!/usr/bin/env python3
import rospy
from std_msgs.msg import  Int32
from flo_humanoid.msg import SetArmsJointPositions
from sensor_msgs.msg import JointState
import math

NODE_NAME = 'joint_state_to_dual_arm_motors'
TOPIC_JOINT_STATES = '/joint_states'
TOPIC_SET_POSITIONS = '/set_arms_joint_positions'
class JointStateToDxlBridge:
    def __init__(self):
        rospy.init_node(NODE_NAME)
        self.rgripper_position = 1300 # open
        self.lgripper_position = 1300 # open
        # Load joint ID map and mechanical offsets (in degrees) from ROS params
        self.joint_id_map = rospy.get_param('joint_id_map')
        self.offsets = rospy.get_param('offsets')
        # Publisher
        self.pub = rospy.Publisher(TOPIC_SET_POSITIONS, SetArmsJointPositions, queue_size=1)
        # Subscribers
        rospy.Subscriber(TOPIC_JOINT_STATES, JointState, self.joint_states_callback)
        rospy.Subscriber('/rgripper', Int32, self.rgripper_callback)
        rospy.Subscriber('/lgripper', Int32, self.lgripper_callback)
        # Log
        rospy.loginfo(f"[{NODE_NAME}] Bridging {TOPIC_JOINT_STATES} → {TOPIC_SET_POSITIONS}")
        
    def convert_to_dynamixel_position(self, angle_deg):
        """
        Convert a joint angle in degrees (0-360) to a 12-bit Dynamixel position (0-4095).
        """
        angle = angle_deg % 360.0
        return int((angle / 360.0) * 4096.0)

    def joint_states_callback(self, msg):
        # global self.rgripper_position
        # global self.lgripper_position
        
        js = dict(zip(msg.name, msg.position))

        try:
            r1_position = math.degrees(js['r1']) + self.offsets['r1']
            r2_position = math.degrees(js['r2']) + self.offsets['r2']
            r3_position = math.degrees(js['r3']) + self.offsets['r3']
            r4_position = math.degrees(js['r4']) + self.offsets['r4']

            l1_position = math.degrees(js['l1']) + self.offsets['l1']
            l2_position = math.degrees(js['l2']) + self.offsets['l2']
            l3_position = math.degrees(js['l3']) + self.offsets['l3']
            l4_position = math.degrees(js['l4']) + self.offsets['l4'] # 180 - l4_position ?
        
        except KeyError as e:
            rospy.logwarn(f"Joint '{e.args[0]}' not found in /joint_states, skipping.")
            return


        self.pub.publish(SetArmsJointPositions(
            self.joint_id_map['l1'], self.joint_id_map['l2'], 
            self.joint_id_map['l3'], self.joint_id_map['l4'], 
            self.joint_id_map['lgripper'],
            self.joint_id_map['r1'], self.joint_id_map['r2'], 
            self.joint_id_map['r3'], self.joint_id_map['r4'], 
            self.joint_id_map['rgripper'],

            'position', 'position', 'position', 'position', 'position',
            'position', 'position', 'position', 'position', 'position',
            self.convert_to_dynamixel_position(l1_position), 
            self.convert_to_dynamixel_position(l2_position),
            self.convert_to_dynamixel_position(l3_position), 
            self.convert_to_dynamixel_position(l4_position),
            self.lgripper_position,
            self.convert_to_dynamixel_position(r1_position), 
            self.convert_to_dynamixel_position(r2_position),
            self.convert_to_dynamixel_position(r3_position), 
            self.convert_to_dynamixel_position(r4_position),
            self.rgripper_position

        ))

        rospy.loginfo(f"r1: {r1_position:.2f}°, r2: {r2_position:.2f}°, r3: {r3_position:.2f}°, r4: {r4_position:.2f}°, gripper: {self.rgripper_position}, gripper: {self.lgripper_position}")

    def rgripper_callback(self, msg):
        self.rgripper_position
        rgripper_position = msg.data
        rospy.loginfo(f"Received gripper position: {rgripper_position}")

    def lgripper_callback(self, msg):
        self.lgripper_position
        lgripper_position = msg.data
        rospy.loginfo(f"Received gripper position: {lgripper_position}")


if __name__ == '__main__':
    try:
        bridge = JointStateToDxlBridge()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
