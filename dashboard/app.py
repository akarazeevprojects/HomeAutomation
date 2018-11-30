from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Lock
import datetime
import logging

from utils import ELLIPSIS, SHORT_FLOAT_STR, WEATHER_STR
from utils import get_trains, get_weather, get_exchange, check_date

logging.getLogger('engineio').setLevel(logging.WARNING)
logging.getLogger('socketio').setLevel(logging.WARNING)


app = Flask(__name__)
socketio = SocketIO(app, logger=False, engineio_logger=False, async_mode=None)
thread = None
thread_lock = Lock()


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(0.1)

        now = datetime.datetime.now()
        nowstr = now.strftime("%H:%M:%S")

        weather = get_weather(now)
        trains = get_trains(now, 10)
        exchange = get_exchange()

        data = dict(
            time=nowstr,
            weather=weather,
            traintime=trains[0],
            traintimenext=trains[1],
            usd=exchange['usd'],
            eur=exchange['eur']
        )

        check_date(now)
        socketio.emit('my_response', data=data, namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
