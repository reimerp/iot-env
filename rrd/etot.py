#!/usr/bin/env -S -i python3
from strom import StromSub

class StromTotalSub(StromSub):

   def addTopics(self, target = None):
        if target == None: target = self
        target.addTopic('tasmota/strom/tele/SENSOR')

if __name__ == '__main__':
    sensor = StromTotalSub()
    # sensor.verbose = True
    sensor.connect_mqtt()
