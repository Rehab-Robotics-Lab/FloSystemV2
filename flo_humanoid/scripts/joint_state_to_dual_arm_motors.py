#!/usr/bin/env python3
import rospy
from flo_humanoid.msg import SetArmsJointPositions
from sensor_msgs.msg import JointState
import math

NODE_NAME = 'joint_state_to_dual_arm_motors'
TOPIC_JOINT_STATES = '/joint_states'
TOPIC_SET_POSITIONS = '/set_arms_joint_positions'

class JointStateToDxlBridge:
    def __init__(self):
        rospy.init_node(NODE_NAME)
        # Load joint ID map, mechanical offsets (degrees), and joint direction multipliers from ROS params.
        self.joint_id_map = rospy.get_param('joint_id_map')
        self.offsets = rospy.get_param('offsets')
        self.joint_signs = rospy.get_param('joint_signs')

        # Publisher
        self.set_arms_joint_positions_pub = rospy.Publisher(TOPIC_SET_POSITIONS, SetArmsJointPositions, queue_size=1)
        # Subscribers
        rospy.Subscriber(TOPIC_JOINT_STATES, JointState, self.joint_states_callback)

        # Log
        rospy.loginfo(f"[{NODE_NAME}] Bridging {TOPIC_JOINT_STATES} -> {TOPIC_SET_POSITIONS}")

    def convert_to_dynamixel_position(self, angle_deg):
        """
        Convert a joint angle in degrees (0-360) to a 12-bit Dynamixel position (0-4095).
        """
        return int((angle_deg / 360.0) * 4096.0)

    def joint_states_callback(self, msg):

        js = dict(zip(msg.name, msg.position))

        try:
            l1_position = self.joint_signs['l1'] * math.degrees(js['l1']) + self.offsets['l1']
            l2_position = self.joint_signs['l2'] * math.degrees(js['l2']) + self.offsets['l2']
            l3_position = self.joint_signs['l3'] * math.degrees(js['l3']) + self.offsets['l3']
            l4_position = self.joint_signs['l4'] * math.degrees(js['l4']) + self.offsets['l4']

            r1_position = self.joint_signs['r1'] * math.degrees(js['r1']) + self.offsets['r1']
            r2_position = self.joint_signs['r2'] * math.degrees(js['r2']) + self.offsets['r2']
            r3_position = self.joint_signs['r3'] * math.degrees(js['r3']) + self.offsets['r3']
            r4_position = self.joint_signs['r4'] * math.degrees(js['r4']) + self.offsets['r4']

        except KeyError as e:
            rospy.logwarn(f"Joint or config entry '{e.args[0]}' not found, skipping.")
            return

        self.set_arms_joint_positions_pub.publish(SetArmsJointPositions(
            self.joint_id_map['l1'], self.joint_id_map['l2'],
            self.joint_id_map['l3'], self.joint_id_map['l4'],
            self.joint_id_map['r1'], self.joint_id_map['r2'],
            self.joint_id_map['r3'], self.joint_id_map['r4'],
            # Command type for each: all 'position'
            'position', 'position', 'position', 'position',
            'position', 'position', 'position', 'position',
            # Values: convert angles to DXL ticks
            self.convert_to_dynamixel_position(l1_position),
            self.convert_to_dynamixel_position(l2_position),
            self.convert_to_dynamixel_position(l3_position),
            self.convert_to_dynamixel_position(l4_position),
            self.convert_to_dynamixel_position(r1_position),
            self.convert_to_dynamixel_position(r2_position),
            self.convert_to_dynamixel_position(r3_position),
            self.convert_to_dynamixel_position(r4_position),
        ))

        rospy.logdebug(
            f"Published DXL positions: L[{l1_position:.1f},{l2_position:.1f},{l3_position:.1f},{l4_position:.1f}]"
            f"R[{r1_position:.1f},{r2_position:.1f},{r3_position:.1f},{r4_position:.1f}]")


if __name__ == '__main__':
    try:
        bridge = JointStateToDxlBridge()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
