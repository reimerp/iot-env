#!/bin/sh

# simply run: c run --rm telegraf_stats --test --test-wait 60

C=${C:-"docker"}

run_docker() {

. ./.env
. ./env.telegraf_mqtt
#set | grep INF
#echo $TELEGRAF_TAG

$C run --rm -v $(pwd)/telegraf_mqtt/etc/telegraf/:/etc/telegraf/:ro \
  -e MQTT_SERV=${MQTT_SERV} -e MQTT_USER=${MQTT_USER} -e MQTT_PASS=${MQTT_PASS} \
  -v $(pwd)/telegraf_test/tmp/input:/tmp/input -it telegraf:$TELEGRAF_TAG telegraf --test --test-wait 300
}
# geht nicht weil dyn: --env-file env.telegraf_mqtt \

conv() {
  IN="fritz.conf"
  #cat telegraf_mqtt/etc/telegraf/telegraf.d/$IN | \
  cat telegraf_test/etc/telegraf/telegraf.d/speedtest_hassbian.conf | \
  sed -e "s/\[inputs.mqtt_consumer/[inputs.file/" | \
  diff - telegraf_test/etc/telegraf/telegraf.d/speedtest.conf
  #
  # hinzu
  # [[inputs.file]]
  # files = ["tmp/input/xxx.json"]
  # topic_parsing kommentieren
}

cmd="${1:-run_docker}"
#shift
$cmd $*
