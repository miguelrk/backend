import glob
import numpy as np
import os
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Dropout, Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from netty import EfficientNetB0 as Net
input_shape=(224, 224, 3)
model_effinet = Net(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
model = Sequential()
model.add(model_effinet)
model.add(GlobalAveragePooling2D())
model.add(Dropout(0.35))
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model_input = Input(input_shape)
model_evaluate = model(model_input)
model_output = Dense(5, activation='softmax')(model_evaluate)
evaluate_model = Model(inputs=model_input,outputs=model_output)
evaluate_model.load_weights("model")
categories = ['Jam Sandwich','Yoghurt','Banana','Lemon','Cookies']

path = '/home/pi/backend/food-pricing-backend/picture.jfif'
sample_image = os.listdir()[0] #is the bread photo, this should be connected to the taken picture

def create_features(imagePath):
    x_scratch = []
    image = load_img(imagePath, target_size=(224, 224))
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image, axis=0)  
    x_scratch.append(image)    
    x = np.vstack(x_scratch)
    return x

def predict(imagePath = path):
    picture_features = create_features(imagePath)
    prediction = evaluate_model.predict(picture_features)
    return format(categories[np.argmax(prediction)])

