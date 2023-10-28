import os
import openai
import dotenv
import serial
import time
from elevenlabs import set_api_key, play, generate, stream

# Load .env and set API keys
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API = os.getenv("ELEVENLABS_API")
set_api_key(ELEVENLABS_API)

SKULL_SYSTEM_PROMPT = """You are an evil bro skull. It is halloween season. 
You are very sarcastic and you try to trick user all the time.
 But you are also a bro. You are aggressive.
 You also have a studip scorpion friend, but scorpion does not talk. 
 You can sometimes forward user questions to the skorpion. Keep your answers short."""

def main():
    try:
        from tqdm import tqdm

        arduino = serial.Serial('/dev/cu.usbserial-2110', 9600)
        while True:  # handshake to prevent any signals from being lost
            if arduino.readline().decode('ascii').strip() == "READY":
                print(f"Arduino connected: {arduino.name}, wait 2 sec for it to blink")
                for _ in tqdm(range(2), desc='Waiting'):
                    time.sleep(1)
                break
    except Exception as e:
        print(f"Failed to connect to Arduino: {e}")
        return

    messages = [
        {"role": "system", "content": SKULL_SYSTEM_PROMPT}
    ]

    # from pydub import AudioSegment
    # import pydub.playback 
    # # Load MP3 file into pydub
    # buffer_0 = AudioSegment.from_mp3("buffer_0.mp3")
    # pydub.playback.play(buffer_0)
    try:
        while True:
            user_input = input("You: ")
            messages.append({"role": "user", "content": user_input})
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            assistant_message = completion.choices[0].message['content']
            
            def assistant_speech(text):
                yield text

            audio_stream = generate(
                text=assistant_speech(assistant_message),
                voice="batman",
                model="eleven_monolingual_v1",
                stream=True
            )
            arduino.write(b'P')
            print(f"Assistant: {assistant_message}")
            stream(audio_stream)
            arduino.write(b'P') 
            # we gotta fix this because after arduino.write(b'P') 
            # skull moves for 20 secs and 
            # 1) we ahve to stop moving after end of 11labs streaming
            # 2) we have to  keep moving while streaming is happenidn
            # probabry should use threading
            
            messages.append({"role": "assistant", "content": assistant_message})
            
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")

    arduino.close()

if __name__ == "__main__":
    main()
