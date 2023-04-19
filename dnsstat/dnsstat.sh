#!/bin/bash
# das geht ins syslog
# ps aux | grep [d]nsmasq | awk '{print $2}' | xargs -r kill -USR1
# ps -eo pid,comm | awk '$2~/^dnsmasq$/ { print $1 }' | xargs -r kill -USR1

server=${1:-fb}

MQTT_ADDRESS=hassbian

read -r _ _ _ MQTT_USER _ MQTT_PASSWORD < <(grep mqtt_remote ${HOME}/.netrc);

dodig() {
    dig +short chaos txt $1 @$server|sed 's/"//g'
}

doserver() {
    server=$1
    time=$(date +%FT%T)
    csize=$(dodig cachesize.bind)
    chits=$(dodig hits.bind)
    cmiss=$(dodig misses.bind)

    echo '{"Time":"'$time'","server":"'$server'","size":'$csize',"hits":'$chits',"miss":'$cmiss'}'
}

if [ "_$server" = "_fb" -o "_$server" = "_probook" ]; then
doserver $server | mosquitto_pub -h ${MQTT_ADDRESS} -u ${MQTT_USER} -P ${MQTT_PASSWORD} -t test/dnscache/$server -q 1 -l
else
doserver $server
fi
