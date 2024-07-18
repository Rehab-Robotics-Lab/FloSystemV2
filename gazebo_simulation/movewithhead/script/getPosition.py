#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from flo_humanoid.msg import SetJointPositions
from sensor_msgs.msg import JointState
import math

def convert_to_dynamixel_position(angle):
    return int((angle / 360.0) * 4096.0)





def joint_states_callback(msg,pub):
    
    joint_positions = dict(zip(msg.name, msg.position))

    
    r1_position = joint_positions.get('r1', None)
    r2_position = joint_positions.get('r2', None)
    r3_position = joint_positions.get('r3', None)
    r4_position = joint_positions.get('r4', None)

    
    if r1_position is not None:
        r1_position = math.degrees(r1_position)
    if r2_position is not None:
        r2_position = math.degrees(r2_position)
    if r3_position is not None:
        r3_position = math.degrees(r3_position)
    if r4_position is not None:
        r4_position = math.degrees(r4_position)

    r1_position += 90
    r2_position += 90
    r3_position += 180
    r4_position += 90


    pub.publish(SetJointPositions(
        211, 212, 221, 222,
        'position', 'position', 'position', 'position',
        convert_to_dynamixel_position(r1_position), convert_to_dynamixel_position(r2_position), convert_to_dynamixel_position(r3_position), convert_to_dynamixel_position(r4_position)
    ))

    rospy.loginfo(f"r1: {r1_position:.2f}°, r2: {r2_position:.2f}°, r3: {r3_position:.2f}°, r4: {r4_position:.2f}°")

def joint_state_listener():

    rospy.init_node('joint_state_listener', anonymous=True)
    pub = rospy.Publisher("/set_joint_positions", SetJointPositions, queue_size=10)
    rospy.Subscriber('/joint_states', JointState, joint_states_callback, callback_args=pub)
    rospy.spin()

if __name__ == '__main__':
    try:
        joint_state_listener()
    except rospy.ROSInterruptException:
        pass
