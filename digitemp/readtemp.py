#!/usr/bin/env -S -i python3

#
# Written for PyUSB 1.0 (w/libusb 1.0.3)
#
# Includes functionality to retrieve string descriptors
#
# Author: follower@rancidbacon.com
#
# Version: 20091021
#

import time

import paho.mqtt.client as mqtt
from basemqtt import MqttBase

from arduino.usbdevice import ArduinoUsbDevice
from basemqtt import MqttBase
getTime = MqttBase.getUTCTime

class DigiTemp(ArduinoUsbDevice):
  DallasId = '000000C94107'

  def __init__(self):
    try:
      super().__init__(idVendor=0x16c0, idProduct=0x05df)
      # print(f'found: 0x{self.idVendor:04x}:0x{self.idProduct:04x}')

      # print("Found: 0x%04x 0x%04x  %s %s" % (theDevice.idVendor,
      #      theDevice.idProduct,
      #      theDevice.productName,
      #      theDevice.manufacturer))
    except Exception as e:
      print('No DigiUSB Device Found', e)


  def getTemp(self):
    self.write(0x20) # Trigger new loop
    time.sleep(2)  # ensure new measurement
    try:
      while True:
        line = self.read_line()
    except Exception as e:
      temp = line
      return f'{{"Time":"{getTime()}","DS18B20":{{"Id":"{self.DallasId}","Temperature":{temp}}},"TempUnit":"C"}}'


class RemoteSensor(MqttBase):

    def __init__(self):
        self.getcred('mqtt_remote')
        self.device = DigiTemp()

    def on_publish(self, client, userdata, mid):
        print(client, userdata, mid)
        pass

    def publish(self):
        val = self.data
        if self.verbose: print('#', val)
        (rc, mid) = self.mqttc.publish('test/digi/temperature', val)
        if rc != mqtt.MQTT_ERR_SUCCESS: MqttBase.eprint('Publish Error {} {}'.format(rc, mqtt.error_string(rc)))
        if rc == mqtt.MQTT_ERR_QUEUE_SIZE: self.run = 0

    def measure(self):
        self.data = self.device.getTemp()
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
  # sensor.verbose = True
  sensor.connect_mqtt()
