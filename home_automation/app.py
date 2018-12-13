from flask import Flask, jsonify
import subprocess

from home_automation import system


app = Flask(__name__)
home = system.Home()


def fail_message_device(device):
    return "FAILED. POSSIBLE REASON: NO SUCH DEVICE '{}'".format(device)


def fail_message():
    return "FAILED"


@app.route("/")
def hello_world():
    return "HomeAutomation project"


@app.route("/temperature/cpu")
def temperature_cpu():
    p = subprocess.Popen(["vcgencmd", "measure_temp"], stdout=subprocess.PIPE)
    out, err = p.communicate()
    out = str(out)[7:-5]
    return jsonify(temperature=out)


@app.route("/state/<device>")
def get_state(device):
    global home

    try:
        state = home.get_state(device)
        if state == 0:
            return "OFF"
        elif state == 1:
            return "ON"
    except KeyError:
        return fail_message_device(device)
    except Exception:
        return fail_message()


@app.route("/states")
def get_states():
    global home

    try:
        return jsonify(home.get_states_full())
    except Exception:
        return fail_message()


@app.route("/mapping")
def get_mapping():
    global home

    try:
        return jsonify(home.name_to_fullname)
    except Exception:
        return fail_message()


@app.route("/switch/<device>")
def switch_state(device):
    global home

    try:
        state = home.get_state(device)
        if state == 0:
            # Turn ON.
            home.set_state(device, 1)
            return "ON"
        elif state == 1:
            # Turn OFF.
            home.set_state(device, 0)
            return "OFF"
    except KeyError:
        return fail_message_device(device)
    except Exception:
        return fail_message()


@app.route("/on/<device>")
def turn_on(device):
    global home

    try:
        if home.exists(device):
            home.set_state(device, 1)
            return "ON"
        else:
            raise KeyError
    except KeyError:
        return fail_message_device(device)
    except Exception:
        return fail_message()


@app.route("/off/<device>")
def turn_off(device):
    global home

    try:
        if home.exists(device):
            home.set_state(device, 0)
            return "OFF"
        else:
            raise KeyError
    except KeyError:
        return fail_message_device(device)
    except Exception:
        return fail_message()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
