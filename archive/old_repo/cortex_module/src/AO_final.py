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
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.emotiv_creds import CLIENT_ID, CLIENT_SECRET  

# Global
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

        # Start Cortex connection and initialization
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
        record_title=f'AO_{current_time_str}',
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
    # ser = serial.Serial(serial_port, 9600)  # Open the serial port
    time.sleep(2)  # Wait for the serial connection to initialize

    # Define the MQTT topic
    movement_topic = "ros/mqtt/movement"

    # Instruction sound files
    instruction_sounds = [
        'mp3_AO/instruction1.mp3',  # Replace with actual file paths
        'mp3_AO/instruction2.mp3',
        'mp3_AO/instruction3.mp3',
        'mp3_AO/instruction4.mp3'
    ]

    # Define movements
    movements = ['Movement 1', 'Movement 2', 'Movement 3', 'Movement 4', 'Movement 5', 'Movement 6', 'Movement 7' ,'Movement 21',
                 'Movement 11', 'Movement 12', 'Movement 13', 'Movement 14', 'Movement 15']
    n_repeat = 1
    # Randomize the movement sequence
    randomized_movements = movements * n_repeat
    random.shuffle(randomized_movements)

    # Current step index
    current_step = 0

    # Create the main GUI application window
    root = tk.Tk()
    root.title("Experiment Control")

    # Status variable to display current process
    status_var = StringVar()
    status_var.set("Initializing...")

    # Function to update the status label
    def update_status():
        nonlocal current_step
        if current_step == 0:
            status_var.set("Play Instruction 1-2")
        elif current_step == 1:
            status_var.set("Cross Sound and Display")
        elif current_step == 2:
            status_var.set("Play Instruction 3-4")
        elif current_step >= 3 and current_step < 3 + len(randomized_movements):
            status_var.set(f"{randomized_movements[current_step - 3]}")
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
        nonlocal current_step
        if current_step == 0:
            # Initially close the cross
            # send_command('0')
            # Play instruction 1-2
            play_sound(os.path.join(this_file_path, instruction_sounds[0]))
            play_sound(os.path.join(this_file_path, instruction_sounds[1]))
        elif current_step == 1:
            # Play cross sound and simulate displaying cross for 5 seconds
            play_sound(os.path.join(this_file_path, 'mp3_AO/cross_sound.mp3'))  # Replace with the cross sound file
            # send_command('1')  # Turn on cross on the LED matrix
            time.sleep(5.0)  # Simulate displaying cross for 5 seconds
            # send_command('0')  # Turn off cross on the LED matrix
        elif current_step == 2:
            # Play instruction 3-4
            play_sound(os.path.join(this_file_path, instruction_sounds[2]))
            play_sound(os.path.join(this_file_path, instruction_sounds[3]))
        elif current_step >= 3 and current_step < 3 + len(randomized_movements):
            # Simulate displaying cross for 3 seconds, then indicate movement
            # send_command('1')  # Turn on cross on the LED matrix
            time.sleep(3.0)  # Simulate displaying cross for 3 seconds
            # send_command('0')  # Turn off cross on the LED matrix

            # Get the actual movement number from the randomized movement list
            movement_label = randomized_movements[current_step - 3]
            movement_number = ''.join(filter(str.isdigit, movement_label))

            marker_handler.inject_marker("1000", "fixationCross")
            time.sleep(1.0)
            marker_handler.inject_marker("3000", "intertrial_interval")

            # 通过MQTT发送movement_number
            # send_movement_via_mqtt(movement_number, movement_topic)
            marker_handler.inject_marker(movement_number, movement_label)

        else:
            # End the experiment
            status_var.set("End")
            marker_handler.stop_record()  # Stop the recording when the experiment ends
            pygame.quit()
            root.quit()
            return

        # Update current step
        current_step += 1
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
    # client.disconnect()


if __name__ == '__main__':
    # 设置MQTT Broker的IP地址
    broker_ip = "169.254.131.1"  # 替换为Ubuntu机器的IP地址

    # # 创建MQTT客户端
    # client = mqtt.Client()

    # # 尝试连接到Broker
    # try:
    #     client.connect(broker_ip, 1883, 60)
    #     print(f"Connected to MQTT Broker at {broker_ip}")
    # except Exception as e:
    #     print(f"Failed to connect to MQTT Broker: {e}")
    #     exit(1)

    main()
