import os

MQTT_BROKER_HOST = os.environ.get("MQTT_BROKER_HOST", "host.docker.internal")
MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT", "1883"))
