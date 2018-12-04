from flask import Flask
from home_automation import system
import platform

RPI = True
if platform.system() == 'Darwin':
    RPI = False

if RPI:
    from home_automation import switcher


class Home:
    def __init__(self):
        devices = list(system.gpio_mapping.keys())
        zeros = [0] * len(devices)
        self.device_states = dict(zip(devices, zeros))

    def get_state(self, device):
        return self.device_states[device]

    def set_state(self, device, state):
        self.device_states[device] = state

        if RPI:
            if state == 1:
                switcher.turn_on(device)
            elif state == 0:
                switcher.turn_off(device)


app = Flask(__name__)
home = Home()


def fail_message_device(device):
    return "FAILED. POSSIBLE REASON: NO SUCH DEVICE '{}'".format(device)


def fail_message():
    return "FAILED"


@app.route('/')
def hello_world():
    return "HomeAutomation project"


@app.route('/state/<device>')
def get_state(device):
    global home

    try:
        state = home.get_state(device)
        if state == 0:
            return 'OFF'
        elif state == 1:
            return 'ON'
    except KeyError:
        return fail_message_device(device)
    except Exception:
        return fail_message()


@app.route('/switch/<device>')
def switch_state(device):
    global home

    try:
        state = home.get_state(device)
        if state == 0:
            # Turn ON.
            home.set_state(device, 1)
            return 'ON'
        elif state == 1:
            # Turn OFF.
            home.set_state(device, 0)
            return 'OFF'
    except KeyError:
        return fail_message_device(device)
    except Exception:
        return fail_message()


@app.route('/on/<device>')
def turn_on(device):
    global home

    try:
        home.set_state(device, 1)
        return 'ON'
    except KeyError:
        return fail_message_device(device)
    except Exception:
        return fail_message()


@app.route('/off/<device>')
def turn_off(device):
    global home

    try:
        home.set_state(device, 0)
        return 'OFF'
    except KeyError:
        return fail_message_device(device)
    except Exception:
        return fail_message()


if __name__ == '__main__':
    if RPI:
        switcher.setup_pins()
    app.run(host='0.0.0.0', port=5000)
