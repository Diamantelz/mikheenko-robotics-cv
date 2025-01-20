import serial
import time

ser = serial.Serial('/dev/cu.usbmodem1201', 115200)
file_path = "/Users/diamantelz/Downloads/draw-portrait-simple-edited.gcode"

with open(file_path, "r") as f:
    for line in f:
        line = line.strip()
        print(line)
        ser.write(line.encode() + b'\n')
        time.sleep(2)
        try:
            response = ser.readline().decode().strip()
            print(f"Ответ Arduino: {response}")
        except:
            print("Нет ответа от Arduino (таймаут)")
ser.close()