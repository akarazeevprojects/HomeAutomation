from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Lock
import datetime
import logging

from utils import get_trains, get_weather, get_exchange

logging.getLogger('engineio').setLevel(logging.WARNING)
logging.getLogger('socketio').setLevel(logging.WARNING)

SHORT_FLOAT_STR = "{:.2f}"
ELLIPSIS = "..."

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
        if trains:
            traintime = SHORT_FLOAT_STR.format(trains[0])
        else:
            traintime = ELLIPSIS

        if len(trains) >= 2:
            traintimenext = SHORT_FLOAT_STR.format(trains[1])
        else:
            traintimenext = ELLIPSIS

        exchange = get_exchange()
        exchange['usd'] = SHORT_FLOAT_STR.format(exchange['usd'])
        exchange['eur'] = SHORT_FLOAT_STR.format(exchange['eur'])

        data = dict(
            time=nowstr,
            weather="{}, {}/{}".format(weather['text'], weather['high'], weather['low']),
            traintime=traintime,
            traintimenext=traintimenext,
            usd=exchange['usd'],
            eur=exchange['eur']
        )

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
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
