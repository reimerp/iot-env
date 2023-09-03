#!/bin/bash

MQTT_ADDRESS=hassbian

[ -z $HOME ] && export HOME=/home/pi
read -r _ _ _ MQTT_USER _ MQTT_PASSWORD < <(grep mqtt_remote ${HOME}/.netrc);

# fester Server, weil Server der Vereinigten Stadtwerke haben nur 0.76M
# mehrfach accept ist egal
speedtest --accept-license --accept-gdpr -s 4087 -f json | mosquitto_pub -h ${MQTT_ADDRESS} -u ${MQTT_USER} -P ${MQTT_PASSWORD} -t test/speedtest -q 1 -l
