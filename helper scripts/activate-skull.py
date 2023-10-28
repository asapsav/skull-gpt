import serial
import time

# open Arduino IDE -> Tools -> Port and put in usb port path that Arduino's is connected to
# let me know if there is an easier/automated way to do this
arduino = serial.Serial('/dev/cu.usbserial-1110', 9600)  
time.sleep(2)  # give the connection a second to settle

arduino.write(b'P')  # Send the "press" command
#arduino.write(b'P') added thia cause skull kep turing off immediatl, idk why
arduino.close()  # Close the connection
