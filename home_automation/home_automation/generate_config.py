from shutil import copyfile
import argparse
import json

from home_automation import system


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--replace", help="replace ~/.homebridge/config.json with generated newconfig.json", action="store_true")
    return parser


def generate_newconfig():
    with open(system.TEMPLATECONFIG_PATH, 'r') as f:
        template_config = json.load(f)

    TemperatureFile = {
        "accessory": "HttpTemperature",
        "name": "RPi Temperature",
        "url": "http://localhost:5000/temperature/cpu"
    }
    template_config['accessories'].append(TemperatureFile)

    cmdSwitch2 = {
        "platform": "cmdSwitch2",
        "switches": list()
    }

    for fullname in system.alias_mapping:
        alias = system.alias_mapping[fullname]
        struct = {
            "name": fullname,
            "on_cmd": "python3 {} -d {} -on".format(system.ADAPTER_PATH, alias),
            "off_cmd": "python3 {} -d {} -off".format(system.ADAPTER_PATH, alias),
            "state_cmd": "python3 {} -d {} -s".format(system.ADAPTER_PATH, alias)
        }
        cmdSwitch2["switches"].append(struct)
    template_config["platforms"].append(cmdSwitch2)

    with open(system.NEWCONFIG_PATH, 'w') as f:
        json.dump(template_config, f, indent=4, sort_keys=True)


def main():
    parser = build_parser()
    args = parser.parse_args()

    generate_newconfig()

    if args.replace:
        copyfile(system.NEWCONFIG_PATH, system.CONFIG_PATH)


if __name__ == '__main__':
    main()
