import elevenlabs
import os
import dotenv
from elevenlabs import VoiceSettings

dotenv.load_dotenv()

#import api key from .env file
ELEVENLABS_API = os.getenv("ELEVENLABS_API")
elevenlabs.set_api_key(ELEVENLABS_API)

from elevenlabs import clone

settings = VoiceSettings(speaking_rate=0.8, pitch=0.5, stability=0.7, similarity_boost=1)  

voice = clone(
   name = "batman",
   files = ["helper scripts/Ben Affleck Batman voice.mp3"],
   settings = settings
)
