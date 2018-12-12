import RPi.GPIO as GPIO
import requests

from home_automation import system

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def setup_pins():
    pins = system.gpio_mapping.values()
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)


def turn_on(device):
    if device == "ledstrip":
        requests.get("http://192.168.0.24:81/RELAY=ON")
    elif device == "smartclock":
        requests.get("http://192.168.0.24:81/OLED=ON")
    else:
        pin = system.gpio_mapping[device]
        GPIO.output(pin, 1)


def turn_off(device):
    if device == "ledstrip":
        requests.get("http://192.168.0.24:81/RELAY=OFF")
    elif device == "smartclock":
        requests.get("http://192.168.0.24:81/OLED=OFF")
    else:
        pin = system.gpio_mapping[device]
        GPIO.output(pin, 0)
