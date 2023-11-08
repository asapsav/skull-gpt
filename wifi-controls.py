import requests
import time
import dotenv
import os
dotenv.load_dotenv()

esp_ip = os.getenv("esp_ip")


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
