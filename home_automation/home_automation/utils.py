import emoji
import json
import os
import requests

from home_automation import system


def get_publicurl():
    os.system("curl http://localhost:4040/api/tunnels > /home/pi/tunnels.json")

    with open('/home/pi/tunnels.json') as data_file:
        datajson = json.load(data_file)

    msg = "ngrok URL: "

    for i in datajson['tunnels']:
        msg = msg + i['public_url'] + '\n'

    return msg


def get_config():
    with open(system.CONFIG_PATH, 'r') as f:
        config = json.load(f)

    return config


def get_temperature():
    with open(system.TEMPERATURE_PATH, 'r') as f:
        temp = f.read()

    return temp


def get_aliases():
    aliases = list(system.gpio_mapping.keys())
    return aliases


def compose_state():
    text = list()
    for full_name in system.alias_mapping:
        device = system.alias_mapping[full_name]
        switch_command = '{}{}'.format(system.SWITCH, device)

        r = requests.get('http://localhost:5000/state/{}'.format(device))
        content = r.content.decode()
        if content == 'ON':
            state = 1
        elif content == 'OFF':
            state = 0
        else:
            raise Exception

        print(device, state)

        if state == 0:
            # Turned off.
            state = ':electric_plug:'
        else:
            # Turned on.
            if 'fan' in device:
                state = ':dash:'
            else:
                state = ':bulb:'

        to_append = '{} - {} - {}'.format(full_name, state, switch_command)
        to_append = emoji.emojize(to_append, use_aliases=True)
        text.append(to_append)

    temp = get_temperature()
    text.append('Temperature of RPi: *{}*'.format(temp))

    text = '\n'.join(text)
    return text
