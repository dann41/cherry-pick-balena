FROM resin/raspberry-pi3-debian:jessie

RUN apt-get update && apt-get install -yq \
   python sense-hat raspberrypi-bootloader python-pip && \
   apt-get clean && rm -rf /var/lib/apt/lists/* && \
   pip install paho-mqtt

WORKDIR /usr/src/app

COPY . .

ENV INITSYSTEM on

CMD modprobe i2c-dev && python game-master/src/main.py
#CMD modprobe i2c-dev && python player/src/main.py
