#!/bin/sh

MOS="mosquitto_pub -h mqtt -u admin -P AiyuXee4"

upload() {
  TOPIC=$(echo $FILE | sed -e "s#\.json\$##" -e "s#\.#\/#g")
  jq -c . $FILE | tr -d '\n' | $MOS -t "$TOPIC" -r -s
}

ls -1 *.json | while read FILE; do upload; done

#FILE=homeassistant.device.doorterrasse.config.json; upload
#FILE=homeassistant.light.kerze.config.json; upload
