#!/usr/bin/env -S -i python3
from kerze import RemoteMqtt2Rrd

class StromSub(RemoteMqtt2Rrd):

    def rrd_out(self, ts, data):
        sensor = data['MT681']
        return '{:%s}:{:0.0f}'.format(ts, 1000 * sensor['Total_in'])

if __name__ == '__main__':
    sensor = StromSub()
    #sensor.verbose = True
    sensor.connect_mqtt()
