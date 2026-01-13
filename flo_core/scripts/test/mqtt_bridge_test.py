#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time

import paho.mqtt.client as mqtt


def main():
    print("Starting MQTT bridge test...", flush=True)
    broker_host = os.environ.get("MQTT_BROKER_HOST", "host.docker.internal")
    broker_port = int(os.environ.get("MQTT_BROKER_PORT", "1883"))
    action_done_delay = float(os.environ.get("MQTT_ACTION_DONE_DELAY", "0.5"))
    connect_retries = int(os.environ.get("MQTT_CONNECT_RETRIES", "5"))
    connect_retry_delay = float(os.environ.get("MQTT_CONNECT_RETRY_DELAY", "2.0"))
    test_topic = os.environ.get("MQTT_TEST_TOPIC", "ros/mqtt/test")

    topic_movement = "ros/mqtt/movement"
    topic_led = "ros/mqtt/led"
    topic_action_done = "ros/mqtt/action_done"
    topic_feedback = "ros/mqtt/feedback"

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print(f"Connected to MQTT broker at {broker_host}:{broker_port}")
            client.subscribe([(topic_movement, 0), (topic_led, 0)])
            client.publish(test_topic, "docker_connect_ok")
            print(f"Published test message to {test_topic}")
        else:
            print(f"Failed to connect to MQTT broker (rc={reason_code}) at {broker_host}:{broker_port}")

    def on_message(client, userdata, message):
        payload = message.payload.decode().strip()
        print(f"Received {message.topic}: {payload}")

        if message.topic == topic_movement:
            time.sleep(action_done_delay)
            client.publish(topic_feedback, "A")
            client.publish(topic_action_done, f"done:{payload}")
            print(f"Published action_done for {payload}")

    client.on_connect = on_connect
    client.on_message = on_message

    print(
        f"Attempting connect to {broker_host}:{broker_port} "
        f"(retries={connect_retries}, delay={connect_retry_delay}s)",
        flush=True,
    )
    connected = False
    for attempt in range(1, connect_retries + 1):
        try:
            client.connect(broker_host, broker_port, 60)
            connected = True
            break
        except Exception as exc:
            print(
                f"Connect attempt {attempt}/{connect_retries} failed to "
                f"{broker_host}:{broker_port}: {exc}"
            )
            sys.stdout.flush()
            time.sleep(connect_retry_delay)

    if not connected:
        print("Unable to connect to MQTT broker; exiting.")
        return

    client.loop_forever()


if __name__ == "__main__":
    main()
