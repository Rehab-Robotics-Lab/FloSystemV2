import pygame
import tkinter as tk
from tkinter import StringVar
import time
import serial
import random
from cortex import Cortex
import threading
import datetime
import paho.mqtt.client as mqtt
from cortex_module.config.emotiv_creds import CLIENT_ID, CLIENT_SECRET  
import os

# global
marker_handler = None
this_file_path = os.path.dirname(os.path.abspath(__file__))


class MarkerHandler():
    def __init__(self, app_client_id, app_client_secret, **kwargs):
        self.c = Cortex(app_client_id, app_client_secret, debug_mode=True, **kwargs)
        self.c.bind(create_session_done=self.on_create_session_done)
        self.c.bind(create_record_done=self.on_create_record_done)
        self.c.bind(stop_record_done=self.on_stop_record_done)
        self.c.bind(warn_cortex_stop_all_sub=self.on_warn_cortex_stop_all_sub)
        self.c.bind(inject_marker_done=self.on_inject_marker_done)
        self.c.bind(export_record_done=self.on_export_record_done)
        self.c.bind(inform_error=self.on_inform_error)

    def start(self, record_title, record_description, folder, stream_types, export_format, version, headsetId=''):
        self.record_title = record_title
        self.record_description = record_description
        self.record_export_folder = folder
        self.record_export_data_types = stream_types
        self.record_export_format = export_format
        self.record_export_version = version

        if headsetId != '':
            self.c.set_wanted_headset(headsetId)

        # start Cortex连接和初始化
        self.c.open()

    def inject_marker(self, marker_value, marker_label):
        marker_time = time.time() * 1000
        self.c.inject_marker_request(marker_time, marker_value, marker_label, port='python_app')

    def stop_record(self):
        self.c.stop_record()

    # Callbacks
    def on_create_session_done(self, *args, **kwargs):
        print('on_create_session_done')
        self.c.create_record(self.record_title, description=self.record_description)

    def on_create_record_done(self, *args, **kwargs):
        data = kwargs.get('data')
        self.record_id = data['uuid']
        start_time = data['startDatetime']
        title = data['title']
        print(f'on_create_record_done: recordId: {self.record_id}, title: {title}, startTime: {start_time}')

    def on_stop_record_done(self, *args, **kwargs):
        data = kwargs.get('data')
        record_id = data['uuid']
        start_time = data['startDatetime']
        end_time = data['endDatetime']
        title = data['title']
        print(
            f'on_stop_record_done: recordId: {record_id}, title: {title}, startTime: {start_time}, EndTime: {end_time}')
        print('on_stop_record_done: Disconnect the headset to export record')
        self.c.disconnect_headset()

    def on_inject_marker_done(self, *args, **kwargs):
        data = kwargs.get('data')
        marker_id = data['uuid']
        start_time = data['startDatetime']
        marker_type = data['type']
        print(f'on_inject_marker_done: markerId: {marker_id}, type: {marker_type}, startTime: {start_time}')

    def on_warn_cortex_stop_all_sub(self, *args, **kwargs):
        print('on_warn_cortex_stop_all_sub')
        time.sleep(3)
        self.c.export_record(self.record_export_folder, self.record_export_data_types, self.record_export_format,
                             [self.record_id], self.record_export_version)

    def on_export_record_done(self, *args, **kwargs):
        print('on_export_record_done')
        data = kwargs.get('data')
        print(data)
        self.c.close()

    def on_inform_error(self, *args, **kwargs):
        error_data = kwargs.get('error_data')
        print(error_data)


def start_recording():
    global marker_handler

    # Initialize the Marker handler
    your_app_client_id = CLIENT_ID
    your_app_client_secret = CLIENT_SECRET
    current_time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    marker_handler = MarkerHandler(your_app_client_id, your_app_client_secret)
    marker_handler.start(
        record_title=f'AOE_{current_time_str}',
        record_description='',
        folder=os.path.join(this_file_path, 'record_data'),
        stream_types=['EEG', 'PM', 'BP'],
        export_format='CSV',
        version='V2'
    )


def send_movement_via_mqtt(movement_number, topic):
    # 将movement_number转换为字符串
    message = str(movement_number)
    # 发布消息到指定主题
    client.publish(topic, message)
    print(f"Message sent to topic {topic}: {message}")


