#!/bin/bash

set -e

[ -z $HOME ] && export HOME=/home/homeassistant

HOST="$(hostname -s)"
if [ -z "$MQTT_PASS" ]; then
# re-use when already set
  MQTT_SERV=mqtt
  if [ "_$HOST" = "_hp" ]; then
    read -r _ _ _ MQTT_USER _ MQTT_PASS < <(grep mqtt_remote "${HOME}"/.netrc)
  else
    eval "$(~/projects/python/pykeypass.py -e MQTT mosquitto -p remote)"
  fi
fi

# fester Server, weil Server der Vereinigten Stadtwerke haben nur 0.76M
# 13.07.23: stimmt so nicht mehr.
# mehrfach accept ist egal
# accept licence loggt auf stdout
speedtest --accept-license --accept-gdpr -s 4087 -f json | \
  jq -cR '. as $line|try (fromjson|del(.download.bytes,.download.elapsed,.interface.internalIp,.interface.name,.interface.isVpn,.isp,.result,.server.port,.server.name,.server.location,.server.host,.server.country,.server.ip,.type,.upload.bytes,.upload.elapsed)|{"Time":.timestamp,"speedtest":.}|del(.speedtest.timestamp)) catch $line' | tail -1 | \
  mosquitto_pub -h "${MQTT_SERV}" -u "${MQTT_USER}" -P "${MQTT_PASS}" -t "test/speedtest/${HOST}" -l
