import pygame
from psychopy import visual, core
import tkinter as tk
from tkinter import StringVar
import time
import serial
import paho.mqtt.client as mqtt

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Set up the serial connection (adjust the port to match your setup)
serial_port = 'COM5'
ser = serial.Serial(serial_port, 9600)  # Open the serial port
time.sleep(2)  # Wait for the serial connection to initialize

# Initialize MQTT client
broker_address = "172.20.10.6"  # Change to your broker address
broker_port = 1883
mqtt_client = mqtt.Client(client_id="MovementPublisher", protocol=mqtt.MQTTv5)  # Using MQTT version 5

# Define the MQTT topic
movement_topic = "ros/mqtt/movement"

# Connect to the MQTT broker
mqtt_client.connect(broker_address, broker_port)

# Initialize PsychoPy window
win = visual.Window([800, 600], fullscr=False, monitor="testMonitor", units="deg")

# Define the cross (not used for visual, but for marker)
cross = visual.TextStim(win, text="+", pos=(0, 0), height=0.1, color='white')

# Instruction sound files
instruction_sounds = [
    'instruction1.mp3',  # Replace with actual file paths
    'instruction2.mp3',
    'instruction3.mp3',
    'instruction4.mp3'
]

# Define movements (added Movement 6)
movements = ['Movement 1', 'Movement 2', 'Movement 3', 'Movement 4', 'Movement 5', 'Movement 6']

# Current step index
current_step = 0

# Create the main GUI application window
root = tk.Tk()
root.title("Experiment Control")

# Status variable to display current process
status_var = StringVar()
status_var.set("Start")

# Function to update the status label
def update_status():
    if current_step == 0:
        status_var.set("Play Instruction 1-2")
    elif current_step == 1:
        status_var.set("Cross Sound and Display")
    elif current_step == 2:
        status_var.set("Play Instruction 3-4")
    elif current_step >= 3 and current_step < 3 + len(movements):
        status_var.set(f"{movements[current_step - 3]}")
    elif current_step >= 3 + len(movements):
        status_var.set("End")

# Function to play a sound
def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        core.wait(0.1)

# Function to send a command via serial
def send_command(command):
    ser.write(command.encode())
    time.sleep(0.1)  # Small delay to ensure the command is processed

# Function to proceed to the next step
def next_step():
    global current_step
    if current_step == 0:
        # Initially close the cross
        send_command('0')
        add_marker("Cross Initial Close 0")

        # Play instruction 1-2
        play_sound(instruction_sounds[0])
        play_sound(instruction_sounds[1])
    elif current_step == 1:
        # Play cross sound and display cross for 5 seconds
        play_sound('cross_sound.mp3')  # Replace with the cross sound file
        add_marker("Cross Sound End")
        send_command('1')  # Turn on cross on the LED matrix
        add_marker("Cross Open 1")
        core.wait(5.0)  # Display cross for 5 seconds
        send_command('0')  # Turn off cross on the LED matrix
        add_marker("Cross Close 0")
    elif current_step == 2:
        # Play instruction 3-4
        play_sound(instruction_sounds[2])
        play_sound(instruction_sounds[3])
        add_marker("Instruction 3-4 Played")
    elif current_step >= 3 and current_step < 3 + len(movements):
        # Show cross for 3 seconds, then indicate movement
        send_command('1')  # Turn on cross on the LED matrix
        add_marker(f"Cross for {movements[current_step - 3]} Open 1")
        core.wait(3.0)  # Display cross for 3 seconds
        send_command('0')  # Turn off cross on the LED matrix
        add_marker(f"Cross for {movements[current_step - 3]} Close 0")
        core.wait(5.0)  # Wait 5 seconds before indicating movement
        print(movements[current_step - 3])
        add_marker(movements[current_step - 3])
        
        # Send the movement command via MQTT
        mqtt_client.publish(movement_topic, str(current_step - 2))
        print(f"Published Movement {current_step - 2} to MQTT")

    else:
        # End the experiment
        status_var.set("End")
        win.close()
        core.quit()
        pygame.quit()
        root.quit()
        return

    # Update current step
    current_step += 1
    update_status()

# Function to add markers for EEG data logging
def add_marker(label):
    timestamp = time.time()
    print(f"Marker {label}: {timestamp}")

# Create GUI elements
status_label = tk.Label(root, textvariable=status_var, font=("Arial", 16))
status_label.pack(pady=10)

next_button = tk.Button(root, text="Next", command=next_step, font=("Arial", 16))
next_button.pack(pady=10)

# Initialize the status
update_status()

# Start the Tkinter main loop
root.mainloop()
