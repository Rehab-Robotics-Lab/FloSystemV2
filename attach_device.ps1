usbipd attach --wsl --hardware-id 0403:6014
usbipd attach --wsl --hardware-id 046d:08e5
Start-Job { usbipd attach --wsl --hardware-id 0403:6014 --auto-attach }
Start-Job { usbipd attach --wsl --hardware-id 046d:08e5 --auto-attach }
usbipd list