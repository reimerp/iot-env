#!/bin/sh -e
C="docker"

CONTAINER_ID="$(${C} ps --filter "name=influxdb" --format "{{.ID}}")"
#echo $CONTAINER_ID

# import env (may not necessary when docker-compose is used)
. ./.env

BACKUP_PATH=/backup

# geht beliebig oft, da die Filenamen einen Timestampnamen haben
backup() {
  # Backing up the database
  # imports can be used to write output
  ${C} compose exec influxdb influxd backup -portable "${BACKUP_PATH}"

  # die continous queries fehlen

#-db "${INFLUXDB_DB}"
   #Once your data is generated in /opt/data, copy it to the current directory on Docker host -
   #docker cp $CONTAINER_ID:/opt/data ./

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
  #docker exec -it $CONTAINER_ID influx -execute 'SELECT * INTO "'$SRC'"."autogen".:MEASUREMENT FROM "restore"."autogen"./.*/ GROUP BY *'
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
  #DB=sensors
  DB=telegraf
  ${C} compose exec influxdb influx_inspect export -waldir /var/lib/influxdb/wal -datadir /var/lib/influxdb/data -out "${BACKUP_PATH}/influx_$DB.db" -database "$DB"
# retention m und autogen werden exportiert

#-start 2024-01-27T08:00:00Z
#-out -
#-retention m

}

#backup #backup_inspect #restore

cmd="${1:-backup}"
"$cmd"
