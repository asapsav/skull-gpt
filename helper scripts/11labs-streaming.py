import os
import dotenv
dotenv.load_dotenv()
from elevenlabs import set_api_key, play, generate, stream


#import api key from .env file
ELEVENLABS_API = os.getenv("ELEVENLABS_API")
set_api_key(ELEVENLABS_API)


def text_stream():
    yield "Hello motherfucker"
    yield "This is an evil skull talking"
    yield "Why? Why did you summon me?"
    yield "What do you need?"
    yield "I AM ANGRY!!"

audio_stream = generate(
    text=text_stream(),
    voice="skull_0",
    model="eleven_monolingual_v1",
    stream=True
)

stream(audio_stream)
