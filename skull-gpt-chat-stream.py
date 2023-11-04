import os
import openai
import dotenv
import serial
from elevenlabs import set_api_key, play, generate, stream
import serial.tools.list_ports

# This version uses threading to stream GPT respones, 
# collect them in batches, send them to ElevenLabs and stream the audio 
# all concurrently. This is an attempt to make the most efficient way to stream audio from GPT.

# Under development

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'USB2.0-Serial' in p.description:
            return p.device
    return None

# Load .env and set API keyssay hi
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API = os.getenv("ELEVENLABS_API")
set_api_key(ELEVENLABS_API)

SKULL_SYSTEM_PROMPT = """You are an evil bro skull. It is halloween season. 
You are very sarcastic and you try to trick user all the time. You also write limerics.
 But you are also a bro. You are aggressive.
 You also have a stupid scorpion friend, but scorpion does not talk. 
 You can sometimes forward user questions to the skorpion. Keep your answers short. 
 You were build from a skul from Ace Hardware, 10$ walgreens speaker, an arduino, and a couple of toy electric parts."""

# Come up with good prank for this hackathon
# Write a limeric about scorpion
import threading
from queue import Queue    
import time

def collect_openai_responses(response_openai, queue, messages):
    collected_messages, messages_batch = [], []
    batch_counter, sentence_counter = 0, 0

    for chunk in response_openai:
        chunk_delta = chunk['choices'][0]['delta']
        collected_messages.append(chunk_delta)
        messages_batch.append(chunk_delta)

        if any(punct in chunk_delta.get('content', '') for punct in ".!?"):
            sentence_counter += 1

        batch_counter += 1

        if sentence_counter >= 4 or batch_counter >= 50 or chunk['choices'][0].get('finish_reason') == "stop":
            batch_reply_content = ''.join(m.get('content', '') for m in messages_batch)
            print(f"Skull: {batch_reply_content}")
            queue.put(batch_reply_content)
            messages_batch.clear()
            batch_counter, sentence_counter = 0, 0
        
    # Combine chunks into full text
    full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
    messages.append({"role": "assistant", "content": full_reply_content})

def generate_and_stream_audio(queue):
    while True:
        text = queue.get()  # get text from the queue
        if text is None: break  # None is the signal to stop
        
        # Convert text to speech and stream
        audio_stream = generate(
            text=text,
            voice="batman",
            model="eleven_monolingual_v1",
            stream=True, 
            latency=4
        )
        stream(audio_stream)
        queue.task_done()

def main(arduino=None):

    messages = [
        {"role": "system", "content": SKULL_SYSTEM_PROMPT}
    ]

    try:
        while True:
            user_input = input("You: ")
            start_time = time.time()
            messages.append({"role": "user", "content": user_input})

            response_openai = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages, 
                stream=True
            )

            # Create a queue to communicate between threads
            message_queue = Queue()

            # Start the thread that collects OpenAI responses
            openai_thread = threading.Thread(target=collect_openai_responses, args=(response_openai, message_queue, messages))
            openai_thread.start()

            # Start the thread that generates and streams audio
            audio_thread = threading.Thread(target=generate_and_stream_audio, args=(message_queue,))
            audio_thread.start()

            # Wait for the OpenAI response collection to finish
            openai_thread.join()

            # Signal the audio thread to stop
            message_queue.put(None)

            # Wait for the audio thread to finish
            audio_thread.join()
            
    except KeyboardInterrupt:
        print("Exiting...")
        if arduino:
            arduino.write(b's')
            arduino.close() 
    except Exception as e:
        print(f"An error occurred: {e}")
        if arduino:
            arduino.write(b's')
            arduino.close() 

if __name__ == "__main__":
    try:
        arduino_port = find_arduino_port()
        arduino = serial.Serial(arduino_port, 9600)
        while arduino.readline().decode('ascii').strip() != "READY":
            pass
        print(f"Arduino connected: {arduino.name}")
        main(arduino)
    except Exception as e:
        print(f"Failed to connect to Arduino: {e}")
        main()
