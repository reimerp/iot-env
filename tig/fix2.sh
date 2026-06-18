#!/bin/sh

set -e

DB=sensors
B_FILE="influx_$DB.export"
B_PATH="/tmp/$B_FILE"

#./influx-backup.sh backup      # for safety
./influx-backup.sh backup_inspect

sudo chown $(id -u) "$B_PATH"

# Das cleanup ist nicht erforderlich
# sed -e "/^#/d" -e "/^$/d" -e "s#/d*\$#/p#" -n -e "/^s*\//p" ../fix2.sed | while IFS= read -r l; do echo $l#; sed -n -e "$l" "$B_PATH" ; done

sed -f fix2.sed -i "$B_PATH"

docker compose down telegraf_mqtt

docker compose exec influxdb influx -execute 'DROP DATABASE "'"$DB"'"'
# TODO alle continous queries muessen neu

# ohne 2> dauerts ewig
docker compose exec influxdb influx -import -path "/backup/$B_FILE" 2>/dev/null

docker compose up -d

: <<'END_COMMENT'

# warum, das macht doch python
delete from tmp
SELECT mean("Temperature") AS "Temperature" INTO "tmp" FROM "autogen"."devices" GROUP BY time(30m),*
# ggf *
SELECT * INTO "tmp" FROM "m"."dnscache" GROUP BY *
// einfach m mitkopieren....
SELECT * INTO "m"."tmp" FROM "m"."dnscache" GROUP BY *


delete from "devices"   # careful: deletes all rp dadrauf, aber ein delete ohne rt wird nicht supported
SELECT * into "autogen"."devices" FROM "tmp" GROUP BY *
delete from tmp
// import m

END_COMMENT
