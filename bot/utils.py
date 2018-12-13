import emoji
import json
import requests

SWITCH = '/switch\_'
TGTOKEN_PATH = '/home/sams/HomeAutomation/res/token.json'

# MAIN_URL = 'http://localhost'
MAIN_URL = 'http://192.168.0.111'

def get_publicurl():
    msg = "ngrok URL: " + json.loads(requests.get('{}:4040/api/tunnels'.format(MAIN_URL)).content.decode())['tunnels'][0]['public_url'] + '\n'
    return msg


def get_temperature():
    temp = json.loads(requests.get('{}:5000/temperature/cpu'.format(MAIN_URL)).content.decode())['temperature']
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

    mapping = json.loads(requests.get('{}:5000/mapping'.format(MAIN_URL)).content.decode())
    states = json.loads(requests.get('{}:5000/states'.format(MAIN_URL)).content.decode())

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
