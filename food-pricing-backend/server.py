from flask_cors import CORS
import picamera
import time
import uuid
#import glob
import numpy as np
import os
import json
from flask import Flask, Response#, send_file
from visionModel import predict
from pyrebase_utils import storage # If an error occurs in this line, delete it.
from camera import BaseCamera

app = Flask(__name__)
CORS(app)

path = '/home/pi/backend/food-pricing-backend/data/*.jpg'
jpg = '.jpg'
imgpath = "/home/pi/backend/food-pricing-backend/"

EMULATE_HX711=False
referenceUnit = 1
if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711
def cleanAndExit():
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()       
    print("Bye!")
    sys.exit()
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()

@app.route('/')
def mainRoute():
    return 'Hello!'

@app.route('/predict', methods=['GET']) # you can delete methods=['GET'] if this line return an error
def predictRoute():
    id = str(uuid.uuid4())
    with picamera.PiCamera() as camera:
        camera.resolution = (1024,768)
        camera.start_preview()
        time.sleep(1)
        camera.capture('%s%s%s' %(imgpath,id,jpg) ) 
    prediction = predict('%s%s%s' %(imgpath,id,jpg))
    storage.child("/predictions/%s%s" %(id,jpg)).put("%s%s%s" %(imgpath, id, jpg))

    #picture_image = glob.glob(path)
    #os.remove("/home/pi/backend/food-pricing-backend/data/%s%s" %(id,jpg) )
    val = hx.get_weight(5)

    label = prediction
    data = json.dumps({"id": id, "label": label, "weight": "10", "price": "20", "iscorrect": "false", "weight":val })
    print(data)
    return data

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=False)


