FROM balenalib/raspberrypi3:buster
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libfreetype6-dev \
        libhdf5-dev \
        libpng-dev \
        libzmq3-dev \
        pkg-config \
        python3-dev \
        python3-numpy \
        python3-scipy \
        rsync \
        unzip

RUN  apt-get clean && \
        rm -rf /var/lib/apt/lists/*

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
        rm get-pip.py

RUN pip --no-cache-dir install \
        matplotlib ipykernel jupyter && \
        python3 -m ipykernel.kernelspec

ADD tensorflow-2.0.0-cp37-none-linux_armv7l.whl .

RUN pip install tensorflow-2.0.0-cp37-none-linux_armv7l.whl

# install keras dependencies
RUN pip install keras
RUN pip install numpy

# install pillow and its dependencies
RUN pip install Pillow

#RUN apt-get update
#RUN apt-get upgrade

RUN usermod -a -G video $(whoami)
#RUN groups $(whoami)

RUN rm tensorflow-2.0.0-cp37-none-linux_armv7l.whl

#WORKDIR /app
#COPY . /app
#EXPOSE 5000
RUN pip install flask
RUN pip install picamera
#CMD raspistill --nopreview --output image.jpg
#CMD python3 ./app.py
