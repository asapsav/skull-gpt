import requests
import time

# Replace with your ESP32's IP address
esp_ip = "192.168.7.139"

def toggle_led(state):
    if state.lower() == 'on':
        requests.get(f'http://{esp_ip}/H')
    elif state.lower() == 'off':
        requests.get(f'http://{esp_ip}/L')

# Example usage:
while True:
    toggle_led('on')
    time.sleep(1)  # Keep the LED on for 2 seconds
    toggle_led('off')
    time.sleep(1)
