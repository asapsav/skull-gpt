### Getting Started with the Project

#### Requirements
- Python 3.x
- Arduino with Serial interface
- Install dependencies: 
  ```bash
  pip install python-dotenv openai pyserial tqdm elevenlabs
  ```
- `.env` file with `OPENAI_API_KEY` and `ELEVENLABS_API`

#### Functionality
This script connects to an Arduino via serial, simulates an "evil bro skull" chatbot for Halloween using GPT-3.5-turbo and ElevenLabs API for voice generation. It reads user inputs, processes them, and plays the voice back.

#### How to Run
1. Load the required Arduino code onto your Arduino.
2. Connect the Arduino to your computer.
3. Fill in your `.env` file with the API keys.
4. Run the script:
    ```bash
    python skull-gpt.py
    ```
    
#### Known Issues
1. Skull movements with Arduino aren't perfectly synchronized with audio stream. Threading might be required.
2. Ensure your Arduino device name is `/dev/cu.usbserial-2110` or modify the code accordingly.

#### TODO
- Implement threading for Arduino skull movements.
- Error handling for missing `.env` keys.

Run the script and interact with your evil bro skull. Have fun.