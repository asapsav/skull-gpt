### Getting Started (generated by gpt, be carefull)

#### The very silly version requires:
- Python 3.x
- Arduino with Serial interface
- Install dependencies: 
  ```bash
  pip install python-dotenv openai pyserial elevenlabs
  ```
- `.env` file with `OPENAI_API_KEY`, `ELEVENLABS_API` and `PICO_ACCES_KEY` (optional)
- one skull with a motorized jaw and LED eyes.

#### Functionality
This script connects to an Arduino via serial, simulates an "evil bro skull" chatbot for Halloween using GPT-3.5-turbo and ElevenLabs API for voice generation. It reads user inputs, processes them, and plays the voice back.

#### How to Run
1. Load the required Arduino code onto your Arduino.
2. Connect the Arduino to your computer.
3. Fill in your `.env` file with the API keys.
4. To chat with skull, run:
    ```bash
    python skull-gpt-chat.py
    ```
5. To speak with skull, run:
    ```bash
    python skull-gpt-voice.py
    ```
    
#### Latencies breakdown in a good wifi
- speech recognisiton: 1.5s
- text responce generation: 0.5s
- voice generation: 1.5s
total t(voice responce) - t(question asked): 3.5s

#### Known Issues
- skull-gpt-hotword.py gives ||PaMacCore (AUHAL)|| Error on line 2523: err='-50', msg=Unknown Error

#### TODO
- [] Change Arduino Nano to wifi controller with Mic to remove usb cord
- [] Fix the hotword detection (Error on line 2523: err='-50')
- [] Optimise SpeechRecognition library to reduce latency, like use simpler model or tune pause threshold
- [] Split ElevenLabs streaming and Arduino skull movements into two threads to syncronise jaw movements and speech.
- [] Add agency features to the skull and function calling to change ElevenLabs voice, draw spooky Dalle pictures, make prank calls with Twilio, etc.

#### Acknowledgements
Thank you Noisebridge for using some of your parts. Thank you GPT for 101 on simple driver circuits and microcontrollers.

#### Further Notes
Try adapting the hack to breathe life to other objects and ping me x.com/savakholin for any questions. Have fun.