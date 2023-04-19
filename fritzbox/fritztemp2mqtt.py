#!/usr/bin/env -S -i python3

import paho.mqtt.client as mqtt
from basemqtt import MqttBase
from fritzquery import FritzQuery

class RemoteSensor(MqttBase):

    def __init__(self):
        self.getcred('mqtt_remote')
        self.fq = FritzQuery()

    def on_publish(self, client, userdata, mid):
        print(client, userdata, mid)
        pass

    def publish(self):
        val = self.data
        if self.verbose: print('#', val)
        (rc, mid) = self.mqttc.publish('test/fb/temperature', val)
        if rc != mqtt.MQTT_ERR_SUCCESS: MqttBase.eprint('Publish Error {} {}'.format(rc, mqtt.error_string(rc)))
        if rc == mqtt.MQTT_ERR_QUEUE_SIZE: self.run = 0

    def measure(self):
        self.data = self.fq.getTemp()
        self.run = 0

    #@override
    def loop(self):
        self.mqttc.loop_start()
        while self.run > 0:
            self.measure()
            self.publish()
        self.disconnect()

if __name__ == '__main__':
    sensor = RemoteSensor()
    #sensor.verbose = True
    sensor.connect_mqtt()
