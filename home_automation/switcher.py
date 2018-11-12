import RPi.GPIO as GPIO
import argparse
import pickle
import os
import sys
import logging

from home_automation import system

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def setup_pins(relays):
    for key in relays:
        GPIO.setup(key, GPIO.OUT)


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
            relays = None
            while relays is None:
                try:
                    relays = pickle.load(f)
                except:
                    pass

    setup_pins(relays)

    return relays


def turn_on(alias):
    relays = check_exists(system.RELAYS_PATH)
    relay = system.gpio_mapping[alias]
    relays[relay] = 1
    GPIO.output(relay, relays[relay])
    dump(system.RELAYS_PATH, relays)


def turn_off(alias):
    relays = check_exists(system.RELAYS_PATH)
    relay = system.gpio_mapping[alias]
    relays[relay] = 0
    GPIO.output(relay, relays[relay])
    dump(system.RELAYS_PATH, relays)


def get_state_returncode(alias):
    relays = check_exists(system.RELAYS_PATH)
    relay = system.gpio_mapping[alias]
    status = relays[relay]
    if status == 0:
        sys.exit(1)


def get_state(alias):
    relays = check_exists(system.RELAYS_PATH)
    relay = system.gpio_mapping[alias]
    status = relays[relay]
    return status


def perform_action(args):
    relays = check_exists(system.RELAYS_PATH)
    logging.info(relays)

    if args.on:
        turn_on(args.device)
    elif args.off:
        turn_off(args.device)
    elif args.status:
        get_state_returncode(args.device)


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

    perform_action(args)


if __name__ == '__main__':
    main()
