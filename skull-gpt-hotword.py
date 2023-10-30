import os
import openai
import dotenv
import serial
from elevenlabs import set_api_key, generate, stream
import speech_recognition as sr
import pvporcupine
import serial.tools.list_ports
import pyaudio
import numpy as np

# ISSUE WITH THE CODE:
# after detecting the hotword, the program crashes with the following error:
# ||PaMacCore (AUHAL)|| Error on line 2523: err='-50', msg=Unknown Error





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
PICO_ACCES_KEY = os.getenv("PICO_ACCES_KEY")
set_api_key(ELEVENLABS_API)

SKULL_SYSTEM_PROMPT = """You are an evil bro skull. It is halloween season. 
You are very sarcastic and you try to trick user all the time.
 But you are also a bro. You are aggressive.
 You also have a studip scorpion friend, but scorpion does not talk. 
 You can sometimes forward user questions to the skorpion. Keep your answers short."""


    

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

    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        print(pa.get_device_info_by_index(i))
    stream_pa = pa.open(rate=16000,
                     channels=1,
                     format=pyaudio.paInt16,
                     input=True,
                     frames_per_buffer=512)

    # Initialize the recognizer and Porcupine
    r = sr.Recognizer()
    porcupine = pvporcupine.create(access_key = PICO_ACCES_KEY, keywords=["alexa"])

    try:
        while True:
            print("Listening for hotwords...")
            pcm = np.frombuffer(stream_pa.read(512), dtype=np.int16)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Listening for your command...")
                mic = sr.Microphone()
                with mic as source:
                    r.adjust_for_ambient_noise(source)
                    audio_command = r.listen(source)
                    try:
                        user_input = r.recognize_google(audio_command)
                        print(f"User: {user_input}")

                        # Code to process the command 

                        if user_input is None:  # Skip the loop if no speech recognized
                            print("No speech recognized. Skipping.")
                            continue

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
                        print(f"Assistant: {assistant_message}")
                        stream(audio_stream)
                        arduino.write(b's') 
                        
                        messages.append({"role": "assistant", "content": assistant_message})

                    except sr.UnknownValueError:
                        print("Could not understand the command.")
                    except sr.RequestError:
                        print("Could not request results, check your network connection.")
            
    except KeyboardInterrupt:
        print("Exiting...")
        arduino.write(b's') 
    except Exception as e:
        print(f"An error occurred: {e}")
        arduino.write(b's') 
        stream_pa.close()
        pa.terminate()
        arduino.close()

    stream_pa.close()
    pa.terminate()
    arduino.close()

if __name__ == "__main__":
    main()
