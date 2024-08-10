#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import time
import os
import threading
import paho.mqtt.client as mqtt

# Define the broker address and port
broker_address = "172.20.10.6"  # Change to your broker address
broker_port = 1883

# Create a client instance
mqtt_client = mqtt.Client("Publisher")

# Connect to the broker
mqtt_client.connect(broker_address, broker_port)

# Define the MQTT topic
movement_topic = "ros/mqtt/movement"

class ControlGUI:
    def __init__(self, root, display_gui):
        self.root = root
        self.display_gui = display_gui
        self.root.title("Control Panel")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")

        self.start_time = time.time()
        self.log_time("Control GUI started")

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Choose a mode:", font=("Arial", 20), bg="#f0f0f0").place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.mode1_button = tk.Button(self.root, text="Robot Movement Imitation with Object", font=("Arial", 16), command=self.mode_with_object)
        self.mode1_button.place(relx=0.5, rely=0.3, relwidth=0.5, anchor=tk.CENTER)

        self.mode2_button = tk.Button(self.root, text="Robot Movement Imitation without Object", font=("Arial", 16), command=self.mode_without_object)
        self.mode2_button.place(relx=0.5, rely=0.5, relwidth=0.5, anchor=tk.CENTER)
        
        self.quit_button = tk.Button(self.root, text="Quit", font=("Arial", 16), command=self.quit)
        self.quit_button.place(relx=0.5, rely=0.7, relwidth=0.5, anchor=tk.CENTER)

    def mode_with_object(self):
        self.clear_window()
        tk.Label(self.root, text="Select a Movement:", font=("Arial", 20), bg="#f0f0f0").place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        for i in range(1, 5):
            tk.Button(self.root, text=f"Movement {i}", font=("Arial", 16), command=lambda i=i: self.perform_movement(i)).place(relx=0.5, rely=0.2 + i*0.15, relwidth=0.5, anchor=tk.CENTER)
        
        self.back_button = tk.Button(self.root, text="Back", font=("Arial", 16), command=self.create_main_menu)
        self.back_button.place(relx=0.5, rely=0.85, relwidth=0.5, anchor=tk.CENTER)

    def mode_without_object(self):
        self.clear_window()
        detected_objects = self.detect_objects()
        tk.Label(self.root, text="Select an Object:", font=("Arial", 20), bg="#f0f0f0").place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        for idx, obj in enumerate(detected_objects):
            tk.Button(self.root, text=obj, font=("Arial", 16), command=lambda obj=obj: self.perform_object_movement(obj)).place(relx=0.5, rely=0.3 + idx*0.2, relwidth=0.5, anchor=tk.CENTER)

        self.back_button = tk.Button(self.root, text="Back", font=("Arial", 16), command=self.create_main_menu)
        self.back_button.place(relx=0.5, rely=0.85, relwidth=0.5, anchor=tk.CENTER)

    def detect_objects(self):
        # Placeholder for running a shell script to detect objects
        # Replace with actual shell script command
        # os.system("path/to/detect_objects.sh")
        detected_objects = ["Object A", "Object B", "Object C"]  # Example detected objects
        return detected_objects

    def perform_movement(self, movement_id):
        self.display_gui.show_message(f"Focus on the robot movement and stay for 3 seconds. Performing Movement {movement_id}")
        self.log_time(f"Started Movement {movement_id}")
        
        self.play_sound("start_sound.mp3")
        self.root.after(3000, lambda: self.run_robot_script(movement_id))

    def perform_object_movement(self, obj):
        self.display_gui.show_message(f"Focus on the robot movement and stay for 3 seconds. Performing Movement with {obj}")
        self.log_time(f"Started Movement with {obj}")
        
        self.play_sound("start_sound.mp3")
        self.root.after(3000, lambda: self.run_robot_script(obj))

    def run_robot_script(self, identifier):
        # Publish the movement identifier to the MQTT topic
        mqtt_client.publish(movement_topic, str(identifier))
        print(f"Published Movement {identifier} to MQTT")
        # Placeholder for running a shell script for the robot
        # Replace with actual shell script command
        # os.system(f"path/to/robot_script_{identifier}.sh")
        self.display_gui.show_message(f"Imitate the movement: {identifier}")
        self.log_time(f"Finished Movement {identifier}")
        self.play_sound("finish_sound.mp3")
        self.create_main_menu()

    def play_sound(self, sound_file):
        # Placeholder for playing a sound file
        # Replace with actual sound playing command
        # os.system(f"play {sound_file}")
        pass

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def log_time(self, action):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        log_entry = f"{action} at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))} (elapsed: {elapsed_time:.2f} seconds)"
        print(log_entry)

    def quit(self):
        self.root.quit()
        self.display_gui.root.quit()

class DisplayGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Display Panel")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")

        self.start_time = time.time()
        self.log_time("Display GUI started")

        self.message_var = tk.StringVar(value="")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Current Message:", font=("Arial", 20), bg="#f0f0f0").place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        tk.Label(self.root, textvariable=self.message_var, font=("Arial", 16), bg="#f0f0f0").place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    def show_message(self, message):
        # Schedule the update to happen in the main thread
        self.root.after(0, self.message_var.set, message)
        self.log_time(message)

    def log_time(self, action):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        log_entry = f"{action} at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))} (elapsed: {elapsed_time:.2f} seconds)"
        print(log_entry)

def run_control_gui(display_gui):
    control_root = tk.Tk()
    control_gui = ControlGUI(control_root, display_gui)
    control_root.mainloop()

def run_display_gui():
    display_root = tk.Tk()
    display_gui = DisplayGUI(display_root)
    display_thread = threading.Thread(target=run_control_gui, args=(display_gui,))
    display_thread.start()
    display_root.mainloop()

if __name__ == "__main__":
    run_display_gui()
