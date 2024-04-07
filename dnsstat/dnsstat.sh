#!/bin/bash -e

# das geht ins syslog
# ps aux | grep [d]nsmasq | awk '{print $2}' | xargs -r kill -USR1
# ps -eo pid,comm | awk '$2~/^dnsmasq$/ { print $1 }' | xargs -r kill -USR1

server=${1:-fb}

if [ -z "$MQTT_PASS" ]; then
  MQTT_SERV=hassbian
  if [ "_$(hostname -s)" = "_hassbian" ]; then
    read -r _ _ _ MQTT_USER _ MQTT_PASS < <(grep mqtt_remote "${HOME}"/.netrc)
  else
    eval "$(~/projects/python/pykeypass.py -e MQTT mosquitto -p remote)"
  fi
fi

dodig() {
    dig +short chaos txt "$1" @"$server" | sed 's/"//g'
}

doserver() {
    server=$1
    time=$(date +%FT%T)
    csize=$(dodig cachesize.bind)
    chits=$(dodig hits.bind)
    cmiss=$(dodig misses.bind)

    printf '{"Time":"%s","dnscache":{"server":"%s","size":%i,"hits_total":%i,"miss_total":%i}}' "$time" "$server" "$csize" "$chits" "$cmiss"
}

if [ "_$server" = "_fb" ] || [ "_$server" = "_probook" ]; then
  doserver "$server" | mosquitto_pub -h "${MQTT_SERV}" -u "${MQTT_USER}" -P "${MQTT_PASS}" -t metrics/dnscache -q 1 -l
else
  doserver "$server"
fi
