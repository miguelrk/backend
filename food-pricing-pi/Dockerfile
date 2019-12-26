FROM mertcanboz/raspberrypi3-keras:latest

WORKDIR /app
COPY . /app
EXPOSE 5000
CMD pip list | grep Keras && pip list | grep ensorflow && python3 ./server.py
