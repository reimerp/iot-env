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
#/GT-WT02 Temperature=[4-9][0-9]/d
#/GT-WT02 Temperature=1[0-9][0-9]/d
#/GT-WT02 Temperature=-/d
#/,device=GT-WT02,source=rtl433 Humidity=/d

#s/ ESP32_Temperature/ Temp_int/

##/^devices.*value/d

# topic löschen
#/^sensors,topic=Unknown/d

# measurement löschen
/^tmp,/d

# negative timestamp
#/\-[0-9]\+$/d

#s/,ifPhysAddress=0x4494fc772f42 / /

# topic migration
#s/\(,device=[^, ]\+,source=tasmota\),topic=[^, ]\+ /\1 /
#/ Id="[^", ]\+" /d

#s/^sensors,topic=\([^, ]\+\) /sensors,device=\1,source=tasmota /
#s/,source=tasmota,topic=strom /,source=tasmota /
#s/,source=tasmota_ble,topic=\(schlaf\|bad\)BT /,source=tasmota_ble /
#s/,source=rtl433,topic=inFactory-TH /,source=rtl433 /
#s/,source=tasmota,topic=warm /,source=tasmota /
#s/,source=tasmota,topic=schlaf /,source=tasmota/

s/^sensors,device=warm,id=\([0-9A-F]*\),/sensors,Id=\1,device=warm,/

/ PWM_PWM[0-9]=/d
/^dnscache,server=fb,size=0 /d
s/^dnscache,server=probook,size=0 /dnscache,server=probook,size=300 /
s/^fb_docinfo,channelID=\([0-9]\+\),frequency=\([0-9]\+\),/fb_docinfo,channelID=\1,frequency=\2.000,/
