import os
import paho.mqtt.client as mqtt


try:
    MQTT_BROKER_CLIENT = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
except AttributeError:
    MQTT_BROKER_CLIENT = mqtt.Client()

MQTT_BROKER_HOST = os.environ.get("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT", "1883"))
