#!/bin/sh

C=${C:-"docker"}
# C=echo continous.sh   # works well for testing

DB=${DB:-"sensors"}
CMD="$C compose exec influxdb influx -precision=rfc3339 -database $DB"

check() {
xargs -n1 -d'\n' -o $CMD -execute <<- "C_EOF"
 SHOW RETENTION POLICIES
 SHOW CONTINUOUS QUERIES
C_EOF
}

cont_sens() {
# a cont query runs all 30 min for the 30 min interval before: so at 13:30 for 13-13:30. inserted is the time 13:00 for the interval start
# dont neet to drop them first

# TOCHECK: what happens if a values is not existing anymore, what with new ones?
xargs -n1 -d'\n' -o $CMD -execute <<- "CS_EOF"
CREATE CONTINUOUS QUERY "cq_broker_30m" ON "sensors" BEGIN SELECT mean("total") as "total", mean("value") as "value" INTO "autogen"."broker" FROM "m"."broker" GROUP BY time(30m),* END
CREATE CONTINUOUS QUERY "cq_dnscache_30m" ON "sensors" BEGIN SELECT mean("hits_total") AS "hits_total", mean("miss_total") AS "miss_total" INTO "autogen"."dnscache" FROM "m"."dnscache" GROUP BY time(30m),* END
CREATE CONTINUOUS QUERY "cq_docinfo_30m" ON "sensors" BEGIN SELECT max("corrErrors") as "corrErrors", mean("latency") as "latency", mean("mse") as "mse", max("nonCorrErrors") as "nonCorrErrors", mean("powerLevel") as "powerLevel" INTO "autogen"."fb_docinfo" from "m"."fb_docinfo" GROUP BY time(30m),* END
CREATE CONTINUOUS QUERY "cq_fb_tr069_30m" ON "sensors" BEGIN SELECT last("v_NewAutoDisconnectTime") as "v_NewAutoDisconnectTime", mean("v_NewByteReceiveRate") as "v_NewByteReceiveRate", mean("v_NewByteSendRate") as "v_NewByteSendRate", last("v_NewChannel") as "v_NewChannel", last("v_NewConnectionStatus") as "v_NewConnectionStatus", last("v_NewDescription") as "v_NewDescription", last("v_NewExternalIPAddress") as "v_NewExternalIPAddress", last("v_NewExternalIPv6Address") as "v_NewExternalIPv6Address", last("v_NewHostNumberOfEntries") as "v_NewHostNumberOfEntries", last("v_NewIdleDisconnectTime") as "v_NewIdleDisconnectTime", last("v_NewLastConnectionError") as "v_NewLastConnectionError", last("v_NewLayer1DownstreamMaxBitRate") as "v_NewLayer1DownstreamMaxBitRate", last("v_NewLayer1UpstreamMaxBitRate") as "v_NewLayer1UpstreamMaxBitRate", last("v_NewNumberOfEntries") as "v_NewNumberOfEntries", last("v_NewNumberOfNumbers") as "v_NewNumberOfNumbers", mean("v_NewPacketReceiveRate") as "v_NewPacketReceiveRate", mean("v_NewPacketSendRate") as "v_NewPacketSendRate", last("v_NewPhysicalLinkStatus") as "v_NewPhysicalLinkStatus", last("v_NewRoutedBridgedModeBoth") as "v_NewRoutedBridgedModeBoth", last("v_NewTotalAssociations") as "v_NewTotalAssociations", mean("v_NewTotalBytesReceived") as "v_NewTotalBytesReceived", mean("v_NewTotalBytesSent") as "v_NewTotalBytesSent", mean("v_NewTotalPacketsReceived") as "v_NewTotalPacketsReceived", mean("v_NewTotalPacketsSent") as "v_NewTotalPacketsSent", last("v_NewUpTime") as "v_NewUpTime", last("v_NewUpnpControlEnabled") as "v_NewUpnpControlEnabled", last("v_NewUptime") as "v_NewUptime", last("v_NewWANAccessType") as "v_NewWANAccessType", last("v_NewX_AVM_DE_TotalBytesReceived64") as "v_NewX_AVM_DE_TotalBytesReceived64", last("v_NewX_AVM_DE_TotalBytesSent64") as "v_NewX_AVM_DE_TotalBytesSent64", last("v_NewX_AVM_DE_WANAccessType") as "v_NewX_AVM_DE_WANAccessType" INTO "autogen"."fb_tr069" FROM "m"."fb_tr069"  GROUP BY time(30m),* END
CREATE CONTINUOUS QUERY "cq_ping_30m" ON "sensors" BEGIN SELECT mean("mdev") AS "mdev", max("pl") AS "pl", mean("rtt") as "rtt" INTO "autogen"."ping" FROM "m"."ping" GROUP BY time(30m),* END
CREATE CONTINUOUS QUERY "cq_snmp_1h" ON "sensors" BEGIN SELECT last("etherStatsBroadcastPkts_count") AS "etherStatsBroadcastPkts_count", last("etherStatsMulticastPkts_count") AS "etherStatsMulticastPkts_count", last("etherStatsPkts_count") AS "etherStatsPkts_count", last("ifInDiscards_total") AS "ifInDiscards_total", last("ifInErrors_total") AS "ifInErrors_total", last("ifInUcastPkts_count") AS "ifInUcastPkts_count", last("ifOutDiscards_total") AS "ifOutDiscards_total", last("ifOutErrors_total") AS "ifOutErrors_total", last("ifOutUcastPkts_count") AS "ifOutUcastPkts_count", min("ifSpeed") AS "ifSpeed" INTO "autogen"."snmp" FROM "m"."snmp" GROUP BY time(1h),* END
CREATE CONTINUOUS QUERY "cq_speedtest_60m" ON "sensors" BEGIN SELECT last("interface_externalIp") AS "interface_externalIp", mean("download_bandwidth") AS "download_bandwidth", max("download_latency_high") AS "download_latency_high", mean("download_latency_iqm") AS "download_latency_iqm", mean("download_latency_jitter") AS "download_latency_jitter", min("download_latency_low") AS "download_latency_low", max("packetLoss") AS "packetLoss", max("ping_high") AS "ping_high", max("ping_latency") AS "ping_latency", mean("ping_jitter") AS "ping_jitter", min("ping_low") AS "ping_low", last("server_id") AS "server_id", mean("upload_bandwidth") AS "upload_bandwidth", max("upload_latency_high") AS "upload_latency_high", mean("upload_latency_iqm") AS "upload_latency_iqm", mean("upload_latency_jitter") AS "upload_latency_jitter", min("upload_latency_low") AS "upload_latency_low" INTO "autogen"."speedtest" FROM "m"."speedtest" GROUP BY time(60m),* END
CREATE CONTINUOUS QUERY "cq_sensors_1h" ON "sensors" BEGIN SELECT mean("ApparentPower") as "ApparentPower", mean("Battery") as "Battery", mean("Broadband") as "Broadband", mean("Current") as "Current", mean("DewPoint") as "DewPoint", mean("ESP32_HallEffect") as "ESP32_HallEffect", mean("Factor") as "Factor", mean("Gas") as "Gas", mean("Heap") as "Heap", mean("HeapUsed") as "HeapUsed", mean("Humidity") as "Humidity", mean("IR") as "IR", mean("Illuminance") as "Illuminance", max("LinkCount") as "LinkCount", mean("LoadAvg") as "LoadAvg", last("MqttCount") as "MqttCount", mean("Objects") as "Objects", mean("PWM_PWM1") as "PWM_PWM1", mean("PWM_PWM2") as "PWM_PWM2", mean("PWM_PWM3") as "PWM_PWM3", mean("Period") as "Period", mean("Power") as "Power", mean("Power_curr") as "Power_curr", mean("Power_curr") as "Power_curr", mean("Pressure") as "Pressure", mean("RSSI") as "RSSI", mean("ReactivePower") as "ReactivePower", mean("Scheme") as "Scheme", mean("SeaPressure") as "SeaPressure", mean("Signal") as "Signal", mean("Sleep") as "Sleep", mean("Speed") as "Speed", mean("Temp_int") as "Temp_int", mean("Temperature") as "Temperature", last("Total") as "Total", last("Total_in") as "Total_in", last("UptimeSec") as "UptimeSec", mean("VL53L0X_Distance") as "VL53L0X_Distance", mean("Vcc") as "Vcc", mean("Voltage") as "Voltage" INTO "autogen"."sensors" FROM "m"."sensors" GROUP BY time(1h),* END
CREATE CONTINUOUS QUERY "cq_temperature_30m" ON "sensors" BEGIN SELECT mean("Temperature") as "Temperature" INTO "autogen"."temperature" FROM "m"."temperature" GROUP BY time(30m),* END
CS_EOF
}

