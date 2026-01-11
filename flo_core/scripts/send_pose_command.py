#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import sys
import time

def send_pose_command(pose_number):
    """
    Send a pose command to the robot via MQTT
    """
    client = mqtt.Client()
    
    try:
        # Connect to MQTT broker
        client.connect("localhost", 1883, 60)
        print(f"✅ Connected to MQTT broker")
        
        # Publish the pose command
        topic = "ros/mqtt/movement"
        message = str(pose_number)
        
        client.publish(topic, message)
        print(f"📤 Sent pose command: {message} to topic: {topic}")
        
        # Wait a moment for the message to be sent
        time.sleep(0.5)
        
        client.disconnect()
        print("🔌 Disconnected from MQTT broker")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    if len(sys.argv) != 2:
        print("🤖 FloRobot Motion Command Tool")
        print("=" * 40)
        print("Usage: python3 send_pose_command.py <pose_number>")
        print("\n📋 Available poses:")
        print("\n🦾 Right Arm Actions:")
        print("  1: Right arm wave")
        print("  2: Right arm punch") 
        print("  3: Right arm raise")
        print("  4: Right arm wave with bell")
        print("  6: Right arm smart bell interaction (requires AprilTag)")
        print("  7: Right arm smart drink (requires AprilTag)")
        print("  8: Right arm smart brush (requires AprilTag)")
        print("\n🦾 Left Arm Actions:")
        print("  11: Left arm wave")
        print("  12: Left arm punch")
        print("  13: Left arm raise") 
        print("  14: Left arm wave with bell")
        print("  16: Left arm smart bell interaction (requires AprilTag)")
        print("  17: Left arm smart drink (requires AprilTag)")
        print("  18: Left arm smart brush (requires AprilTag)")
        print("\n🤝 Dual Arm Actions:")
        print("  21: Dual arm clap")
        print("  22: Dual arm up-down")
        print("  23: Dual arm alternate")
        print("  24: Dual arm punch")
        print("\n💡 Note: Smart actions (6,7,8,16,17,18) require AprilTag detection to be running")
        return
    
    try:
        pose_number = int(sys.argv[1])
        
        # Validate pose number
        valid_poses = [1,2,3,4,6,7,8,11,12,13,14,16,17,18,21,22,23,24]
        if pose_number not in valid_poses:
            print(f"❌ Invalid pose number: {pose_number}")
            print(f"Valid poses: {valid_poses}")
            return
            
        print(f"🚀 Sending pose command: {pose_number}")
        send_pose_command(pose_number)
        print("✅ Command sent successfully!")
        
    except ValueError:
        print("❌ Error: Pose number must be an integer")

if __name__ == "__main__":
    main()
