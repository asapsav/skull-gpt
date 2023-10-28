import os
import dotenv
dotenv.load_dotenv()
from elevenlabs import set_api_key, play, generate, stream

#import api key from .env file
ELEVENLABS_API = os.getenv("ELEVENLABS_API")
set_api_key(ELEVENLABS_API)

audio = generate(
  text="Ha ha ha ha ha ha haaaaaa...",
  voice="skull_0",
  model="eleven_monolingual_v1"
)
# Open a new MP3 file in binary write mode and save the bytes
with open('buffer_0.mp3', 'wb') as f:
    f.write(audio)