#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32, Float64MultiArray
from flo_humanoid.msg import SetJointPositions
import math

def convert_to_dynamixel_position(angle):
    return int((angle / 360.0) * 4096.0)

gripper_position = 114  # open

def joint_angles_callback(msg, pub):
    global gripper_position
    
    joint_angle_sequences = msg.data
    num_joints = 4  # 每组4个关节
    num_sequences = len(joint_angle_sequences) // num_joints

    for i in range(num_sequences):
        r1_position = math.degrees(joint_angle_sequences[i * num_joints + 0]) + 110
        r2_position = math.degrees(joint_angle_sequences[i * num_joints + 1]) + 90
        r3_position = math.degrees(joint_angle_sequences[i * num_joints + 2]) + 180
        r4_position = math.degrees(joint_angle_sequences[i * num_joints + 3]) + 90

        pub.publish(SetJointPositions(
            211, 212, 221, 222, 13,
            'position', 'position', 'position', 'position', 'position',
            convert_to_dynamixel_position(r1_position), convert_to_dynamixel_position(r2_position),
            convert_to_dynamixel_position(r3_position), convert_to_dynamixel_position(r4_position),
            gripper_position
        ))

        rospy.loginfo(f"r1: {r1_position:.2f}°, r2: {r2_position:.2f}°, r3: {r3_position:.2f}°, r4: {r4_position:.2f}°, gripper: {gripper_position}")

def gripper_callback(msg):
    global gripper_position
    gripper_position = msg.data
    rospy.loginfo(f"Received gripper position: {gripper_position}")

def joint_angles_listener():
    rospy.init_node('joint_angles_listener', anonymous=True)
    pub = rospy.Publisher("/set_joint_positions", SetJointPositions, queue_size=10)
    rospy.Subscriber('/joint_angles', Float64MultiArray, joint_angles_callback, callback_args=pub)
    rospy.Subscriber('/gripper', Int32, gripper_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        joint_angles_listener()
    except rospy.ROSInterruptException:
        pass
