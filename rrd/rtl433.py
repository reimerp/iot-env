#!/usr/bin/env -S -i python3
from kerze import RemoteMqtt2Rrd
import syslog

class Tasmota2Rrd(RemoteMqtt2Rrd):

    def addTopics(self, target = None):
        if target == None: target = self
        target.addTopic('{}/inFactory-TH'.format(self.name()))

    def rrd_out(self, ts, data):
        return '{:%s}:{}:{}'.format(ts, data['Temperature'], data['Humidity'])

if __name__ == '__main__':
    syslog.openlog(logoption = syslog.LOG_PID, facility = syslog.LOG_USER)
    sensor = Tasmota2Rrd()
    #sensor.verbose = True
    sensor.connect_mqtt()
