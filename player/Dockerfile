FROM resin/raspberry-pi3-debian:jessie

RUN apt-get update && apt-get install -yq \
   python sense-hat raspberrypi-bootloader python-pip && \
   apt-get clean && rm -rf /var/lib/apt/lists/* && \
   pip install paho-mqtt uuid

WORKDIR /usr/src/app

COPY . .

ENV INITSYSTEM on

CMD modprobe i2c-dev && python src/main.py
