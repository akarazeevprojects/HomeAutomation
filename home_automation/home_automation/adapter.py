import argparse
import requests
import sys
import logging


def turn_on(device):
    requests.get('http://localhost:5000/on/{}'.format(device))


def turn_off(device):
    requests.get('http://localhost:5000/off/{}'.format(device))


def switch(device):
    requests.get('http://localhost:5000/switch/{}'.format(device))


def get_state_returncode(device):
    r = requests.get('http://localhost:5000/state/{}'.format(device))
    content = r.content.decode()

    if content == 'ON':
        state = 1
    elif content == 'OFF':
        state = 0
    else:
        raise Exception

    if state == 0:
        sys.exit(1)


def perform_action(args):
    if args.on:
        turn_on(args.device)
    elif args.off:
        turn_off(args.device)
    elif args.state:
        get_state_returncode(args.device)


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-d", "--device", help="device id")
    parser.add_argument("-on", "--on", help="switch on device", action="store_true")
    parser.add_argument("-off", "--off", help="switch off device", action="store_true")
    parser.add_argument("-s", "--state", help="state of device", action="store_true")
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
