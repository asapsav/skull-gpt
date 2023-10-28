import os
import openai
import dotenv
import serial
import time



def main():
    dotenv.load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        arduino = serial.Serial('/dev/cu.usbserial-2110', 9600)
        time.sleep(2)
    except Exception as e:
        print(f"Failed to connect to Arduino: {e}")
        return

    messages = [
        {"role": "system", "content": "You are an evil skull that is very sarcastic and tries to trick me every time."}
    ]
    
    try:
        while True:
            user_input = input("You: ")
            messages.append({"role": "user", "content": user_input})
            
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            assistant_message = completion.choices[0].message['content']
            print(f"Assistant: {assistant_message}")
            arduino.write(b'P')

            messages.append({"role": "assistant", "content": assistant_message})
            
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")

    arduino.close()

if __name__ == "__main__":
    main()
