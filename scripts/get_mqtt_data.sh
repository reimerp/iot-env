#!/bin/bash

trap 'exit 0' ABRT

[ -z "$TMPDIR" ] && export TMPDIR="$HOME/tmp"

# Achtung: Das sollte geloggt werden!
[ $(pgrep -c $(basename $0|cut -c-15)) -gt 1 ] && exit 2;

export DIR=$(cd $(dirname $0) && pwd)
. $DIR/tools

DIR=$(dirname $(readlink -f $0))

debug() {
   # debug /var/tmp = persistent ~/tmp nicht
   # ~/tmp ist nicht immer gemounted
   DL=${TMPDIR}/$(basename $0).debug.log
   echo "<<< $(date -Iseconds)" >> $DL
   #ip address show dev eth0 >> $DL
   env | grep MQTT >> $DL
}
#debug

cd $DIR

ps -eo pid,etimes,comm | awk '$3~/^speedtest$/ && $2>2000 { print $1 }' | xargs -r kill

# sensoren ca 30s
# ping braucht ca 1min, daher am Schluss!
for script in $DIR/../fritzbox/fritz.sh $DIR/../snmp/netgear.sh $DIR/../dnsstat/dnsstat.sh $DIR/check_net.sh $DIR/ping.sh
do
    echo "${script} "
    ${script} || echo "${script} had an error"
done

MIN=$(date +%M)
HOUR=$(date +%H)

# halbstündlich 18:30-23:30
#if [ $HOUR -ge 18 -a $MIN -ge 30 -a $MIN -lt 35 ]; then
#  ./speedtest.sh
#fi
# 3,8,13
[ $MIN -lt 1 -o $MIN -ge 6 ] && exit 0
# hourly
#for script in iot/rrd/strom.py iot/speedtest/speedtest.sh
for script in $DIR/../speedtest/speedtest.sh
do
    echo "${script} "
    ${script} || echo "${script} had an error"
done

exit

[ $HOUR -ne 0 ] && exit 0
# daily
for script in iot/rrd/etot.py
do
    echo "${script} "
    ${script} || echo "${script} had an error"
done
