#!/usr/bin/env -S -i python3
import rrdtool
from mqtt2rrd import Mqtt2Rrd
import syslog
from json import loads as jl

class RemoteMqtt2Rrd(Mqtt2Rrd):

    def addTopics(self, target = None) -> None:
        if target == None: target = self
        target.addTopic(f'tasmota/{self.name()}/tele/SENSOR')

    def rrd_out(self, ts, data) -> str:
        sensor = data['ENERGY']
        return f"{ts:%s}:{sensor['Voltage']}:{sensor['Current']}:{sensor['Factor']}"

    def update(self, target = None, debug = False) -> None:
        error = False
        if target == None: target = self
        data = jl(list(target.topics.values())[0])
        ts = self.getTs(data['Time'])
        if self.checkTs(ts):
            self.warn(f'{self.name()} too old: {ts}')
            return
        #syslog.syslog(f'update {ts}')
        temp_out = self.rrd_out(ts, data)
        if self.verbose:
            from time import asctime
            print(f'## {asctime()} Temp: {temp_out}')
        if debug: return
        try:
            rrdtool.update(f'/var/www/rrd/logs/home_stats/{self.name()}.rrd', temp_out)
        except rrdtool.OperationalError as e:
            err=f'Processing error {e}.'
            self.warn(err)
            #syslog.syslog(syslog.LOG_ERR, err)
            error = True
        if error:
            raise SystemExit()
        if self.verbose: print('Update done.')

if __name__ == '__main__':
    syslog.openlog(logoption = syslog.LOG_PID, facility = syslog.LOG_USER)
    sensor = RemoteMqtt2Rrd()
    #sensor.verbose = True
    sensor.connect_mqtt()
