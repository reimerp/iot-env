#!/usr/bin/env -S python3 -u
# split String and unbuffer stdout

import paho.mqtt.client as mqtt
from basemqtt import MqttBase
from time import sleep
from subprocess import Popen, PIPE
import json
from datetime import datetime, timedelta

class RemoteSensor(MqttBase):

    def __init__(self):
        self.val = None
        self.oldTS = datetime.now();
        self.getcred('mqtt_remote')
        self.models = ['inFactory-TH', 'GT-WT02']
        # alt: 433198200 434000 434087
        self.pipe = Popen(['rtl_433', '-p20', '-g42', '-f434086k', '-R91', '-R25', '-Csi', '-Fjson'], stdout=PIPE, stdin=PIPE, stderr=None)

    def on_publish(self, client, userdata, mid):
        print(client, userdata, mid)
        pass

    @staticmethod
    def format(v) -> str:
        r = v.copy()    # leave passed value untouched
        r['time'] = RemoteSensor.getTime()
        r['Vcc'] = r['battery_ok'] * 3.3
        if r['model'] == 'GT-WT02':
          # fix temp offset and non working hum
          r['temperature_C'] = r['temperature_C'] - 2.0
          r['humidity'] = 0.0
        return '{{"Time":"{time}","Temperature":{temperature_C},"Humidity":{humidity},"Vcc":{Vcc},"TempUnit":"C"}}'.format(**r)

    def publish(self):
        self.oldTS = datetime.now();
        val = RemoteSensor.format(self.val)
        retain = True
        if self.verbose: print('pub: ', val)
        (rc, mid) = self.mqttc.publish('rtl433/{}'.format(self.val['model']), val, retain=retain)
        if rc != mqtt.MQTT_ERR_SUCCESS: MqttBase.eprint(f'Publish Error {rc} {mqtt.error_string(rc)}')
        if rc == mqtt.MQTT_ERR_QUEUE_SIZE: self.run = 0

    def measure(self):
        log_ignore = True
        while self.pipe.poll() is None:
            child_output = self.pipe.stdout.readline()
            if self.verbose: print(child_output)
            j_data = json.loads(child_output)
            # id changes on each battery insertion
            if not j_data['model'] in self.models or j_data['channel'] != 1:
                print('invalid', child_output)
                continue
            del j_data['time']
            if j_data != self.val:
                if self.verbose: print('ok', j_data, self.val)
                self.val = j_data
                break;
            else:
                # burst 500 messages/s occasionally
                # nur 1x loggen
                if log_ignore:
                    if self.verbose: print('ignored same data.')
                    log_ignore = False
                # trotzdem senden wenn seit 4 Minuten gleich
                delta = abs(datetime.now() - self.oldTS)
                if delta > timedelta(minutes=4):
                    break;
        else:
            MqttBase.eprint(f'Pipe Error {self.pipe.returncode}')
            self.run = 0

    #@override
    def loop(self):
        self.mqttc.loop_start()
        while self.run > 0:
            self.measure()
            self.publish()
        self.disconnect()

def test():
    v = {'model': 'GT-WT02', 'id': 5, 'channel': 1, 'battery_ok': 1, 'temperature_C': 11.0, 'humidity': 66, 'mic': 'CRC'}
    print('vorher ', v)
    a = RemoteSensor.format(v)
    print('format ', a)
    print('nachher', v)

if __name__ == '__main__':
    #test()
    sensor = RemoteSensor()
    #sensor.verbose = True
    sensor.connect_mqtt()
