#!/usr/bin/env -S -i python3
import rrdtool
from mqtt2rrd import Mqtt2Rrd
import syslog
from json import loads as jl

class RemoteMqtt2Rrd(Mqtt2Rrd):

    def addTopics(self, target = None) -> None:
        if target == None: target = self
        target.addTopic(f'tasmota/{self.name()}/tele/SENSOR')
        # target.addTopic(f'tasmota/sensor/tele/SENSOR')    # DEBUG

    def rrd_out(self, ts, data: dict) -> str:
        sensor = data['BME280']
        return f"{ts:%s}:{sensor['Temperature']}:{sensor['Humidity']}:{sensor['Pressure']}"

    def update(self, target = None, debug = False) -> None:
        error = False
        if target == None: target = self
        topic = list(target.topics.keys())[0]
        data = jl(target.topics[topic])
        ts = self.getTs(data['Time'])
        if self.checkTs(ts):
            self.warn(f'{self.name()} too old: {ts}')
            return
        #syslog.syslog(f'update {ts}')
        try:
            temp_out = self.rrd_out(ts, data)
        except KeyError as k:
            target.topics[topic] = None
            raise k
        if self.verbose:
            from time import asctime
            print(f'## {asctime()} Temp: {temp_out}')
        if debug: return
        try:
            rrdtool.update('/var/www/rrd/logs/home_stats/bme280.rrd', temp_out)
        except rrdtool.OperationalError as e:
            err=f'Processing error {e}.'
            self.warn(err)
            #syslog.syslog(syslog.LOG_ERR, err)
            error = True
        sensor = data['TSL2561']
        temp_out = f"{ts:%s}:{sensor['Illuminance']}"
        if self.verbose:
            print(f'## {asctime()} Temp: {temp_out}')
        try:
            rrdtool.update('/var/www/rrd/logs/home_stats/illuminance.rrd', temp_out)
        except rrdtool.OperationalError as e:
            err=f'Processing error {e}.'
            self.warn(err)
            syslog.syslog(syslog.LOG_ERR, err)
            error = True
        if error: raise SystemExit()
        if self.verbose: print('Update done.')

if __name__ == '__main__':
    syslog.openlog(logoption = syslog.LOG_PID, facility = syslog.LOG_USER)
    sensor = RemoteMqtt2Rrd()
    # sensor.verbose = True
    sensor.connect_mqtt()
