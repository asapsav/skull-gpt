import os
import openai
import dotenv
import serial
import time
from elevenlabs import set_api_key, play, generate, stream
import speech_recognition as sr
import serial.tools.list_ports

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'USB2.0-Serial' in p.description:
            return p.device
    return None

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



def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None  # Return None if audio is not understood
    except sr.RequestError:
        return "Could not request results; check network"

    

def main():
    try:
        arduino_port = find_arduino_port()
        arduino = serial.Serial(arduino_port, 9600)
        while True:  # handshake to prevent any signals from being lost
            if arduino.readline().decode('ascii').strip() == "READY":
                print(f"Arduino connected: {arduino.name}")
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
            #user_input = input("You: ")
            print("Listening...")
            user_input = recognize_speech()
            if user_input is None:  # Skip the loop if no speech recognized
                print("No speech recognized. Skipping.")
                continue
            print(f"You: {user_input}")
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
                stream=True, 
                latency=4
            )
            arduino.write(b'g')
            #print(f"Assistant: {assistant_message}")
            stream(audio_stream)
            arduino.write(b's') 
            # we gotta fix this because after arduino.write(b'P') 
            # skull moves for 20 secs and 
            # 1) we ahve to stop moving after end of 11labs streaming
            # 2) we have to  keep moving while streaming is happenidn
            # probabry should use threading
            
            messages.append({"role": "assistant", "content": assistant_message})
            
    except KeyboardInterrupt:
        print("Exiting...")
        arduino.write(b's') 
    except Exception as e:
        print(f"An error occurred: {e}")
        arduino.write(b's') 

    arduino.close()

if __name__ == "__main__":
    main()
