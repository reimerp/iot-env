#!/bin/sh
D=$(dirname $0)

docker run --rm -t -v $D/:/opt/python -v ~/.netrc:/home/python/.netrc:ro tig-rtl433 python3 fritztemp2mqtt.py
docker run --rm -t -v $D/:/opt/python -v ~/.netrc:/home/python/.netrc:ro tig-rtl433 python3 fritzdoc2mqtt.py

l=$(docker run --rm -t -e "FRITZ_USERNAME=$FRITZ_USERNAME" -e "FRITZ_PASSWORD=$FRITZ_PASSWORD" -v $D/:/opt/python -v ~/.netrc:/home/python/.netrc:ro tig-rtl433 python3 checkfritz.py | jq -c .)

printf '{"Time":"%s","FritzTR069":%s}' $(date -u +%FT%TZ) "$l" | \
  mosquitto_pub -h ${MQTT_SERV} -u ${MQTT_USER} -P ${MQTT_PASS} -t fb/fb_tr069 -q 1 -s

