FROM mertcanboz/raspberrypi3-keras:latest

RUN pip install pyrebase

WORKDIR /app
COPY . /app
EXPOSE 5000
CMD pip list | grep Keras && pip list | grep ensorflow && python3 ./server.py
