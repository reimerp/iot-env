#!/bin/sh -e

C=${C:-"docker"}

CONTAINER_ID="$(${C} ps --filter "name=influxdb" --format "{{.ID}}")"
#echo $CONTAINER_ID

# import env (may not necessary when docker-compose is used)
. ./.env

# backup is a bind mount to host
BACKUP_PATH=/backup

DB=sensors
#DB=telegraf

B_FILE="influx_$DB.export"

rm -f "/tmp/$B_FILE"	# this file can have other rights, so delete first

# this works multiple times, since output is timestamped
backup() {
  # Backing up the database
  # imports can be used to write output
  ${C} compose exec influxdb influxd backup -portable "${BACKUP_PATH}"

  # continous queries are missing: recreate on restore

#-db "${INFLUXDB_DB}"
   #${C} cp $CONTAINER_ID:/opt/data ./

#influxd backup -portable -database  /path/to/backup
# Droping the database
#influx -username $USERNAME -password $PASSWORD -execute "DROP DATABASE \"${DATABASE}\""

# Restoring the database as newdb
}

#influx
#sensors
#_internal
#telegraf

# restore geht NICHT in gleiche db
restore() {
  #SVC=$(sed -n "s/\s*container_name\s*:\s\(.*influx-*\)/\1/p" docker-compose.yml)
  #NEW="-newdb restore"      # falls allte DB noch existent
  SRC="telegraf"
  #SRC="sensors"
  for s in $SRC; do
    ${C} compose exec influxdb influxd restore -portable -db "$s" $NEW "${BACKUP_PATH}"
  done
  # cqs sind gelöscht
  #${C} exec -it $CONTAINER_ID influx -execute 'SELECT * INTO "'$SRC'"."autogen".:MEASUREMENT FROM "restore"."autogen"./.*/ GROUP BY *'
  #${C} exec -it $CONTAINER_ID influx -execute 'DROP DATABASE "restore"'
}

copy() {
  SRC="sensors"
  #${C} compose exec influxdb influx -execute 'SELECT * INTO "'$SRC'"."autogen".:MEASUREMENT FROM "restore"."autogen"./.*/ GROUP BY *'
  #selective
  # SELECT * INTO "sensors"."autogen"."speedtest" FROM "restore"."autogen"."speedtest" GROUP BY *
}

# oneline ASCII export, editable by sed
backup_inspect() {
  ${C} compose exec influxdb influx_inspect export -waldir /var/lib/influxdb/wal -datadir /var/lib/influxdb/data -database "$DB" -out "${BACKUP_PATH}/$B_FILE"
  # default: all rps are exported

  #-start 2024-01-27T08:00:00Z
  #-lponly
  #-out -
  #-retention autogen

  B_PATH="/tmp/$B_FILE"
  [ -f "$B_PATH" ] && sudo chown $(id -u) "$B_PATH"  
  #scp hp:"$B_PATH" "$B_PATH"                   # just jor test


}

#backup #backup_inspect #restore

cmd="${1:-backup}"
"$cmd"
