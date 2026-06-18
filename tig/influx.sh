#!/bin/sh

# C=telegraf ./influx.sh cmd "select count(*) from telegraf..temp where host='prolab'"

C=${C:-"docker"}

DB=${DB:-"sensors"}
#DB="telegraf"
#DB="_internal"
CMD="$C compose exec influxdb influx -precision=rfc3339 -database $DB"

# ? working -> move to influx-backup.sh
import() {
$C run -it \
--network="docker-telegraf-influx-grafana-stack_default" \
-v "$(pwd):/tmp/workdir" \
influxdb:1.8-alpine influx -host influxdb -database "$DB" \
-import -path=/tmp/workdir/testdata.line -precision=s

}

# interactive
ia() {
  $CMD
}

cmd() {
  $CMD -precision=rfc3339 -execute "$*"
}

dbs() {
  cmd "SHOW DATABASES" | tail -n+4
}

meas() {
  cmd "SHOW MEASUREMENTS" | tail -n+4
}

series() {
  cmd "SHOW SERIES" | tail -n+3
}

rp() {
  cmd "SHOW RETENTION POLICIES" | tail -n+3
}

cont() {
  cmd "SHOW CONTINUOUS QUERIES"
}


#--env-file env.influxdb

cmd="${1:-ia}"
[ "$#" -ne 0 ] && shift
$cmd "$*"
