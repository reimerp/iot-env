#!/usr/bin/env -S -i python3

import paho.mqtt.client as mqtt
from basemqtt import MqttBase
import json
from fritzdoc import FritzDoc

class FritzDocInfoSensor(MqttBase):

    def __init__(self):
        self.getcred('mqtt_remote')
        self.fd = FritzDoc()

    def on_publish(self, client, userdata, mid):
        print(client, userdata, mid)
        pass

    def publish(self):
        val = json.dumps(self.data)
        if self.verbose: print('#', val)
        (rc, mid) = self.mqttc.publish('fb/fb_docinfo', val)
        if rc != mqtt.MQTT_ERR_SUCCESS: MqttBase.eprint('Publish Error {} {}'.format(rc, mqtt.error_string(rc)))
        if rc == mqtt.MQTT_ERR_QUEUE_SIZE: self.run = 0

    def measure(self):
        self.data = self.fd.getDocInfo()
        self.run = 0

    #@override
    def loop(self):
        self.mqttc.loop_start()
        while self.run > 0:
            self.measure()
            self.publish()
        self.disconnect()

if __name__ == '__main__':
    sensor = FritzDocInfoSensor()
    #sensor.verbose = True
    sensor.connect_mqtt()
