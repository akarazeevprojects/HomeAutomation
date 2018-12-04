import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led_pins = [2, 3, 4, 17, 27, 22, 10]


def blink(led_pin, delay=0.1):
    GPIO.output(led_pin, True)
    time.sleep(delay)
    GPIO.output(led_pin, False)
    time.sleep(delay)


def from_to(pins, delay=0.3):
    for pin in pins:
        GPIO.output(pin, True)
    time.sleep(delay)
#    for pin in pins:
#        GPIO.output(pin, False)
#    time.sleep(delay)


for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)


#while True:
#    for pin in led_pins:
#        blink(pin)
while True:
    for i in range(len(led_pins)):
        from_to(led_pins[:i + 1])
    for pin in led_pins:
        GPIO.output(pin, False)
