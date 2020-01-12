# TUTORIAL: https://codefresh.io/docker-tutorial/hello-whale-getting-started-docker-flask/

import picamera
from flask import Flask, send_file
import time
import pyrebase
import uuid
import glob

import numpy as np
import os
#import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import imagenet_utils

app = Flask(__name__)

model = load_model("model.hdf5")
path = '/home/pi/backend/food-pricing-backend/data/*.jpg'
id = str(uuid.uuid4())
jpg = '.jpg'

config = {
    'apiKey': 'AIzaSyCCL8LNWfr2Ri2wSOV8rjlbxZ4S1SWRWco',
    'authDomain': 'tum-food-app.firebaseapp.com',
    'databaseURL': 'https://tum-food-app.firebaseio.com',
    'storageBucket': 'tum-food-app.appspot.com'
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


# feature enginnering
def create_features(dataset):
     x_scratch = []
     for imagePath in dataset:
         image = load_img(imagePath, target_size=(224, 224))
         image = img_to_array(image)
         image = np.expand_dims(image, axis=0)
         image = imagenet_utils.preprocess_input(image)
         x_scratch.append(image)
         x = np.vstack(x_scratch)
     return x

@app.route('/')
def nicki():
    return 'Hello!'

@app.route('/predict')
def predict():
    # image_path = 'image.jpg'
    with picamera.PiCamera() as camera:
        camera.resolution = (1024,768)
        camera.start_preview()
        time.sleep(1)
        camera.capture('/home/pi/backend/food-pricing-backend/data/%s%s' %(id,jpg) )

        storage.child("/predictions/%s%s" %(id,jpg)).put("/home/pi/backend/food-pricing-backend/data/*.jpg")
        # img = camera.capture(image_path)        


# # loding the ml model 
    categories = ['Bread','Dairy product','Dessert','Egg','Fried food','Meat','Noodles/Pasta','Rice','Seafood', 'Soup', 'Vegetable/Fruit']
    picture_image = glob.glob(path)

    picture_features = create_features(picture_image)

    prediction = model.predict(picture_features)
    return "Predicted Class is: {}".format(categories[np.argmax(prediction)])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=False)