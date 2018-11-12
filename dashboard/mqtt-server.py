import paho.mqtt.client as mqtt
import requests
import datetime
import time
import json

departures = None
saved_date = datetime.datetime.now()

client = mqtt.Client(clean_session=True)
client.connect('192.168.0.111', 1883, 60)
client.loop_start()


def get_trains(date):
    global departures
    global saved_date

    if departures is None or date.hour != saved_date.hour:
        if date.hour != saved_date.hour:
            saved_date = date

        URL = "https://api.rasp.yandex.net/v3.0/search/?apikey=57f7ab5c-05ca-4f02-a9af-61c71b46dbb6&format=json&from=s9600766&to=s9601830&lang=ru_RU&page=1&date=2018-11-13"
        r = requests.get(url=URL)
        data = r.json()
        segments = data['segments']
        segments = list(filter(lambda x: x['thread']['express_type'] != 'express', segments))

        departures = list()
        for i in segments:
            deptime = i['departure'][:-6]
            deptime = datetime.datetime.strptime(deptime, "%Y-%m-%dT%H:%M:%S")
            departures.append(deptime)

    trains = list()
    for deptime in departures:
        difference = deptime - date
        if difference.days >= 0:
            trains.append(difference.seconds / 60.)
    trains = sorted(trains)

    return trains


print('Script is running, press Ctrl-C to quit...')
while True:
    now = datetime.datetime.now()
    nowstr = now.strftime("%H:%M:%S")

    trains = get_trains(now)

    if trains:
        traintime = trains[0]
    else:
        traintime = "..."

    payload = {
        "time": nowstr,
        "weather": "Температура: ...",
        "trains": "Электричка до Окружной: через {:.2f} минут".format(traintime),
        "exchange": "$::..., €::..."
    }
    payload = json.dumps(payload)

    print(payload)

    client.publish('dashboard', payload, qos=2)
    time.sleep(1)
