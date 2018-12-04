import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

redled_pin = 14
blueled_pin = 15

GPIO.setup(redled_pin, GPIO.OUT)
GPIO.setup(blueled_pin, GPIO.OUT)

while True:
    GPIO.output(blueled_pin, True)
    time.sleep(0.3)
    GPIO.output(blueled_pin, False)
    time.sleep(0.3)

    GPIO.output(redled_pin, True)
    time.sleep(0.3)
    GPIO.output(redled_pin, False)
    time.sleep(0.3)
