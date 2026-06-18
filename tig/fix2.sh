#!/bin/sh

C=${C:-"docker"}

DB=${DB:-"sensors"}

B_FILE="influx_$DB.export"
B_PATH="/tmp/$B_FILE"

#./influx-backup.sh backup      # for safety
#./influx-backup.sh backup_inspect
# scp hp:$B_PATH $B_PATH

# Das cleanup ist nicht erforderlich
# sed -e "/^#/d" -e "/^$/d" -e "s#/d*\$#/p#" -n -e "/^s*\//p" ../fix2.sed | while IFS= read -r l; do echo $l#; sed -n -e "$l" "$B_PATH" ; done

sed -f fix2.sed -i "$B_PATH"

$C compose down telegraf_mqtt

$C compose exec influxdb influx -execute 'DROP DATABASE "'"$DB"'"'

# needs tons of more time without  2>
# This command can es to error, mainly because imports into rps are done when they are already retired
$C compose exec influxdb influx -import -path "/backup/$B_FILE" 2>/dev/null

# rebuild all continous queries
./continous.sh cont_sens

$C compose up -d

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
