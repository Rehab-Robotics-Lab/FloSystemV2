import pygame
import tkinter as tk
from tkinter import StringVar
import time
import serial
import random
import threading
import paho.mqtt.client as mqtt


# Placeholder for marker handler (Cortex related code commented out)
# marker_handler = None

def send_movement_via_mqtt(movement_number, topic):
    message = str(movement_number)
    client.publish(topic, message)
    print(f"Movement {movement_number} sent to topic {topic}")


def main():
    # Initialize Pygame
    pygame.mixer.init()

    # Set up Serial connection (adjust the port to match your setup)
    serial_port = 'COM5'
    ser = serial.Serial(serial_port, 9600)
    time.sleep(2)

    # Define MQTT topics
    movement_topic = "ros/mqtt/movement"
    feedback_topic = "ros/mqtt/feedback"

    # List of movements to randomize
    movements = ['Movement 6', 'Movement 7', 'Movement 16', 'Movement 17']
    # random.shuffle(movements)

    current_step = 0
    awaiting_feedback = False

    # Set up the main GUI window
    root = tk.Tk()
    root.title("Experiment Control")

    # Status display
    status_var = StringVar()
    status_var.set("Initializing...")

    def update_status():
        if current_step < len(movements):
            status_var.set(
                f"Running: {movements[current_step]} | Next: {movements[(current_step + 1) % len(movements)]}")
        else:
            status_var.set("End of experiment")

    def send_command(command):
        ser.write(command.encode())

    # Handle feedback message from MQTT
    def on_feedback_message(client, userdata, message):
        nonlocal awaiting_feedback
        payload = message.payload.decode()
        if payload == 'A':
            awaiting_feedback = True

    # Subscribe to feedback topic
    client.message_callback_add(feedback_topic, on_feedback_message)

    # Main experimental step control
    def next_step():
        nonlocal current_step, awaiting_feedback

        if current_step < len(movements):
            # Display Fixation Cross (1s)
            status_var.set("Fixation Cross")
            send_command('1')
            time.sleep(1)
            send_command('0')
            status_var.set("Square")
            send_command('2')
            time.sleep(1)
            # Send current movement MQTT message
            movement_number = ''.join(filter(str.isdigit, movements[current_step]))
            send_movement_via_mqtt(movement_number, movement_topic)
            # marker_handler.inject_marker(movement_number, movements[current_step]) # Cortex related code commented out

            # Wait for feedback signal to continue
            awaiting_feedback = False
            status_var.set("Waiting for feedback 'A'")
            while not awaiting_feedback:
                client.loop()

            time.sleep(1)

            # Display Fixation Cross (1s) and Triangle (5s)
            status_var.set("Fixation Cross")
            send_command('1')
            # marker_handler.inject_marker("1000", "fixationCross")  # Cortex related code commented out
            time.sleep(1)
            send_command('0')

            status_var.set("Triangle")
            send_command('3')
            # marker_handler.inject_marker("5000", "Triangle")  # Cortex related code commented out
            time.sleep(5)
            send_command('0')

            current_step += 1
            update_status()
        else:
            status_var.set("End of experiment")
            # marker_handler.stop_record()  # Cortex related code commented out
            pygame.quit()
            root.quit()

    # GUI setup
    status_label = tk.Label(root, textvariable=status_var, font=("Arial", 16))
    status_label.pack(pady=10)

    next_button = tk.Button(root, text="Next", command=next_step, font=("Arial", 16))
    next_button.pack(pady=10)

    update_status()
    root.mainloop()
    client.disconnect()


if __name__ == '__main__':
    broker_ip = "169.254.131.1"
    client = mqtt.Client()

    try:
        client.connect(broker_ip, 1883, 60)
        print(f"Connected to MQTT Broker at {broker_ip}")
        client.subscribe("ros/mqtt/feedback")
    except Exception as e:
        print(f"Failed to connect to MQTT Broker: {e}")
        exit(1)

    main()
