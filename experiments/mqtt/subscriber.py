import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

led_pins = [2, 3, 4, 17, 27, 22, 10]

RED_PIN = 14
BLUE_PIN  = 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.output(RED_PIN, GPIO.LOW)
p = GPIO.PWM(RED_PIN, 1000)
p.start(0)

GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.output(BLUE_PIN, GPIO.LOW)


for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/leds/red")
    client.subscribe("/leds/blue")
    client.subscribe("/light")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str( msg.payload))
    if msg.topic == '/leds/red':
        if msg.payload == b'TOGGLE':
            GPIO.output(RED_PIN, not GPIO.input(RED_PIN))
    elif msg.topic == '/leds/blue':
        if msg.payload == b'TOGGLE':
          GPIO.output(BLUE_PIN, not GPIO.input(BLUE_PIN))
    elif msg.topic == '/light':
        level = round(8 * float(msg.payload) / 100)
        print(msg.payload)
        print(level)

        for pin in led_pins:
            GPIO.output(pin, False)

        for pin in led_pins[:level]:
            GPIO.output(pin, True)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)
client.loop_start()

print('Script is running, press Ctrl-C to quit...')
while True:
    time.sleep(1)
