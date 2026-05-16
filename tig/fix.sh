#!/bin/sh

#for l in $(./influx.sh cmd "show series on telegraf where host='prolab'" | tail +3); do
for l in $(./influx.sh cmd "show series from disk where host='prolap'" | grep mapper); do
  echo "$l"

   #./influx.sh cmd "$(echo "$l" | awk -F, 'function f(s){split(s,a,"=");return "\042"a[1]"\042=\047"a[2]"\047"}{s="select count(*) from telegraf.."$1" where ";for(i=2;i<=NF;i++){s=s f($i);if(i<NF){s=s" and "}}print s}')"
   ./influx.sh cmd "$(echo "$l" | awk -F, 'function f(s){split(s,a,"=");return "\042"a[1]"\042=\047"a[2]"\047"}{s="delete from "$1" where ";for(i=2;i<=NF;i++){s=s f($i);if(i<NF){s=s" and "}}print s}')"

done
