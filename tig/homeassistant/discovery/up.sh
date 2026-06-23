#!/bin/sh

MOS="mosquitto_pub -h mqtt -u $MQTT_USER -P $MQTT_PASS"

upload() {
  TOPIC=$(echo $FILE | sed -e "s#\.json\$##" -e "s#\.#\/#g")
  echo "Send $FILE to $TOPIC"
  jq -c . $FILE | tr -d '\n' | $MOS -t "$TOPIC" -r -s
}

delete() {
  TOPIC=$(echo $FILE | sed -e "s#\.json\$##" -e "s#\.#\/#g")
  echo "Delete $TOPIC"
  $MOS -t "$TOPIC" -n -r
}

#ls -1 *.json | while read FILE; do upload; done

#ls -1 homeassistant.device.mottion*.json | while read FILE; do delete; done
ls -1 homeassistant.device.mottion*.json | while read FILE; do upload; done

#FILE=homeassistant.device.doorterrasse.config.json; upload
#FILE=homeassistant.light.kerze.config.json; upload
