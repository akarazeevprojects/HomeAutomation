import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button_pin = 18
led_pin = 2
led_pins = [2, 3]

GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN)

while True:
    if GPIO.input(button_pin):
        GPIO.output(led_pin, True)
    else:
        GPIO.output(led_pin, True)
        time.sleep(0.3)
        GPIO.output(led_pin, False)
        time.sleep(0.3)
