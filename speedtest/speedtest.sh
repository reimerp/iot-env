#!/bin/bash

MQTT_ADDRESS=hassbian

[ -z $HOME ] && export HOME=/home/pi

if [ "_$(hostname -d)" = "_hassbian" ]; then
  read -r _ _ _ MQTT_USER _ MQTT_PASS < <(grep mqtt_remote ${HOME}/.netrc)
else
  eval "$(~/projects/python/pykeypass.py -e MQTT mosquitto -p remote)"
fi

# fester Server, weil Server der Vereinigten Stadtwerke haben nur 0.76M
# 13.07.23: stimmt so nicht mehr.
# mehrfach accept ist egal
speedtest --accept-license --accept-gdpr -s 4087 -f json | mosquitto_pub -h ${MQTT_ADDRESS} -u ${MQTT_USER} -P ${MQTT_PASS} -t test/speedtest -q 1 -l
