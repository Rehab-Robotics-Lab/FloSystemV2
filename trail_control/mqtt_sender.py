import paho.mqtt.client as mqtt

# 设置MQTT Broker的IP地址
broker_ip = "169.254.131.1"  # 替换为Ubuntu机器的IP地址

# 创建MQTT客户端
client = mqtt.Client()

# 尝试连接到Broker
try:
    client.connect(broker_ip, 1883, 60)
    print(f"Connected to MQTT Broker at {broker_ip}")
except Exception as e:
    print(f"Failed to connect to MQTT Broker: {e}")
    exit(1)

# 发布消息到指定主题
topic = "test/topic"
message = "Hello from Windows!"
client.publish(topic, message)
print(f"Message sent to topic {topic}: {message}")

# 断开连接
client.disconnect()
