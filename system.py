CONFIG_PATH = '/home/pi/.homebridge/config.json'
TEMPERATURE_PATH = '/home/pi/WD/home_automation/res/temp.txt'
RELAYS_PATH = '/home/pi/WD/home_automation/res/relays.pkl'

RELAYS_FILE = 'relays.pkl'

SWITCH = '/switch\_'


alias_mapping = {
    'Fan': 'fan',
    'Right lamp': 'rlamp',
    'Left lamp': 'llamp',
    'Neon': 'neon'
}

gpio_mapping = {
    'fan': 12,
    'rlamp': 16,
    'llamp': 20,
    'neon': 21
}