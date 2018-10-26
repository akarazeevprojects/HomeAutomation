import RPi.GPIO as GPIO
import argparse
import pickle
import os
import sys
import logging

import system

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def check_exists(relays_path):
    if os.path.exists(relays_path) is False:
        pins = list(system.gpio_mapping.values())
        zeros = [0] * len(pins)

        # {gpio: state}.
        relays = dict(zip(pins, zeros))

        with open(relays_path, 'wb') as f:
            pickle.dump(relays, f)
    else:
        with open(relays_path, 'rb') as f:
            relays = pickle.load(f)

    return relays


def setup_pins(relays):
    for key in relays:
        GPIO.setup(key, GPIO.OUT)


def perform_action(args, relays):
    logging.info(relays)

    if args.on:
        relay = system.gpio_mapping[args.device]
        relays[system.gpio_mapping[args.device]] = 1
        GPIO.output(relay, relays[relay])
    elif args.off:
        relay = system.gpio_mapping[args.device]
        relays[system.gpio_mapping[args.device]] = 0
        GPIO.output(relay, relays[relay])
    elif args.status:
        relay = system.gpio_mapping[args.device]
        status = relays[relay]
        if status == 0:
            sys.exit(1)


def dump(relays_path, relays):
    with open(relays_path, 'wb') as f:
        pickle.dump(relays, f)


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-d", "--device", help="device id")
    parser.add_argument("-on", "--on", help="switch on device", action="store_true")
    parser.add_argument("-off", "--off", help="switch off device", action="store_true")
    parser.add_argument("-s", "--status", help="status of device", action="store_true")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    # relays_path = os.path.join(dir_path, system.RELAYS_FILE)

    # relays = check_exists(relays_path)
    relays = check_exists(system.RELAYS_PATH)
    setup_pins(relays)
    perform_action(args, relays)
    # dump(relays_path, relays)
    dump(system.RELAYS_PATH, relays)


if __name__ == '__main__':
    main()