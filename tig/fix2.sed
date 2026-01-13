# https://github.com/influxdata/influxdb/pull/23197
/^CREATE DATABASE /d
/^# DDL/a \
CREATE DATABASE sensors WITH NAME autogen \
CREATE RETENTION POLICY "forever" ON "sensors" DURATION INF REPLICATION 1 \
CREATE RETENTION POLICY "m" ON "sensors" DURATION 31d REPLICATION 1
# rename
# s/^CREATE DATABASE sensors /CREATE DATABASE sensors2 /
#
/=GT-WT02 Temperature=[4-9][0-9]/d
/=GT-WT02 Temperature=1[0-9][0-9]/d
# /=GT-WT02 Temperature=-/d
# /=GT-WT02 Humidity=/d


s/^ESP32_Temperature/Temp_int/

#/^devices.*value/d

# topic löschen
#/^sensors,topic=Unknown/d

# measurement löschen
/^tmp,/d
