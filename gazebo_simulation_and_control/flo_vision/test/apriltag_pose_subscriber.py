#!/usr/bin/env python3

import rospy
import math
import tf.transformations as tf
from geometry_msgs.msg import Pose
from std_msgs.msg import String

class AprilTagPoseSubscriber:
    def __init__(self):
        rospy.init_node('apriltag_pose_subscriber', anonymous=True)
        
        # subscribe to AprilTag pose and info topics
        self.pose_sub = rospy.Subscriber('/apriltag_poses', Pose, self.pose_callback)
        self.info_sub = rospy.Subscriber('/apriltag_info', String, self.info_callback)
        
        rospy.loginfo("AprilTag Pose Subscriber initialized")
        rospy.loginfo("Waiting for AprilTag pose messages...")

    def pose_callback(self, pose_msg):
        """handle received pose messages"""
        # extract position information
        x = pose_msg.position.x
        y = pose_msg.position.y
        z = pose_msg.position.z
        
        # calculate distance
        distance = math.sqrt(x**2 + y**2 + z**2)
        horizontal_distance = math.sqrt(x**2 + z**2)  # horizontal distance
        
        # extract quaternion
        qx = pose_msg.orientation.x
        qy = pose_msg.orientation.y
        qz = pose_msg.orientation.z
        qw = pose_msg.orientation.w
        
        # convert to euler angles (roll, pitch, yaw)
        euler = tf.euler_from_quaternion([qx, qy, qz, qw])
        roll = math.degrees(euler[0])   # rotate around X-axis
        pitch = math.degrees(euler[1])  # rotate around Y-axis
        yaw = math.degrees(euler[2])    # rotate around Z-axis
        
        # calculate relative angle to camera
        # horizontal angle (left/right direction)
        horizontal_angle = math.degrees(math.atan2(x, z))
        # vertical angle (up/down direction)
        vertical_angle = math.degrees(math.atan2(-y, z))  # note Y axis is downward
        
        # print detailed information
        print("=" * 60)
        print("AprilTag Detection Results:")
        print("-" * 30)
        print("Position (Camera Frame):")
        print(f"   X: {x:+7.3f}m  (Right/Left)")
        print(f"   Y: {y:+7.3f}m  (Down/Up)")
        print(f"   Z: {z:+7.3f}m  (Forward/Backward)")
        
        print("\n Distance Information:")
        print(f"   Total Distance:      {distance:.3f}m")
        print(f"   Horizontal Distance: {horizontal_distance:.3f}m")
        print(f"   Vertical Offset:     {abs(y):.3f}m")
        
        print("\n Angles from Camera:")
        print(f"   Horizontal Angle: {horizontal_angle:+7.1f}° (+ = Right, - = Left)")
        print(f"   Vertical Angle:   {vertical_angle:+7.1f}° (+ = Up, - = Down)")
        
        print("\n Tag Orientation (Euler Angles):")
        print(f"   Roll:  {roll:+7.1f}° (rotation around X-axis)")
        print(f"   Pitch: {pitch:+7.1f}° (rotation around Y-axis)")
        print(f"   Yaw:   {yaw:+7.1f}° (rotation around Z-axis)")
        
        # position description
        print("\n Position Description:")
        if z > 0:
            print(f"Tag is {z:.2f}m in FRONT of camera")
        else:
            print(f"Tag is {abs(z):.2f}m BEHIND camera")
            
        if x > 0:
            print(f" Tag is {x:.2f}m to the RIGHT")
        elif x < 0:
            print(f"Tag is {abs(x):.2f}m to the LEFT")
        else:
            print(f"Tag is CENTERED horizontally")
            
        if y > 0:
            print(f"Tag is {y:.2f}m BELOW camera center")
        elif y < 0:
            print(f"Tag is {abs(y):.2f}m ABOVE camera center")
        else:
            print(f"Tag is CENTERED vertically")
            
        # angle range hint
        print("\n Angular Information:")
        if abs(horizontal_angle) < 10:
            print("Tag is nearly straight ahead")
        elif abs(horizontal_angle) < 30:
            print("Tag is slightly to the side")
        else:
            print("Tag is significantly to the side")
            
        if abs(vertical_angle) < 5:
            print("Tag is at camera level")
        elif abs(vertical_angle) < 20:
            print("Tag is slightly above/below")
        else:
            print("Tag is significantly above/below")
        
        print("=" * 60)
        print()

    def info_callback(self, info_msg):
        """handle received info messages"""
        rospy.logdebug(f"Tag Info: {info_msg.data}")

def main():
    try:
        subscriber = AprilTagPoseSubscriber()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AprilTag Pose Subscriber shutting down")
    except KeyboardInterrupt:
        print("\n Shutting down AprilTag Pose Subscriber...")

if __name__ == '__main__':
    main()
