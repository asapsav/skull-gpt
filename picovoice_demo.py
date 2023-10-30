import pvporcupine
import dotenv
import os
import pyaudio
import numpy as np

dotenv.load_dotenv()

pico_key = os.getenv("PICO_ACCES_KEY")

porcupine = pvporcupine.create(
  access_key=pico_key,
  keyword_paths=['picovoice_models/yo-skull_en_mac_v3_0_0.ppn']
)

pa = pyaudio.PyAudio()

audio_stream = pa.open(
    rate=16000,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length,
    input_device_index=None
)

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = np.frombuffer(pcm, dtype=np.int16)
        keyword_index = porcupine.process(pcm)
        
        if keyword_index == 0:
            print("detected 'yo skull'")
        elif keyword_index == 1:
            print('detected `bumblebee`')
            
finally:
    audio_stream.stop_stream()
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
