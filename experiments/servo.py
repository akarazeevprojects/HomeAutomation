from serial import Serial
import time

ser = Serial('/dev/ttyUSB0', 115200)
s = [0]

while True:
    s = ser.readline()
    print(s)
    time.sleep(0.1)
