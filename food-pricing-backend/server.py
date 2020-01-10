# TUTORIAL: https://codefresh.io/docker-tutorial/hello-whale-getting-started-docker-flask/

import picamera
from flask import Flask, send_file, render_template, jsonify
import time

import numpy as np
import os

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import imagenet_utils

app = Flask(__name__)

model = load_model("model.hdf5")
print("model loaded.")

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
    return render_template("index.html")

@app.route('/predict')
def predict():
    image_path = 'image.jpg'
    print("taking photo")
    with picamera.PiCamera() as camera:
        camera.resolution = (1024,768)
        #camera.start_preview()
        time.sleep(1)
        img = camera.capture(image_path)
    print("photo taken")
#       return send_file('image.jpg', mimetype='image/jpg')

# # loding the ml model 
    categories = ['Bread','Dairy product','Dessert','Egg','Fried food','Meat','Noodles/Pasta','Rice','Seafood', 'Soup', 'Vegetable/Fruit']
    picture_image = [image_path]

    picture_features = create_features(picture_image)
#    print("features created~")
    prediction = model.predict(picture_features)
    response = "{}".format(categories[np.argmax(prediction)])
    return jsonify({"prediction": response})
    #return send_file('image.jpg', mimetype='image/jpg')

@app.route('/getImage')
def getImage():
    os.rename("image.jpg", "static/image.jpg")
    return "/static/image.jpg"#send_file('image.jpg', mimetype='image/jpg')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=False)
