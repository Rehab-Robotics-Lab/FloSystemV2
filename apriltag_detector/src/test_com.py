#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
# service mosquitto start
# Define the broker address and port
broker_address = "172.20.10.6"  # Change to localhost since broker runs inside the container
broker_port = 1883

# Create a client instance
client = mqtt.Client("Publisher")

# Connect to the broker
client.connect(broker_address, broker_port)

# Publish messages to a topic
topic = "ros/mqtt/topic"
message = "Hello from Docker"
while True:
    client.publish(topic, message)
    print("Published: {}".format(message))
    time.sleep(5)  # Publish a message every 5 seconds