cmd="${1:-check}"
$cmd



: <<'END_COMMENT'

// ALTER RETENTION POLICY "m" ON "sensors" DURATION 24h
DROP CONTINUOUS QUERY "cq_30m" ON "sensors"
SELECT * FROM "autogen"."devices" WHERE "time" < '2023-12-23T22:30:01Z' ORDER BY "time" DESC LIMIT 10
SELECT * FROM "autogen"."devices" WHERE "time" > '2023-12-23T22:30:01Z' ORDER BY "time" ASC LIMIT 10
DROP RETENTION POLICY "forever" ON "sensors"


CREATE RETENTION POLICY "m" ON "sensors" DURATION 31d REPLICATION 1 DEFAULT
# ALTER RETENTION POLICY "m" ON "sensors" DEFAULT       // if not created as default
CREATE RETENTION POLICY "forever" ON "sensors" DURATION INF REPLICATION 1

# This is for grafana to switch policies based on time select
INSERT INTO forever grafana_rp rp="m" 2678400000000000
INSERT INTO forever grafana_rp rp="autogen" 9223372036854775806

1692195416 Mi 16. Aug 16:16:56 CEST 2023
1692195416687 in ms


select * from "autogen"."devices" ORDER BY time DESC LIMIT 10

# NO ? why
delete from "autogen"."devices"

# ok
SELECT * INTO "m"."fb_docinfo" FROM "autogen"."fb_docinfo" WHERE "time" > now()-31d ' GROUP BY *

# > m

SELECT * FROM "m"."fb_docinfo" ORDER BY time ASC LIMIT 1
SELECT * FROM "autogen"."fb_docinfo" where time > now() - 31d LIMIT 3

SELECT * FROM "m"."devices" WHERE device='fb' ORDER BY time ASC LIMIT 10

SELECT * INTO m.ping FROM autogen.ping WHERE time > now() - 31d AND time < '2024-11-11T18:17:00Z' GROUP BY *

END_COMMENT
