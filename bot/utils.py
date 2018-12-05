import emoji
import json
import requests

SWITCH = '/switch\_'
TGTOKEN_PATH = '/home/pi/HomeAutomation/res/token.json'


def get_publicurl():
    msg = "ngrok URL: " + json.loads(requests.get('http://localhost:4040/api/tunnels').content.decode())['tunnels'][0]['public_url'] + '\n'
    return msg


def get_temperature():
    temp = json.loads(requests.get('http://localhost:5000/temperature/cpu').content.decode())['temperature']
    return temp


def emo_state(state, device):
    if state == 0:
        # Turned off.
        res = ':electric_plug:'
    else:
        # Turned on.
        if 'fan' in device:
            res = ':dash:'
        else:
            res = ':bulb:'

    return res


def compose_state():
    text = list()

    mapping = json.loads(requests.get('http://localhost:5000/mapping').content.decode())
    states = json.loads(requests.get('http://localhost:5000/states').content.decode())

    for full_name, device in mapping.items():
        switch_command = '{}{}'.format(SWITCH, device)

        state = emo_state(states[full_name], device)

        to_append = '{} - {} - {}'.format(full_name, state, switch_command)
        to_append = emoji.emojize(to_append, use_aliases=True)
        text.append(to_append)

    temp = get_temperature()
    text.append('Temperature of RPi: *{}*'.format(temp))

    text = '\n'.join(text)
    return text
