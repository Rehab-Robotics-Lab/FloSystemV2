import paho.mqtt.client as mqtt
import time
import ntplib

# 定义MQTT服务器地址
MQTT_BROKER = "169.254.131.1"  # 请填写接收端电脑的IP地址
MQTT_PORT = 1883
TOPIC = "latency_test"
INTERVAL = 0.5  # 每0.5秒发送一条消息，降低频率

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

# 初始化MQTT客户端
client = mqtt.Client()

# 连接到MQTT服务器
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# 启动网络循环（非阻塞模式）
client.loop_start()

# 尝试同步时间
if not sync_time():
    print("Unable to sync time. Proceeding with local time, but delays might be inaccurate.")

# 发送多条测试消息
try:
    while True:
        start_time = time.time()
        client.publish(TOPIC, str(start_time), qos=0)  # 使用QoS 0，简化消息内容
        print(f"Message sent at {start_time:.6f}")
        time.sleep(INTERVAL)  # 每 0.5 秒发送一条消息
except KeyboardInterrupt:
    print("Stopping message sending...")
finally:
    client.loop_stop()
