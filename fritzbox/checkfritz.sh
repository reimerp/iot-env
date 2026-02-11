#!/bin/bash


set -e

#if [ -z "$MQTT_PASS" ]; then
  MQTT_SERV=mqtt

  if [ "_$(hostname -s)" != "_probook" ]; then
    read -r _ _ _ MQTT_USER _ MQTT_PASS < <(grep mqtt_remote ${HOME}/.netrc)
    read -r _ _ _ FRITZ_USERNAME _ FRITZ_PASSWORD < <(grep fritz.monitor ${HOME}/.netrc)
    export FRITZ_USERNAME FRITZ_PASSWORD
  else
    eval "$(~/projects/python/pykeypass.py -e MQTT mosquitto -p remote)"
    eval "$(~/projects/python/pykeypass.py -e FRITZ Fritzbox -p monitor)"
    export FRITZ_USERNAME="$FRITZ_USER"
    export FRITZ_PASSWORD="$FRITZ_PASS"
    unset FRITZ_USER FRITZ_PASS
  fi
#fi

l=$(docker run --rm -it -e "FRITZ_USERNAME=$FRITZ_USERNAME" -e "FRITZ_PASSWORD=$FRITZ_PASSWORD" -v ./:/opt/python -v ~/.netrc:/home/python/.netrc:ro tig-rtl433 python3 checkfritz.py | jq -c .)

#l=$(./checkfritz.py|jq -c .)

printf '{"Time":"%s","FritzTR069":%s}' $(date -u +%FT%TZ) "$l" | \
  mosquitto_pub -h ${MQTT_SERV} -u ${MQTT_USER} -P ${MQTT_PASS} -t fb/fb_tr069 -q 1 -s
