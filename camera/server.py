from flask import Flask, send_file, request
import picamera
import time

app = Flask(__name__)
coeff = 3
resol = (720 // coeff, 480 // coeff)


def make_photo(filename):
    with picamera.PiCamera() as camera:
        camera.resolution = resol
        camera.start_preview()
        time.sleep(1)
        camera.capture(filename)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/get_image')
def get_image():
    filename = '/home/pi/image.jpeg'
    make_photo(filename)
    return send_file(filename, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