def main():
    global marker_handler

    # Initialize pygame mixer for audio playback
    pygame.mixer.init()

    # Set up the serial connection (adjust the port to match your setup)
    serial_port = 'COM5'
    ser = serial.Serial(serial_port, 9600)  # Open the serial port
    time.sleep(2)  # Wait for the serial connection to initialize

    # Define the MQTT topic
    movement_topic = "ros/mqtt/movement"

    # Instruction sound files
    instruction_sounds = [
        'mp3_AOE/instruction1.mp3',  # Replace with actual file paths
        'mp3_AOE/instruction2.mp3'
    ]
    fixation_cross_sound = 'mp3_AOE/fixationcross.mp3'

    # Define movements
    movements = ['Movement 1', 'Movement 2', 'Movement 3', 'Movement 4', 'Movement 5','Movement 6','Movement 7','Movement 16', 'Movement 17','Movement 21',
                 'Movement 11', 'Movement 12', 'Movement 13', 'Movement 14', 'Movement 15']

    # movements = ['Movement 7','Movement 7','Movement 7']
    n_repeat = 1
    # Randomize the movement sequence for two full rounds
    randomized_movements = movements * n_repeat
    random.shuffle(randomized_movements)

    # Current step index
    current_step = 0
    after_print_step = False

    # Create the main GUI application window
    root = tk.Tk()
    root.title("Experiment Control")

    # Status variable to display current process
    status_var = StringVar()
    status_var.set("Initializing...")

    # Function to update the status label
    def update_status():
        nonlocal current_step, after_print_step
        if current_step == 0:
            status_var.set("Play Instruction 1 and Movement 1")
        elif current_step == 1:
            status_var.set("Play Fixation Cross Sound and LED 1")
        elif current_step == 2:
            status_var.set("Play Instruction 2 and LED 3")
        elif current_step >= 3 and current_step < 3 + len(randomized_movements):
            if not after_print_step:
                status_var.set(f"Publish Movement: {randomized_movements[current_step - 3]} via MQTT")
            else:
                status_var.set(f"Control LED and Marker for Movement: {randomized_movements[current_step - 3]}")
        elif current_step >= 3 + len(randomized_movements):
            status_var.set("End")

    # Function to play a sound
    def play_sound(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    # Function to send a command via serial
    def send_command(command):
        ser.write(command.encode())

    # Function to proceed to the next step
    def next_step():
        nonlocal current_step, after_print_step
        if current_step >= 3 and current_step < 3 + len(randomized_movements):
            if not after_print_step:
                # Extract the movement number
                movement_label = randomized_movements[current_step - 3]
                movement_number = ''.join(filter(str.isdigit, movement_label))

                # Send the movement number via MQTT
                send_movement_via_mqtt(movement_number, movement_topic)

                marker_handler.inject_marker(movement_number, movement_label)
                after_print_step = True
            else:
                # Handle the LED and marker after printing
                send_command('1')  # Turn on LED for fixation cross
                time.sleep(5.0)  # Keep LED on for 5 seconds
                send_command('0')  # Turn off LED
                marker_handler.inject_marker("1000", "fixationCross")
                send_command('3')  # Turn on LED for fixation cross
                marker_handler.inject_marker("5000", "fixationSquare")
                time.sleep(3.0)  # Keep LED on for 3 seconds
                send_command('0')  # Turn off LED
                time.sleep(5.0)
                marker_handler.inject_marker("3000", "intertrial_interval")
                after_print_step = False
                current_step += 1
        else:
            if current_step == 0:
                # Play instruction 1 and Movement 1
                play_sound(instruction_sounds[0])
                print("Movement 1")
                time.sleep(1.0)  # Simulate delay
            elif current_step == 1:
                # Play fixation cross sound and control LED 1
                play_sound(fixation_cross_sound)
                send_command('1')  # Turn on LED 1
                time.sleep(3.0)  # Keep LED on for 3 seconds
                send_command('0')  # Turn off LED
            elif current_step == 2:
                # Play instruction 2 and control LED 3
                play_sound(instruction_sounds[1])
                send_command('3')  # Turn on LED 3
                time.sleep(3.0)  # Keep LED on for 3 seconds
                send_command('0')  # Turn off LED
            else:
                # End the experiment
                status_var.set("End")
                marker_handler.stop_record()  # Stop the recording when the experiment ends
                pygame.quit()
                root.quit()
                return

            current_step += 1

        # Update the status after step
        update_status()

    # Create GUI elements
    status_label = tk.Label(root, textvariable=status_var, font=("Arial", 16))
    status_label.pack(pady=10)

    next_button = tk.Button(root, text="Next", command=next_step, font=("Arial", 16))
    next_button.pack(pady=10)

    # Initialize the status
    update_status()

    # Start the recording in a separate thread after the GUI is up
    threading.Thread(target=start_recording).start()

    # Start the Tkinter main loop
    root.mainloop()

    # 在程序结束时断开MQTT连接
    client.disconnect()


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
