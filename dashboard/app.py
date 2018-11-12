"""

A small Test application to show how to use Flask-MQTT.

"""

import eventlet
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
import json

eventlet.monkey_patch()

TOPIC = 'dashboard'
QOS = 2

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '192.168.0.111'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'flask_mqtt'
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = TOPIC
app.config['MQTT_LAST_WILL_MESSAGE'] = 'bye'
app.config['MQTT_LAST_WILL_QOS'] = 2


mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    payload = json.loads(payload)

    data = dict(
        topic=TOPIC,
        payload=payload,
        time=payload['time'],
        weather=payload['weather'],
        trains=payload['trains'],
        exchange=payload['exchange'],
        qos=QOS
    )
    socketio.emit('mqtt_message', data=data)


if __name__ == '__main__':
    mqtt.subscribe(TOPIC, QOS)
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True, debug=True)
