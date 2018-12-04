import RPi.GPIO as GPIO

from home_automation import system

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def setup_pins():
    pins = system.gpio_mapping.values()
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)


def turn_on(device):
    pin = system.gpio_mapping[device]
    GPIO.output(pin, 1)


def turn_off(device):
    pin = system.gpio_mapping[device]
    GPIO.output(pin, 0)
