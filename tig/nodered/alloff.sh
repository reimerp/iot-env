#!/bin/bash

MQTT_ADDRESS=mqtt
# wont work in docker
read -r _ _ _ MQTT_USER _ MQTT_PASSWORD < <(grep mqtt_remote ~//.netrc);

exec >> /tmp/alloff.log ; exec 2>&1

echo $*

# TODO: GRUPPE ist Parameter 2, macht aber keinen Sinn: TV, Radio ist immer Wohn

mosquitto_pub -h ${MQTT_ADDRESS} -u ${MQTT_USER} -P ${MQTT_PASSWORD} -t groups/wohnzimmer/cmnd/Power -m OFF

mosquitto_pub -h ${MQTT_ADDRESS} -u ${MQTT_USER} -P ${MQTT_PASSWORD} -t tasmota/zigbee/cmnd/ZbSend -m '{"Device":"Tripod","Send":{"Power":"OFF"}}'

h=formuler1; ping -c 1 -W 1 -q $h >/dev/null 2>&1 && curl --silent "http://$h/web/powerstate?newstate=1"

h=radio; ping -c 1 -W 1 -q $h >/dev/null 2>&1 && curl --silent "http://$h/fsapi/SET/netremote.sys.power?pin=1234&value=0" >/dev/null

h=lg; ping -c 1 -W 1 -q $h >/dev/null 2>&1 && /home/pi/LGWebOSRemote/lgtv off

echo All Off
