#!/usr/bin/env python
import rospy
from std_msgs.msg import  Int32
from flo_humanoid.msg import SetArmsJointPositions
from sensor_msgs.msg import JointState
import math

def convert_to_dynamixel_position(angle):
    return int((angle / 360.0) * 4096.0)


gripper_position = 114 # open

def joint_states_callback(msg, pub):
    global gripper_position
    
    joint_positions = dict(zip(msg.name, msg.position))

    r1_position = math.degrees(joint_positions.get('r1', None))
    r2_position = math.degrees(joint_positions.get('r2', None))
    r3_position = math.degrees(joint_positions.get('r3', None))
    r4_position = math.degrees(joint_positions.get('r4', None))
    l1_position = math.degrees(joint_positions.get('l1', None))
    l2_position = math.degrees(joint_positions.get('l2', None))
    l3_position = math.degrees(joint_positions.get('l3', None))
    l4_position = math.degrees(joint_positions.get('l4', None))

    
    r1_position += 110
    r2_position += 90
    r3_position += 180
    r4_position += 90

    l1_position += 300
    l2_position += 266 
    l3_position += 180
    l4_position = 180 - l4_position
    pub.publish(SetArmsJointPositions(
        111,112,121,122, 211, 212, 221, 222, 225,
        'position', 'position', 'position', 'position', 'position','position', 'position', 'position', 'position',
        convert_to_dynamixel_position(l1_position), convert_to_dynamixel_position(l2_position),
        convert_to_dynamixel_position(l3_position), convert_to_dynamixel_position(l4_position),
        convert_to_dynamixel_position(r1_position), convert_to_dynamixel_position(r2_position),
        convert_to_dynamixel_position(r3_position), convert_to_dynamixel_position(r4_position),
        gripper_position
    ))

    rospy.loginfo(f"r1: {r1_position:.2f}°, r2: {r2_position:.2f}°, r3: {r3_position:.2f}°, r4: {r4_position:.2f}°, gripper: {gripper_position}")

def gripper_callback(msg):
    global gripper_position
    gripper_position = msg.data
    rospy.loginfo(f"Received gripper position: {gripper_position}")

def joint_state_listener():
    rospy.init_node('joint_state_listener', anonymous=True)
    pub = rospy.Publisher("/set_arms_joint_positions", SetArmsJointPositions, queue_size=10)
    rospy.Subscriber('/joint_states', JointState, joint_states_callback, callback_args=pub)
    rospy.Subscriber('/gripper', Int32, gripper_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        joint_state_listener()
    except rospy.ROSInterruptException:
        pass
