import RPi.GPIO as GPIO
import time

LedPin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LedPin, GPIO.OUT)
GPIO.output(LedPin, GPIO.LOW)

p = GPIO.PWM(LedPin, 1000)
p.start(0)

def breath():
    while True:
        for dc in range(0, 101, 4):
            p.ChangeDutyCycle(dc)
            time.sleep(0.05)
        time.sleep(1)
        for dc in range(100, -1, -4):
            p.ChangeDutyCycle(dc)
            time.sleep(0.05)
        time.sleep(1)

def different_levels():
    while True:
        for level in [0, 20, 80, 100]:
            p.ChangeDutyCycle(level)
            time.sleep(1)

#different_levels()
breath()
