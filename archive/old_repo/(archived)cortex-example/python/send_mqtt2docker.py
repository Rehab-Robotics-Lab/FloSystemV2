#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt

def main():
    # IP of the broker inside Docker from host
    broker_ip = "localhost"  

    broker_port = 1883

    # Always prompt for pose
    pose = input("Enter a pose number to publish to ROS: ")

    client = mqtt.Client()
    client.connect(broker_ip, broker_port, 60)

    client.publish("ros/mqtt/movement", pose)

    client.disconnect()
    print(f"✅ Published pose '{pose}' to ros/mqtt/movement.")

if __name__ == "__main__":
    main()
