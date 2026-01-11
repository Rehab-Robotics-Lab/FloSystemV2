#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import paho.mqtt.client as mqtt

def main():
    # The broker IP and port should match what MoveItIkDemo or your MQTT setup uses
    broker_ip = "localhost"    # or "localhost"
    broker_port = 1883       # default Mosquitto port

    # Retrieve the pose number from the command line (passed in by start_ros_tmux.sh)
    if len(sys.argv) < 2:
        pose = input("No pose argument provided. Enter a pose number: ")
    else:
        pose = sys.argv[1]

    # Initialize MQTT client and connect
    client = mqtt.Client()
    client.connect(broker_ip, broker_port, 60)

    # Publish your pose command
    client.publish("ros/mqtt/movement", pose)

    # Close the connection
    client.disconnect()
    print(f"Published pose '{pose}' to ros/mqtt/movement.")

if __name__ == "__main__":
    main()
