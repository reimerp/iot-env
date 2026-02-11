#!/bin/bash

. $DIR/tools

# ping a host on the local lan (default GW)
DG=$(ip route list default | cut -d" " -f 3)

# ping local lan (default GW), WLAN, DLAN, remote WLAN, provider, external, ralf
for host in $DG radio m1 warm 62.53.8.182 8.8.8.8 skyisnolimit.dnshome.de ; do
  ping_host "$host"
  send_mqtt
done
