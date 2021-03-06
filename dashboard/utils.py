from forex_python.converter import CurrencyRates
# from weather import Weather, Unit
import requests
import datetime


SHORT_FLOAT_STR = "{:.2f}"
WEATHER_STR = "{}, {}/{}"
TEMP_STR = "{}/{}"
TIME_STR = "{:02d}:{:02d}"
ELLIPSIS = "..."


departures = None
saved_date = datetime.datetime.now()
weather_forecast = None


def compare_dates(date1, date2):
    res = (date1.hour == date2.hour)
    return res


def check_date(date):
    global saved_date
    equal_dates = compare_dates(date, saved_date)
    if not equal_dates:
        saved_date = date


def get_trains(date, thresholdmins=15):
    global departures

    equal_dates = compare_dates(date, saved_date)

    if departures is None or not equal_dates:
        datestr = date.strftime("%Y-%m-%d")
        print("==DATE==")
        print(date)
        URL = "https://api.rasp.yandex.net/v3.0/search/?apikey=57f7ab5c-05ca-4f02-a9af-61c71b46dbb6&format=json&from=s9600766&to=s9601830&lang=ru_RU&page=1&date={}".format(datestr)
        print(URL)

        try:
            r = requests.get(url=URL)
            data = r.json()
            segments = data['segments']
            segments = list(filter(lambda x: x['thread']['express_type'] != 'express', segments))

            departures = list()
            for i in segments:
                deptime = i['departure'][:-6]
                deptime = datetime.datetime.strptime(deptime, "%Y-%m-%dT%H:%M:%S")
                departures.append(deptime)
        except Exception as e:
            print('--Failed--')

    trains = list()

    for deptime in departures:
        difference = deptime - date
        if difference.days >= 0:
            difsec = difference.seconds
            if difsec > thresholdmins * 60.:
                trains.append(difsec)

    trains = sorted(trains)

    res = list()

    if trains:
        res.append(TIME_STR.format(int(trains[0] / 60.), trains[0] % 60))
    else:
        res.append(ELLIPSIS)

    if len(trains) >= 2:
        res.append(TIME_STR.format(int(trains[1] / 60.), trains[1] % 60))
    else:
        res.append(ELLIPSIS)

    return res


def get_weather(date):
    global weather_forecast

    equal_dates = compare_dates(date, saved_date)

    try:
        if weather_forecast is None or not equal_dates:
            # weather = Weather(unit=Unit.CELSIUS)
            # location = weather.lookup_by_location('Dolgoprudny')
            #
            # weather_forecast = dict(
            #     temp=location.condition.temp,
            #     date=location.forecast[0].date,
            #     high=location.forecast[0].high,
            #     low=location.forecast[0].low,
            #     text=location.forecast[0].text
            # )

            URL = "http://api.openweathermap.org/data/2.5/weather?q=Dolgoprudny&units=metric&APPID=4588c7b93930a8f20c63e7c7aa6e4cd8"
            r = requests.get(url=URL)
            data = r.json()
            print(data)

            weather_forecast = dict(
                temp=data['main']['temp'],
                high=data['main']['temp_max'],
                low=data['main']['temp_min'],
                text=data['weather'][0]['main']
            )

    except Exception as e:
        weather_forecast = {'text': '404', "high": "404", "low": '404'}

    weather_string = WEATHER_STR.format(weather_forecast['text'], weather_forecast['high'], weather_forecast['low'])
    temp_string = TEMP_STR.format(weather_forecast['high'], weather_forecast['low'])

    return weather_string, temp_string


def get_exchange():
    c = CurrencyRates()

    try:
        res = dict(
            eur=c.get_rate('EUR', 'RUB'),
            usd=c.get_rate('USD', 'RUB')
        )
    except Exception as e:
        res= dict(
            eur=-0.1,
            usd=-0.1
        )

    res['usd'] = SHORT_FLOAT_STR.format(res['usd'])
    res['eur'] = SHORT_FLOAT_STR.format(res['eur'])

    return res
