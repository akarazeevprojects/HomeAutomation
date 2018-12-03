from flask import Flask, send_file, request
import picamera
import time
import cv2 as cv
import numpy as np

app = Flask(__name__)
coeff = 3
resol = (720 // coeff, 480 // coeff)


def make_photo(filename):
    with picamera.PiCamera() as camera:
        camera.resolution = resol
        camera.start_preview()
        time.sleep(1)
        camera.capture(filename)


def face():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
    
        face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    
        time.sleep(0.1)
        output = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(output, 'rgb')
        
        gray = cv.cvtColor(output, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            return 'Face detected'
        else:
            return 'No face detected'


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/get_image')
def get_image():
    filename = '/home/pi/image.jpeg'
    make_photo(filename)
    return send_file(filename, mimetype='image/jpeg')


@app.route('/face')
def detected_face():
    return face()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
