#!/usr/bin/env -S -i python3
from kerze import RemoteMqtt2Rrd
import syslog

class Tasmota2Rrd(RemoteMqtt2Rrd):

    def rrd_out(self, ts, data):
        sensor = data['BME280']
        return '{:%s}:{}'.format(ts, sensor['Temperature'])

if __name__ == '__main__':
    syslog.openlog(logoption = syslog.LOG_PID, facility = syslog.LOG_USER)
    sensor = Tasmota2Rrd()
    sensor.connect_mqtt()
