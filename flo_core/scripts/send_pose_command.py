#!/usr/bin/env python3

import sys
import time

import paho.mqtt.client as mqtt

TOPIC_MOVEMENT = "ros/mqtt/movement"


def send_pose_command(pose_number):
    """
    Send a pose command to the robot via MQTT.
    """
    client = mqtt.Client()

    try:
        client.connect("localhost", 1883, 60)
        print("Connected to MQTT broker")

        message = str(pose_number)
        client.publish(TOPIC_MOVEMENT, message)
        print(f"Sent pose command: {message} to topic: {TOPIC_MOVEMENT}")

        time.sleep(0.5)
        client.disconnect()
        print("Disconnected from MQTT broker")

    except Exception as e:
        print(f"Error: {e}")


def main():
    if len(sys.argv) != 2:
        print("FloRobot Motion Command Tool")
        print("=" * 40)
        print("Usage: python3 send_pose_command.py <pose_number>")
        print("\nAvailable poses:")
        print("\nRight Arm Actions:")
        print("  1: Right arm wave")
        print("  2: Right arm punch")
        print("  3: Right arm raise")
        print("  4: Right arm wave with bell")
        print("\nLeft Arm Actions:")
        print("  11: Left arm wave")
        print("  12: Left arm punch")
        print("  13: Left arm raise")
        print("  14: Left arm wave with bell")
        print("\nDual Arm Actions:")
        print("  21: Dual arm clap")
        print("  22: Dual arm up-down")
        print("  23: Dual arm alternate")
        print("  24: Dual arm punch")
        print("  25: Dual arm go to home")
        return

    try:
        pose_number = int(sys.argv[1])

        valid_poses = [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 25]
        if pose_number not in valid_poses:
            print(f"Invalid pose number: {pose_number}")
            print(f"Valid poses: {valid_poses}")
            return

        print(f"Sending pose command: {pose_number}")
        send_pose_command(pose_number)
        print("Command sent successfully!")

    except ValueError:
        print("Error: Pose number must be an integer")


if __name__ == "__main__":
    main()
