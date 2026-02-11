#!/bin/bash

if [ -z "$MQTT_PASS" ]; then
  MQTT_SERV=mqtt
  if [ "_$(hostname -s)" != "_probook" ]; then
    read -r _ _ _ MQTT_USER _ MQTT_PASS < <(grep mqtt_remote "${HOME}"/.netrc)
  else
    eval "$(~/projects/python/pykeypass.py -e MQTT mosquitto -p remote)"
  fi
fi

log() {
    l=$(printf '{"Time":"%s","server":"%s","error":"%s"}' $(date +%FT%T) $1 "$2")
    #echo $l
    mosquitto_pub -h ${MQTT_SERV} -u ${MQTT_USER} -P ${MQTT_PASS} -t test/monitor/inet -m "$l"
    exit
}

lping() {
    # ping -c 1 -W 3 -q $1 >/dev/null 2>&1
    ping -c 2 -W 3 -q $1 2>&1 | grep -qE "[1-9] received"
}

ldig() {
    dig +short $1 | grep -q "."
}

lnc() {
    nc -vzw5 $1 $2 2>&1 | grep -q "succeeded"
}

GW=$(ip route list default | cut -d" " -f 3)
lping $GW || log "GW/FB" "failure"

lping 8.8.8.8 || log "Gdns" "ping. (Internet failure?)"

ldig google.com || log "DNS" "resolution error."

ldig skyisnolimit.dnshome.de || log Ralf "DNS resolution."
lping skyisnolimit.dnshome.de || log Ralf "ping failure."
#lnc skyisnolimit.dnshome.de 12012 || log Ralf "service failure."

#ldig jp1970.dyndns.org || log jp1970 "DNS resolution."
#lping jp1970.dyndns.org || log jp1970 "ping failure."
#lnc jp1970.dyndns.org 12000 || log jp1970 "service failure."

echo "$(basename $0) all ok."
