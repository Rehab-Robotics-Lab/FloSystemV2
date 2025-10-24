import pygame
import tkinter as tk
from tkinter import StringVar
import time
import serial
import threading
import paho.mqtt.client as mqtt
from cortex import Cortex
import datetime
import pandas as pd
from threading import Lock
feedback_lock = Lock()
# Global marker handler and variables
marker_handler = None
action_table = None
awaiting_feedback = False
step2_done = False


class MarkerHandler():
    def __init__(self, app_client_id, app_client_secret, **kwargs):
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


def on_feedback_message(client, userdata, message):
    global awaiting_feedback
    payload = message.payload.decode()
    print(f"Feedback received: {payload}")
    if payload == 'A':
        awaiting_feedback = True


def main():
    global marker_handler, action_table, awaiting_feedback, step2_done

    pygame.mixer.init()

    serial_port = 'COM5'
    try:
        ser = serial.Serial(serial_port, 9600)
        print(f"Connected to serial port: {serial_port}")
        time.sleep(2)
    except Exception as e:
        print(f"Failed to connect to serial port: {e}")
        return

    action_table = pd.read_excel("AOE_obj_list.xlsx")

    root = tk.Tk()
    root.title("Experiment Control")

    status_var = StringVar()
    status_var.set("Initializing...")

    def update_status(text):
        status_var.set(text)

    def serial_command(command):
        try:
            ser.write(command.encode())
            print(f"Serial command sent: {command}")
        except Exception as e:
            print(f"Failed to send serial command: {e}")

    def start_step2():
        global step2_done
        update_status("Fixation Cross (1s).")
        serial_command('1')
        marker_handler.inject_marker(1000, "Fixation Cross")
        time.sleep(1)
        step2_done = True
        update_status("Step 2 completed. Proceeding to Step 3.")

    def redo_step2():
        global step2_done
        update_status("Redoing Step 2: Fixation Cross (1s).")
        serial_command('1')
        marker_handler.inject_marker(1000, "Fixation Cross")
        time.sleep(1)
        step2_done = True
        update_status("Step 2 redone. Proceeding to Step 3.")

    def run_experiment():
        global step2_done
        n_blocks = action_table['blockNumber'].max()
        for block_id in range(1, n_blocks + 1):
            block_data = action_table[action_table['blockNumber'] == block_id]
            update_status(f"Block {block_id}/{n_blocks} started.")

            for _, row in block_data.iterrows():
                stim_label = row['stimLabel']
                marker_val = row['markerVal']
                condition_num = row['mqttNum']

                update_status(f"Resting for 3 seconds before {stim_label}.")
                time.sleep(3)

                update_status("Waiting for user to start Step 2.")
                step2_done = False
                while not step2_done:
                    time.sleep(0.1)

                update_status(f"Running: {stim_label}")
                serial_command('2')
                marker_handler.inject_marker(marker_val, row['stimulus'])
                send_movement_via_mqtt(condition_num, "ros/mqtt/movement")

                # Step 4: Wait for feedback
                awaiting_feedback = False
                status_var.set("Waiting for feedback 'A'")
                timeout = 10  # 最大等待时间为10秒
                start_time = time.time()

                while True:
                    with feedback_lock:
                        if awaiting_feedback:
                            print("Feedback received. Proceeding to Step 5.")
                            break
                    if time.time() - start_time > timeout:
                        print("Timeout while waiting for feedback. Proceeding anyway.")
                        break
                    client.loop(timeout=0.1)  # 处理 MQTT 消息队列
                    time.sleep(0.1)


                update_status("Fixation Cross (1s) after feedback.")
                serial_command('1')
                marker_handler.inject_marker(1000, "Fixation Cross")
                time.sleep(1)

                update_status("Running 5-second Triangle.")
                serial_command('3')
                marker_handler.inject_marker(100 + marker_val, row['stimulus'])
                time.sleep(5)
                serial_command('0')

            update_status(f"Block {block_id} complete. Resting for 15 seconds.")
            time.sleep(15)

        update_status("Experiment complete!")

    status_label = tk.Label(root, textvariable=status_var, font=("Arial", 16))
    status_label.pack(pady=20)

    step2_button = tk.Button(root, text="Start Step 2", command=start_step2, font=("Arial", 16))
    step2_button.pack(pady=10)

    redo_step2_button = tk.Button(root, text="Redo Step 2", command=redo_step2, font=("Arial", 16))
    redo_step2_button.pack(pady=10)

    start_button = tk.Button(root, text="Start Experiment",
                             command=lambda: threading.Thread(target=run_experiment).start(), font=("Arial", 16))
    start_button.pack(pady=10)

    threading.Thread(target=start_recording).start()
    root.mainloop()


if __name__ == '__main__':
    broker_ip = "169.254.131.1"
    client = mqtt.Client()
    client.on_message = on_feedback_message

    try:
        client.connect(broker_ip, 1883, 60)
        print(f"Connected to MQTT Broker at {broker_ip}")
        client.subscribe("ros/mqtt/feedback")
    except Exception as e:
        print(f"Failed to connect to MQTT Broker: {e}")
        #         # Return to avoid running without feedback handling
        #         # return

    main()

