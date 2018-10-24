import RPi.GPIO as GPIO
import argparse
import pickle
import os
import sys
import logging

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

alias_mapping = {
    'Fan': 'fan',
    'Right lamp': 'rlamp',
    'Left lamp': 'llamp',
    'Neon': 'neon'
}

gpio_mapping = {
    'fan': 12,
    'rlamp': 16,
    'llamp': 20,
    'neon': 21
}
relays = None

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-d", "--device", help="device id")
parser.add_argument("-t", "--on", help="switch on device",
                    action="store_true")
parser.add_argument("-f", "--off", help="switch off device",
                    action="store_true")
parser.add_argument("-s", "--status", help="status of device",
                    action="store_true")

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.CRITICAL)

dir_path = os.path.dirname(os.path.realpath(__file__))
relays_file = 'relays.pkl'
relays_path = os.path.join(dir_path, relays_file)

if os.path.exists(relays_path) is False:
    pins = list(gpio_mapping.values())
    zeros = [0] * len(pins)

    # {gpio: state}.
    relays = dict(zip(pins, zeros))

    with open(relays_path, 'wb') as f:
        pickle.dump(relays, f)
else:
    with open(relays_path, 'rb') as f:
        relays = pickle.load(f)

for key in relays:
    GPIO.setup(key, GPIO.OUT)

if args.on:
    relay = gpio_mapping[args.device]
    relays[gpio_mapping[args.device]] = 1
    GPIO.output(relay, relays[relay])
elif args.off:
    relay = gpio_mapping[args.device]
    relays[gpio_mapping[args.device]] = 0
    GPIO.output(relay, relays[relay])
elif args.status:
    relay = gpio_mapping[args.device]
    status = relays[relay]
    if status == 0:
        sys.exit(1)

logging.info(relays)

with open(relays_path, 'wb') as f:
    pickle.dump(relays, f)
