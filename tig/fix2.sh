#!/bin/sh

set -e

export() {
  #docker compose exec influxdb influx_inspect export -datadir /var/lib/influxdb/data -waldir /var/lib/influxdb/wal -database sensors -retention autogen -lponly -out - | wc -l
  docker compose exec influxdb influx_inspect export -datadir /var/lib/influxdb/data -waldir /var/lib/influxdb/wal -database sensors -retention autogen -lponly -out /backup/influx_sensors.export
  scp hp:/tmp/influx_sensors.export .
}

exit
#./backup.sh backup      # for safety

#./backup.sh backup_inspect

#sudo chown prochnor

# Das cleanup ist nicht erforderlich
# sed -e "/^#/d" -e "/^$/d" -e "s#/d*\$#/p#" -n -e "/^s*\//p" ../fix2.sed | while IFS= read -r l; do echo $l#; sed -n -e "$l" influx_sensors.db ; done
sed -f fix2.sed -i influx_sensors.export

docker compose down telegraf_mqtt

docker compose exec influxdb influx -execute 'DROP DATABASE "sensors"'
# TODO alle continous queries muessen neu

# ohne 2> dauerts ewig
docker compose exec influxdb influx -import -path /backup/influx_sensors.db 2>/dev/null

docker compose up -d


text() {



# # warum, das macht doch python
# delete from tmp
# SELECT mean("Temperature") AS "Temperature" INTO "tmp" FROM "autogen"."devices" GROUP BY time(30m),*
# # ggf *
# SELECT * INTO "tmp" FROM "m"."dnscache" GROUP BY *
# // einfach m mitkopieren....
# SELECT * INTO "m"."tmp" FROM "m"."dnscache" GROUP BY *


# delete from "devices"   # achtung ! löscht alle rp dadrauf, aber ein delete ohne rt wird nicht supported
# SELECT * into "autogen"."devices" FROM "tmp" GROUP BY *
# delete from tmp
# // import m
}
