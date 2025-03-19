#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt

def main():
    # The broker IP and port should match what MoveItIkDemo is using.
    broker_ip = "0.0.0.0"   # or "localhost" if broker is on the same machine
    broker_port = 1883      # default Mosquitto port

    # Initialize MQTT client and connect
    client = mqtt.Client()
    client.connect(broker_ip, broker_port, 60)

    # Publish your pose command, e.g. "1" for the waving motion
    client.publish("ros/mqtt/movement", "1")

    # Close the connection
    client.disconnect()

if __name__ == "__main__":
    main()