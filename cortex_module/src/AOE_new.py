import pygame
import tkinter as tk
from tkinter import StringVar
import time
import serial
import random
import threading
import paho.mqtt.client as mqtt
from cortex import Cortex
import datetime

# Global marker handler
marker_handler = None

class MarkerHandler():
    def __init__(self, app_client_id, app_client_secret, **kwargs):
        # Initialize Cortex connection
        self.c = Cortex(app_client_id, app_client_secret, debug_mode=True, **kwargs)
        self.c.bind(create_session_done=self.on_create_session_done)
        self.c.bind(create_record_done=self.on_create_record_done)
        self.c.bind(stop_record_done=self.on_stop_record_done)
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

        self.c.open()

    def inject_marker(self, marker_value, marker_label):
        marker_time = time.time() * 1000
        self.c.inject_marker_request(marker_time, marker_value, marker_label, port='python_app')

    def stop_record(self):
        self.c.stop_record()

    # Callbacks
    def on_create_session_done(self, *args, **kwargs):
        print('Session created')
        self.c.create_record(self.record_title, description=self.record_description)

    def on_create_record_done(self, *args, **kwargs):
        data = kwargs.get('data')
        self.record_id = data['uuid']
        print(f'Record created: {self.record_id}')

    def on_stop_record_done(self, *args, **kwargs):
        print('Record stopped')
        self.c.disconnect_headset()

    def on_inject_marker_done(self, *args, **kwargs):
        data = kwargs.get('data')
        marker_id = data['uuid']
        print(f'Marker injected: {marker_id}')

    def on_warn_cortex_stop_all_sub(self, *args, **kwargs):
        self.c.export_record(self.record_export_folder, self.record_export_data_types, self.record_export_format,
                             [self.record_id], self.record_export_version)

    def on_export_record_done(self, *args, **kwargs):
        print('Record exported')
        self.c.close()

    def on_inform_error(self, *args, **kwargs):
        print(kwargs.get('error_data'))

def start_recording():
    global marker_handler
    # Initialize the Marker handler
    your_app_client_id = 'UKYzJ29onUzUizejl6jLZui5HdWplC4AGZyh7sqf'
    your_app_client_secret = '8xXsb6e11kDpsHWmKCY7LsGgB28IXYo5HUwd82rvlrxZdwS70e9Pz4CmTTkKGJqKv6nivfo83lcwvaKXTNYtp45NlwcI26FNXaEgOry6oJ7JUn7hLND9CvQOJ1QOMH1Q'

    current_time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    marker_handler = MarkerHandler(your_app_client_id, your_app_client_secret)
    marker_handler.start(
        record_title=f'AOE_{current_time_str}',
        record_description='',
        folder='D:\\Upenn\\OneDrive - PennO365\\robotics research\\LilFlo\\FloSystemV2\\trail_control\\cortex-example\\python\\record_data',
        stream_types=['EEG', 'PM', 'BP'],
        export_format='CSV',
        version='V2'
    )

def send_movement_via_mqtt(movement_number, topic):
    message = str(movement_number)
    client.publish(topic, message)
    print(f"Movement {movement_number} sent to topic {topic}")

def play_instructions():
    # Play instruction files
    instruction_sounds = ['mp3_AOE/instruction1.mp3', 'mp3_AOE/instruction2.mp3']
    for sound_file in instruction_sounds:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

