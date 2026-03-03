#!/bin/bash

DIR=$(cd $(dirname $0) && pwd)
. $DIR/tools

host="2a02:8100:6:2::311"
ping_host "$host"
send_mqtt
