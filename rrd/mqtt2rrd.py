#!/usr/bin/env -S -i python3
from basemqtt import MqttBase
import rrdtool
from datetime import datetime
from time import asctime

class Mqtt2Rrd(MqttBase):

    # macht broker messages
    t_rcv = '$SYS/broker/messages/received'
    t_snd = '$SYS/broker/messages/sent'

    @staticmethod
    def getRRDTimeStamp(t=datetime.now()) -> str:
        #dt = t.replace(second=0, microsecond=0)
        #t.strftime('%s')
        return f'{t:%s}'

    def addTopics(self, target = None) -> None:
        if target == None: target = self
        target.addTopic(self.t_rcv)
        target.addTopic(self.t_snd)

    def __init__(self):
        super().__init__()
        self.addTopics()

    def update(self, target = None, debug = False) -> None:
        if target == None: target = self
        ts = self.getRRDTimeStamp()
        temp_out = f"{ts}:{target.topics[self.t_rcv]}:{target.topics[self.t_snd]}"
        if self.verbose: print('#### {} Msg: {}'.format(asctime(), temp_out))
        if debug: return
        try:
            #  rrdtool.update('/var/www/rrd/logs/home_stats/broker-pkg.rrd', '-t', 'in:out', temp_out) # Template nur wenn nicht wie im DS angegeben
            rrdtool.update('/var/www/rrd/logs/home_stats/broker-pkg.rrd', temp_out)
        except rrdtool.OperationalError as e:
            #self.warn(e)
            raise SystemExit(e)
        if self.verbose: print('Update done.')

    # this checks for all values, calls update and disconnects
    def check_in(self) -> None:
        self.run -= 1
        match = [item for item in iter(self.topics.values()) if item == None]
        if 0 == len(match):
            try:
                self.update()
                self.run = -1
                self.disconnect()
            except KeyError:
                pass

    def on_message(self, client, userdata, msg):
        super(Mqtt2Rrd, self).on_message(client, userdata, msg)
        # print(msg.retain)
        self.topics[msg.topic] = msg.payload

if __name__ == '__main__':
    sensor = Mqtt2Rrd()
    #sensor.verbose = True
    sensor.connect_mqtt()
