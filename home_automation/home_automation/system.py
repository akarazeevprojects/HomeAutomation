TEMPERATURE_PATH = '/home/pi/HomeAutomation/res/temp.txt'
ADAPTER_PATH = '/home/pi/HomeAutomation/home_automation/home_automation/adapter.py'
TGTOKEN_PATH = '/home/pi/HomeAutomation/res/token.json'

NEWCONFIG_PATH = '/home/pi/HomeAutomation/home_automation/res/newconfig.json'
TEMPLATECONFIG_PATH = '/home/pi/HomeAutomation/home_automation/res/template_config.json'
CONFIG_PATH = '/home/pi/.homebridge/config.json'

SWITCH = '/switch\_'

alias_mapping = {
    'Fan': 'fan',
    'Right lamp': 'rlamp',
    'Left lamp': 'llamp',
    'Neon': 'neon'
}

gpio_mapping = {
    'neon': 15,
    'rlamp': 18,
    'llamp': 23,
    'fan': 24
}
