# https://github.com/influxdata/influxdb/pull/23197
/^CREATE DATABASE /d
/^CREATE RETENTION /d
/^# DDL/a \
CREATE DATABASE sensors WITH NAME autogen \
CREATE RETENTION POLICY "forever" ON "sensors" DURATION INF REPLICATION 1 \
CREATE RETENTION POLICY "m" ON "sensors" DURATION 31d REPLICATION 1
# rename
# s/^CREATE DATABASE sensors /CREATE DATABASE sensors2 /
#
#/=GT-WT02 Temperature=[4-9][0-9]/d
#/=GT-WT02 Temperature=1[0-9][0-9]/d
#/=GT-WT02 Temperature=-/d
/=GT-WT02 Humidity=/d
s/ ESP32_Temperature/ Temp_int/

##/^devices.*value/d

# topic löschen
#/^sensors,topic=Unknown/d

# measurement löschen
/^tmp,/d

# negative timestamp
/\-[0-9]\+$/d

s/,ifPhysAddress=0x4494fc772f42 / /

# topic migration
s/\(,device=[^, ]\+,source=tasmota\),topic=[^, ]\+ /\1 /
/ Id="[^", ]\+" /d

s/^sensors,topic=\([^, ]\+\) /sensors,device=\1,source=tasmota /
s/,source=tasmota,topic=strom /,source=tasmota /
s/,source=tasmota_ble,topic=\(schlaf\|bad\)BT /,source=tasmota_ble /
s/,source=rtl433,topic=inFactory-TH /,source=rtl433 /
s/,source=tasmota,topic=warm /,source=tasmota /
s/,source=tasmota,topic=schlaf /,source=tasmota/
