#!/usr/bin/env python3

import argparse
import sys
import time

import paho.mqtt.client as mqtt

DEFAULT_TOPIC_MOVEMENT = "ros/mqtt/movement"
DEFAULT_TOPIC_FEEDBACK = "ros/mqtt/feedback"


def main():
    parser = argparse.ArgumentParser(description="Test MQTT action command flow.")
    parser.add_argument("pose", type=int, help="Pose/action number to send")
    parser.add_argument("--host", default="localhost", help="MQTT broker host")
    parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--topic-movement", default=DEFAULT_TOPIC_MOVEMENT, help="MQTT movement topic")
    parser.add_argument("--topic-feedback", default=DEFAULT_TOPIC_FEEDBACK, help="MQTT feedback topic")
    parser.add_argument("--timeout", type=float, default=5.0, help="Seconds to wait for feedback")
    args = parser.parse_args()

    feedback = {"received": False, "payload": None}

    def on_message(client, userdata, message):
        if message.topic != args.topic_feedback:
            return
        feedback["received"] = True
        feedback["payload"] = message.payload.decode(errors="replace").strip()

    client = mqtt.Client()
    client.on_message = on_message

    try:
        client.connect(args.host, args.port, 60)
    except Exception as exc:
        print(f"Failed to connect to MQTT broker: {exc}")
        return 1

    client.subscribe(args.topic_feedback)
    client.loop_start()

    client.publish(args.topic_movement, str(args.pose))
    print(f"Sent pose {args.pose} on {args.topic_movement}")

    start = time.time()
    while time.time() - start < args.timeout:
        if feedback["received"]:
            break
        time.sleep(0.1)

    client.loop_stop()
    client.disconnect()

    if feedback["received"]:
        print(f"Received feedback on {args.topic_feedback}: {feedback['payload']}")
        return 0

    print(f"Timed out waiting for feedback on {args.topic_feedback}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
