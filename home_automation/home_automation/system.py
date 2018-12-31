import requests
import platform
import logging

RPI = True
if platform.system() == "Darwin":
    RPI = False

if RPI:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

# Interaction.
ADAPTER_PATH = "/home/pi/HomeAutomation/home_automation/home_automation/adapter.py"

# Configs.
NEWCONFIG_PATH = "/home/pi/HomeAutomation/home_automation/res/newconfig.json"
TEMPLATECONFIG_PATH = "/home/pi/HomeAutomation/home_automation/res/template_config.json"
CONFIG_PATH = "/home/pi/.homebridge/config.json"

# Supported types of devices: `switch`, `httpswitch`.
devices = {
    "Fan": {"type": "switch", "name": "fan", "pin": 24},
    "Right lamp": {"type": "switch", "name": "rlamp", "pin": 18},
    "Left lamp": {"type": "switch", "name": "llamp", "pin": 23},
    "Neon": {"type": "switch", "name": "neon", "pin": 15},
    "LED Strip": {
        "type": "httpswitch",
        "name": "ledstrip",
        "onURL": "http://192.168.0.24:81/RELAY=ON",
        "offURL": "http://192.168.0.24:81/RELAY=OFF",
    },
    "Kitchen LED": {
        "type": "httpswitch",
        "name": "kitchenled",
        "onURL": "http://192.168.0.6/LED=ON",
        "offURL": "http://192.168.0.6/LED=OFF"
    },
    "Smart Clock": {
        "type": "httpswitch",
        "name": "smartclock",
        "onURL": "http://192.168.0.24:81/OLED=ON",
        "offURL": "http://192.168.0.24:81/OLED=OFF",
    },
}


class Home:
    def __init__(self):
        devices_names = list([x["name"] for x in devices.values()])
        # Initialize with dict of zeros.
        self.device_states = dict(zip(devices_names, [0] * len(devices_names)))
        self.name_to_fullname = dict(
            [(info["name"], fullname) for fullname, info in devices.items()]
        )
        self.fullname_to_name = dict(
            [(fullname, info["name"]) for fullname, info in devices.items()]
        )

        if RPI:
            self._setup_pins()

        # Initialize logger for data collection.
        logger = logging.getLogger('actions')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('actions.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        self.logger = logger

    def _setup_pins(self):
        pins = [x["pin"] for x in devices.values() if x["type"] == "switch"]
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

    def _turn_on(self, device):
        fullname = self.name_to_fullname[device]

        if devices[fullname]["type"] == "httpswitch":
            on_url = devices[fullname]["onURL"]
            requests.get(on_url)
        elif devices[fullname]["type"] == "switch":
            pin = devices[fullname]["pin"]
            GPIO.output(pin, 1)

        self.logger.info('{} {}'.format(device, 'ON'))

    def _turn_off(self, device):
        fullname = self.name_to_fullname[device]

        if devices[fullname]["type"] == "httpswitch":
            off_url = devices[fullname]["offURL"]
            requests.get(off_url)
        elif devices[fullname]["type"] == "switch":
            pin = devices[fullname]["pin"]
            GPIO.output(pin, 0)

        self.logger.info('{} {}'.format(device, 'OFF'))

    def exists(self, device):
        return device in self.device_states

    def get_state(self, device):
        return self.device_states[device]

    def get_states_full(self):
        res = dict()

        for name, fullname in self.name_to_fullname.items():
            res[fullname] = self.get_state(name)

        return res

    def set_state(self, device, state):
        """
        :param device: name of device (e.g. `rlamp`).
        :param state: 1 or 0.
        """
        self.device_states[device] = state

        if RPI:
            if state == 1:
                self._turn_on(device)
            elif state == 0:
                self._turn_off(device)
