from flask_cors import CORS
import picamera
import time
import pyrebase
import uuid
import glob
import numpy as np
import os
import json
from flask import Flask, send_file
from visionModel import predict
from pyrebase_utils import db, storage # If an error occurs in this line, delete it.

app = Flask(__name__)
CORS(app)

dirpathSecrets = os.getcwd() + "/firebase_secrets.json"
path = '/home/pi/backend/food-pricing-backend/data/*.jpg'
jpg = '.jpg'
imgpath = "/home/pi/backend/food-pricing-backend/"

@app.route('/')
def mainRoute():
    return 'Hello!'

@app.route('/predict', methods=['GET']) # you can delete methods=['GET'] if this line return an error
def predictRoute():
    id = str(uuid.uuid4())
    id = "image"
    #with picamera.PiCamera() as camera:
    #    camera.resolution = (1024,768)
    #    camera.start_preview()
    #    time.sleep(1)
    #    camera.capture('%s%s%s' %(imgpath,id,jpg) ) 
    prediction = predict()
    storage.child("/predictions/%s%s" %(id,jpg)).put("%s%s%s" %(imgpath, id, jpg))

    #picture_image = glob.glob(path)
    
    #os.remove("/home/pi/backend/food-pricing-backend/data/%s%s" %(id,jpg) )

    label = prediction
    data = {"id": "ssdfds", "label": label, "weight": "10", "price": "20", "iscorrect": "false"}
    db.child("/predictions").push(data)
    doc_ref = db.collection(u'predictions').document(u'alovelace')
    doc_ref.set(data)
    return prediction

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=False)


