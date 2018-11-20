import subprocess
import emoji
import json
import os

from home_automation import system, switcher


def get_publicurl():
    os.system("curl  http://localhost:4040/api/tunnels > /home/pi/tunnels.json")

    with open('/home/pi/tunnels.json') as data_file:
        datajson = json.load(data_file)

    msg = "ngrok URL: "

    for i in datajson['tunnels']:
        msg = msg + i['public_url'] +'\n'

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
        alias = system.alias_mapping[full_name]
        switch_command = '{}{}'.format(system.SWITCH, alias)

        state = switcher.get_state(alias)
        print(alias, state)

        if state == 0:
            # Turned off.
            state = ':electric_plug:'
        else:
            # Turned on.
            if 'fan' in alias:
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


def switch(alias):
    state = switcher.get_state(alias)
    if state == 0:
        # Turned off.
        switcher.turn_on(alias)
    else:
        # Turned on.
        switcher.turn_off(alias)


def main():
    # states = get_states()
    # print(states)

    # temp = get_temperature()
    # print(temp)

    # aliases = list(switcher.gpio_mapping.keys())
    # print(aliases)

    # state = compose_state()
    # print(state)

    pass


if __name__ == '__main__':
    main()
