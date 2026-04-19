# LED commands:

import logging
import os
import time

try:
    import serial
except ImportError:  # pragma: no cover - depends on runtime environment
    serial = None

LOG = logging.getLogger(__name__)

MAPPING_TRIAL_EVENTS_TO_LED_COMMANDS = {
    "fixationCross": "1",  # cross
    "stimulusOnset": "2",  # square
    "displayCDFiveToOne": "5",  # countdown 5->1 animation
    "intertrial_interval": "0",  # off
    "off": "0",
}

DEFAULT_SERIAL_PORT = "/dev/flo_led"
DEFAULT_BAUD_RATE = 9600


class LedController:
    def __init__(self, port=None, baud_rate=None, connect_delay=2.0, write_delay=0.1):
        self.port = port or os.environ.get("LED_SERIAL_PORT", DEFAULT_SERIAL_PORT)
        self.baud_rate = int(baud_rate or os.environ.get("LED_SERIAL_BAUD", DEFAULT_BAUD_RATE))
        self.connect_delay = float(os.environ.get("LED_SERIAL_CONNECT_DELAY", connect_delay))
        self.write_delay = float(os.environ.get("LED_SERIAL_WRITE_DELAY", write_delay))
        self.ser = None
        self.available = False
        self.last_error = None

        self._connect()

    def _connect(self):
        if serial is None:
            self.last_error = "pyserial is not installed"
            LOG.warning("LED serial unavailable: %s", self.last_error)
            return

        try:
            self.ser = serial.Serial(self.port, self.baud_rate)
            time.sleep(self.connect_delay)
            self.available = True
            self.last_error = None
            LOG.info("Connected to LED serial port %s at %s baud", self.port, self.baud_rate)
        except Exception as exc:
            self.ser = None
            self.available = False
            self.last_error = str(exc)
            LOG.warning("Failed to open LED serial port %s: %s", self.port, exc)

    def send_command(self, command):
        if not self.available or self.ser is None:
            return False

        payload = str(command).encode()
        self.ser.write(payload)
        time.sleep(self.write_delay)
        return True

    def set_led_state(self, command_or_event):
        command = MAPPING_TRIAL_EVENTS_TO_LED_COMMANDS.get(str(command_or_event), str(command_or_event))
        return self.send_command(command)

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
