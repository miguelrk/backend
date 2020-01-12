import pyrebase
import os

dirpathSecrets = os.getcwd() + "/firebase_secrets.json"

firebaseConfig = {
  "apiKey": "AIzaSyCCL8LNWfr2Ri2wSOV8rjlbxZ4S1SWRWco",
  "authDomain": "tum-food-app.firebaseapp.com",
  "databaseURL": "https://tum-food-app.firebaseio.com",
  #"projectId": "tum-food-app",
  "storageBucket": "tum-food-app.appspot.com",
  #"messagingSenderId": "811530983997",
  #"appId": "1:811530983997:web:12889ab162f54f3f1be854",
  #"measurementId": "G-ZTTXZQNQE8",
  "serviceAccount": dirpathSecrets
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
storage = firebase.storage()
