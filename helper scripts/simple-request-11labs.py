import requests
import dotenv
import os

# Load .env and set API keys
dotenv.load_dotenv()
ELEVENLABS_API = os.getenv("ELEVENLABS_API")
print(ELEVENLABS_API)

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/batman"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": ELEVENLABS_API
}

data = {
  "text": "Hi! My name is Bella, nice to meet you!",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
print(response)