import subprocess
import emoji
import json

import switcher

CONFIG_PATH = '/home/pi/.homebridge/config.json'
TEMP_PATH = '/home/pi/WD/home_automation/temp.txt'
SWITCH = '/switch\_'


def get_config():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    return config


def get_states(config):
    text = list()
    for switch in config['platforms'][0]['switches']:
        state_command = switch['state_cmd']
        process = subprocess.Popen(state_command, stdout=subprocess.PIPE, shell=True)
        out, err = process.communicate()

        if process.returncode == 1:
            state = 'turned off'
        else:
            state = 'turned on'

        text.append('{} -- {}'.format(switch['name'], state))

    text = '\n'.join(text)
    return text


def get_temperature():
    with open(TEMP_PATH, 'r') as f:
        temp = f.read()

    return temp


def get_aliases():
    aliases = list(switcher.gpio_mapping.keys())
    return aliases


def compose_state():
    config = get_config()
    text = list()
    for swch in config['platforms'][0]['switches']:
        full_name = swch['name']
        alias = switcher.alias_mapping[full_name]
        switch_command = '{}{}'.format(SWITCH, alias)

        state_command = swch['state_cmd']
        process = subprocess.Popen(state_command, stdout=subprocess.PIPE, shell=True)
        out, err = process.communicate()

        if process.returncode == 1:
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


def switch(alias_to_switch):
    # print('switching {}...'.format(alias_to_switch))

    config = get_config()
    for swch in config['platforms'][0]['switches']:
        full_name = swch['name']
        alias = switcher.alias_mapping[full_name]

        if alias_to_switch == alias:
            state_command = swch['state_cmd']
            process = subprocess.Popen(state_command, stdout=subprocess.PIPE, shell=True)
            out, err = process.communicate()

            if process.returncode == 1:
                # Turned off.
                command_to_run = swch['on_cmd']
            else:
                # Turned on.
                command_to_run = swch['off_cmd']

            process = subprocess.Popen(command_to_run, stdout=subprocess.PIPE, shell=True)
            out, err = process.communicate()


def main():
    # states = get_states()
    # print(states)

    # temp = get_temperature()
    # print(temp)

    # aliases = list(switcher.gpio_mapping.keys())
    # print(aliases)

    state = compose_state()
    print(state)


if __name__ == '__main__':
    main()
