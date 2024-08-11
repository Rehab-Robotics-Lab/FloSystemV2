import serial
import time

# Set up the serial connection (adjust the port to match your setup)
serial_port = '/dev/ttyACM0'  # Replace with your actual serial port
baud_rate = 9600

try:
    # Open the serial port
    ser = serial.Serial(serial_port, baud_rate)
    time.sleep(2)  # Wait for the serial connection to initialize

    def send_command(command):
        """Send a command to the serial device."""
        ser.write(command.encode())
        time.sleep(0.1)  # Small delay to ensure the command is processed

    # Example usage
    send_command('4')  # Send '1' to turn on the LED
    time.sleep(50)      # Keep the LED on for 5 seconds
    send_command('0')  # Send '0' to turn off the LED

except serial.SerialException as e:
    print(f"Error opening serial port {serial_port}: {e}")

finally:
    # Close the serial connection
    if ser.is_open:
        ser.close()