def main():
    global marker_handler

    pygame.mixer.init()
    serial_port = 'COM5'
    ser = serial.Serial(serial_port, 9600)
    time.sleep(2)

    movement_topic = "ros/mqtt/movement"
    feedback_topic = "ros/mqtt/feedback"

    # Movements for each round and rounds list
    movements = ['Movement 1', 'Movement 2', 'Movement 3', 'Movement 4']
    # random.shuffle(movements)
    n_rounds = 3
    rounds = [movements.copy() for _ in range(n_rounds)]

    current_step = 0
    current_round = 0
    awaiting_feedback = False
    is_resting = False

    root = tk.Tk()
    root.title("Experiment Control")

    status_var = StringVar()
    status_var.set("Initializing...")

    def update_status():
        if is_resting:
            status_var.set("Resting... Click 'Next Round' to proceed.")
            next_round_button.config(state=tk.NORMAL)  # Enable "Next Round" button
        elif current_step < len(rounds[current_round]):
            status_var.set(f"Running: {rounds[current_round][current_step]} | Next: {rounds[current_round][(current_step + 1) % len(rounds[current_round])]}")

        else:
            status_var.set("End of experiment")

    def send_command(command):
        ser.write(command.encode())

    def on_feedback_message(client, userdata, message):
        nonlocal awaiting_feedback
        payload = message.payload.decode()
        if payload == 'A':
            awaiting_feedback = True

    client.message_callback_add(feedback_topic, on_feedback_message)

    def next_step():
        nonlocal current_step, current_round, awaiting_feedback, is_resting

        if is_resting:
            is_resting = False
            current_step = 0
            next_round_button.config(state=tk.DISABLED)  # Disable "Next Round" button after starting
            update_status()
            return

        if current_step < len(rounds[current_round]):
            status_var.set("Fixation Cross")
            send_command('1')
            marker_handler.inject_marker("1000", "fixationCross")
            time.sleep(1)
            send_command('0')
            marker_handler.inject_marker("2000", "Square")
            status_var.set("Square")
            send_command('2')
            time.sleep(1)

            movement_number = ''.join(filter(str.isdigit, rounds[current_round][current_step]))
            send_movement_via_mqtt(movement_number, movement_topic)
            marker_handler.inject_marker("3000", "Movement_start")

            awaiting_feedback = False
            status_var.set("Waiting for feedback 'A'")
            while not awaiting_feedback:
                client.loop()
            marker_handler.inject_marker("4000", "Movement_end")
            time.sleep(1)

            status_var.set("Fixation Cross")
            send_command('1')
            marker_handler.inject_marker("1000", "fixationCross")
            time.sleep(1)
            send_command('0')

            status_var.set("Triangle")
            send_command('3')
            marker_handler.inject_marker("5000", "Triangle")
            time.sleep(5)
            send_command('0')

            current_step += 1
            if current_step >= len(rounds[current_round]):
                is_resting = True
                status_var.set("Resting... Click 'Next Round' to proceed.")
                current_round += 1
                if current_round >= len(rounds):
                    status_var.set("End of experiment")
                    marker_handler.stop_record()
                    pygame.quit()
                    root.quit()
                    return
            update_status()
        else:
            status_var.set("End of experiment")
            marker_handler.stop_record()
            pygame.quit()
            root.quit()

    def start_experiment(play_instruction=False):
        start_button.pack_forget()
        instruction_button.pack_forget()
        if play_instruction:
            play_instructions()
        update_status()
        next_button.pack(pady=10)

    # Initial GUI setup for start options
    status_label = tk.Label(root, textvariable=status_var, font=("Arial", 16))
    status_label.pack(pady=10)

    instruction_button = tk.Button(root, text="Play Instruction", command=lambda: start_experiment(play_instruction=True), font=("Arial", 16))
    instruction_button.pack(pady=10)

    start_button = tk.Button(root, text="Start Movement Only", command=lambda: start_experiment(play_instruction=False), font=("Arial", 16))
    start_button.pack(pady=10)

    next_button = tk.Button(root, text="Next Movement", command=next_step, font=("Arial", 16))
    next_button.pack_forget()

    next_round_button = tk.Button(root, text="Next Round", command=next_step, font=("Arial", 16))
    next_round_button.pack(pady=10)
    next_round_button.config(state=tk.DISABLED)  # Initially disabled

    update_status()
    threading.Thread(target=start_recording).start()
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
