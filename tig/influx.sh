#!/bin/sh

C="docker"

import() {
docker run -it \
--network="docker-telegraf-influx-grafana-stack_default" \
-v "$(pwd):/tmp/workdir" \
influxdb:1.8-alpine influx -host influxdb -database sensors \
-import -path=/tmp/workdir/testdata.line -precision=s

}

CMD="$C compose exec influxdb influx -precision=rfc3339 -database sensors"

ia() {
  $CMD
}

cmd() {
  $CMD -precision=rfc3339 -execute "$*"
}

databases() {
  cmd "SHOW DATABASES" | tail -n+4
}

measurements() {
  cmd "SHOW MEASUREMENTS" | tail -n+4
}

series() {
  cmd "SHOW SERIES" | tail -n+3
}

#--env-file env.influxdb

cmd="${1:-ia}"
[ "$#" -ne 0 ] && shift
$cmd "$*"
