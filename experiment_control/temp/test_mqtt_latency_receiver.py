import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt

# 定义MQTT服务器地址
MQTT_BROKER = "0.0.0.0"  # 设置为本机地址，接收来自外部的连接
MQTT_PORT = 1883
TOPIC = "latency_test"

latencies = []

# 当连接时调用该回调函数
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 连接后订阅测试主题
    client.subscribe(TOPIC)

# 当接收到消息时调用该回调函数
def on_message(client, userdata, msg):
    global latencies
    # 从消息中获取发送的时间戳
    start_time = float(msg.payload.decode())
    # 接收到消息的当前时间
    end_time = time.time()
    latency = end_time - start_time
    latencies.append(latency)
    print(f"Message received at {end_time:.6f}, latency: {latency:.6f} seconds")

# 初始化MQTT客户端
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 连接到MQTT服务器
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# 启动网络循环（非阻塞模式）
client.loop_start()

try:
    # 等待接收消息并记录一段时间
    print("Receiving messages... Press Ctrl+C to stop and plot results.")
    while True:
        time.sleep(1)  # 每秒检查一次
except KeyboardInterrupt:
    print("Stopped receiving messages. Now plotting results...")

    # 计算平均延迟
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        print(f"Average latency: {avg_latency:.6f} seconds")

        # 绘制延迟图
        plt.figure(figsize=(10, 5))
        plt.plot(latencies, label="Latency (seconds)", color='b')
        plt.xlabel("Message Number")
        plt.ylabel("Latency (seconds)")
        plt.title("MQTT Message Latency Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print("No latencies recorded.")
finally:
    client.loop_stop()
