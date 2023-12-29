#!/bin/bash

[ -z $HOME ] && export HOME=/home/pi

if [ -z "$MQTT_PASS" ]; then
  MQTT_SERV=hassbian
  if [ "_$(hostname -s)" = "_hassbian" ]; then
    read -r _ _ _ MQTT_USER _ MQTT_PASS < <(grep mqtt_remote "${HOME}"/.netrc)
  else
    eval "$(~/projects/python/pykeypass.py -e MQTT mosquitto -p remote)"
  fi
fi

# fester Server, weil Server der Vereinigten Stadtwerke haben nur 0.76M
# 13.07.23: stimmt so nicht mehr.
# mehrfach accept ist egal
speedtest --accept-license --accept-gdpr -s 4087 -f json | mosquitto_pub -h ${MQTT_SERV} -u ${MQTT_USER} -P ${MQTT_PASS} -t test/speedtest -q 1 -l
