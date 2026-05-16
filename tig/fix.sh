#!/bin/sh

# deprecated
# if timestamps are already aggregated, than delete by timestamp finds MORE hits

# us liefer ns und ns liefert gerundet
URL="http://influxdb:8086/query?db=sensors&epoch=ns"
OUT="$TMPDIR/delete_timestamps.txt"

s1() {
 MM="speedtest"
 TAG="interface_macAddr='00:00:00:00:00:00'"
}

s2() {
 MM="sensors"
 TAG="\"device\"='GT-WT02'"
 COND="\"Id\" = '0008028D9D94'"
}

s3() {
 MM="sensors"
 TAG="\"device\"='GT-WT02' and \"source\"='rtl433'"
 COND="\"Humidity\" = 0"
}

s4() {
 MM="dnscache"
 COND="\"size\" = '0' and \"server\" = 'probook' and \"hits_total\" = 0"
}

s5() {
 MM="sensors"
 TAG="\"device\"='ATCe4edc2' and \"source\"='tasmota_ble'"
 COND="\"DewPoint\" > 0"
}

s3

#SELECT * FROM ${MM} where time < '2019-12-31T23:59:59Z'
S="select * from \"autogen\".\"${MM}\" where $COND"
[ -n "$TAG" ] && S="$S and $TAG"
# and MT681_Total_in=0 AND MT681_Meter_number=''"
# and Temperature>28.5"

query() {
# perl is a fix for the max integer in jq (Ints -> "Strings")
#|\perl -pe 's/("(?:\.|[^"])*")|-?\d+(?:.\d+)?(?:[eE][-+]?\d+)?/$1||qq("$&")/ge' #|
#SELECT * FROM ${MM} WHERE topic='Bad'
curl --silent --get "$URL" --data-urlencode "q=${S}" | \
  jq -r "(.results[0].series[0].values[][0])" > $OUT
}

delete() {
for t in $(cat $OUT); do
  echo $t;
  S="DELETE FROM ${MM} WHERE \"time\"=$t"
  [ -n "$TAG" ] && S="$S and $TAG"
  curl --silent --get "$URL" \
    --data-urlencode "q=${S}"
done
}

query
HITS=$(wc -l $OUT | cut -d" " -f 1)
echo "hits: $HITS"
if [ $HITS -gt 500 ]; then
  echo "ERROR Too many hits"
  exit 1
fi
delete
