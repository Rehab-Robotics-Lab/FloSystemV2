#!/usr/bin/env python
import paho.mqtt.client as mqtt
import time
import ntplib
import matplotlib.pyplot as plt
import csv
# 定义MQTT服务器地址
MQTT_BROKER = "0.0.0.0"  # 设置为本机地址，接收来自外部的连接
MQTT_PORT = 1883
TOPIC = "latency_test"
latencies = []
MAX_DATA_POINTS = 1000  # 收集 1000 个数据点
REMOVE_LAST_N = 5  # 去掉最后 5 个数据点
CSV_FILE = "latencies.csv"  # 用于保存延迟数据的CSV文件名
# 时间同步函数
def sync_time():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        print(f"Time synced: {time.ctime(response.tx_time)}")
        return True
    except Exception as e:
        print(f"Time synchronization failed: {e}")
        return False
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
# 尝试同步时间
if not sync_time():
    print("Unable to sync time. Proceeding with local time, but delays might be inaccurate.")
# 启动网络循环（非阻塞模式）
client.loop_start()
try:
    # 接收 1000 个数据点
    while len(latencies) < MAX_DATA_POINTS:
        time.sleep(0.1)  # 每 0.1 秒检查一次
    # 去掉最后 5 个数据
    if len(latencies) > REMOVE_LAST_N:
        latencies = latencies[:-REMOVE_LAST_N]
        print(f"Removed the last {REMOVE_LAST_N} data points.")
    # 保存延迟数据到 CSV 文件
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Latency (seconds)"])
        for latency in latencies:
            writer.writerow([latency])
    print(f"Latency data saved to {CSV_FILE}.")
finally:
    # 停止 MQTT 客户端
    client.loop_stop()
# 计算平均延迟并绘图
if latencies:
    avg_latency = sum(latencies) / len(latencies)
    print(f"Average latency: {avg_latency:.6f} seconds")
    # 绘制延迟图，并添加平均延迟线
    plt.figure(figsize=(10, 5))
    plt.plot(latencies, label="Latency (seconds)", color='b')
    plt.axhline(y=avg_latency, color='r', linestyle='--', label=f'Average Latency: {avg_latency:.6f} seconds')
    plt.xlabel("Message Number")
    plt.ylabel("Latency (seconds)")
    plt.title(f"MQTT Message Latency for {MAX_DATA_POINTS} Data Points (Last 5 Data Points Removed)")
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("No latencies recorded.")