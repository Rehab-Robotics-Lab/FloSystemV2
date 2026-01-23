import os
import paho.mqtt.client as mqtt

MQTT_BROKER_CLIENT = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
MQTT_BROKER_HOST = os.environ.get("MQTT_BROKER_HOST", "host.docker.internal") # Set to "localhost" if running MQTT broker locally
MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT", "1883"))
