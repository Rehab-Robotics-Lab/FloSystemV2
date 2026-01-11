#!/usr/bin/env python



import rospy

from std_msgs.msg import Int32,Float64
import paho.mqtt.client as mqtt
import threading



class Mqtt:
    def __init__(self):

                # 初始化ROS节点
        rospy.init_node('mqtt_demo')

        self.xy_pub = rospy.Publisher('/gripper', Float64, queue_size=10)
        self.move_pub = rospy.Publisher('/gripper', Int32, queue_size=10)

        # Define the callback function that will be called when a message is received
        def on_message(client, userdata, message):
            self.move_pub
            print(f"Received message: {message.payload.decode()} on topic {message.topic}")
        # Define the broker address and port
        broker_address = "172.20.10.6"  # Change to the IP of your MQTT broker if not running locally
        broker_port = 1883
        # Create a client instance
        client = mqtt.Client("Subscriber", protocol=mqtt.MQTTv311)
        # Attach the callback function to the client
        client.on_message = on_message
        # Connect to the broker
        client.connect(broker_address, broker_port)
        # Subscribe to the topic
        topic = "ros/mqtt/movement"
        client.subscribe(topic)
        # Start the loop to process received messages
        client.loop_forever()

if __name__ == "__main__":
    Mqtt()


