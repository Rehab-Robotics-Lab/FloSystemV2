import random
import time
import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import StringVar

# Function to send movement command via MQTT
def send_movement_via_mqtt(movement_number, topic):
    # 将 movement_number 转换为字符串
    message = str(movement_number)
    # 发布消息到指定主题
    client.publish(topic, message)
    print(f"Message sent to topic {topic}: {message}")

def main():
    # Define the MQTT topic
    movement_topic = "ros/mqtt/movement"

    # Define movements
    movements = ['Movement 1', 'Movement 2', 'Movement 3', 'Movement 4', 'Movement 5',
                 'Movement 6', 'Movement 7', 'Movement 16', 'Movement 17', 'Movement 21',
                 'Movement 11', 'Movement 12', 'Movement 13', 'Movement 14', 'Movement 15', 'Movement 22', 'Movement 23']

    # Randomize the movement sequence
    random.shuffle(movements)

    # Current step index
    current_step = 0

    # Create the main GUI application window
    root = tk.Tk()
    root.title("Movement Control")

    # Status variable to display current process
    status_var = StringVar()
    status_var.set("Click 'Next' to send movement command")

    # Function to proceed to the next step
    def next_step():
        nonlocal current_step
        if current_step < len(movements):
            # Extract the movement number
            movement_label = movements[current_step]
            movement_number = ''.join(filter(str.isdigit, movement_label))

            # Send the movement number via MQTT
            send_movement_via_mqtt(movement_number, movement_topic)

            # Update status
            status_var.set(f"Sent Movement: {movement_label}")

            # Move to the next movement
            current_step += 1
        else:
            status_var.set("All movements sent.")
            next_button.config(state=tk.DISABLED)  # Disable button after all movements are sent

    # Create GUI elements
    status_label = tk.Label(root, textvariable=status_var, font=("Arial", 16))
    status_label.pack(pady=10)

    next_button = tk.Button(root, text="Next", command=next_step, font=("Arial", 16))
    next_button.pack(pady=10)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == '__main__':
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

    main()

    # 在程序结束时断开MQTT连接
    client.disconnect()
