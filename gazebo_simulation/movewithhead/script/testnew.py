#!/usr/bin/env python
import paho.mqtt.client as mqtt
# Define the MQTT broker address and port
broker_address = "172.20.10.6"  # Change this to your broker address if different
broker_port = 1883
topic = "ros/mqtt/movement"  # Replace with your topic
# Define the callback function for when a message is received
def on_message(client, userdata, message):
    print(f"Received message: {str(message.payload.decode('utf-8'))} on topic {message.topic}")
# Create a new MQTT client instance
client = mqtt.Client()
# Attach the message callback function
client.on_message = on_message
# Connect to the broker
client.connect(broker_address, broker_port)
# Subscribe to the desired topic
client.subscribe(topic)
# Start the MQTT client loop to process network traffic and dispatch callbacks
client.loop_start()
# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()