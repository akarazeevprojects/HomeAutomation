from forex_python.converter import CurrencyRates
from weather import Weather, Unit
import requests
import datetime


departures = None
saved_date = datetime.datetime.now()
weather_forecast = None


def get_trains(date, thresholdmins=15):
    global departures
    global saved_date

    if departures is None or date.hour != saved_date.hour:
        if date.hour != saved_date.hour:
            saved_date = date

        datestr = date.strftime("%Y-%m-%d")
        URL = "https://api.rasp.yandex.net/v3.0/search/?apikey=57f7ab5c-05ca-4f02-a9af-61c71b46dbb6&format=json&from=s9600766&to=s9601830&lang=ru_RU&page=1&date={}".format(datestr)
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
            difsec = difference.seconds
            if difsec > thresholdmins * 60.:
                trains.append(difsec)

    trains = sorted(trains)

    return trains


def get_weather(date):
    global weather_forecast
    global saved_date

    if weather_forecast is None or date.hour != saved_date.hour:
        if date.hour != saved_date.hour:
            saved_date = date

        weather = Weather(unit=Unit.CELSIUS)
        location = weather.lookup_by_location('Dolgoprudny')

        weather_forecast = dict(
            temp=location.condition.temp,
            date=location.forecast[0].date,
            high=location.forecast[0].high,
            low=location.forecast[0].low,
            text=location.forecast[0].text
        )

    return weather_forecast


def get_exchange():
    c = CurrencyRates()

    res = dict(
        eur=c.get_rate('EUR', 'RUB'),
        usd=c.get_rate('USD', 'RUB')
    )

    return res


if __name__ == '__main__':
    print(get_exchange())
