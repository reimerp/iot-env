#!/usr/bin/env -S -i python3
#

import re
from fritzdata import FritzData
from basemqtt import MqttBase
getTime = MqttBase.getTime

class FritzDoc(FritzData):
    def __init__(self, host='fritz.box'):
        super().__init__(host)
        self.time = getTime()
        self.QAMrex = re.compile('^(\d+)QAM$')

    def getTestData(self):
      v = '{"pid":"docInfo","hide":{"ssoSet":true,"shareUsb":true,"mobile":true,"liveTv":true},"time":[],"data":{"channelDs":{"docsis31":[{"powerLevel":"9.6","type":"4K","channel":1,"channelID":0,"frequency":"135 - 325"}],"docsis30":[{"type":"256QAM","corrErrors":4092,"mse":"-38.6","powerLevel":"12.0","channel":1,"nonCorrErrors":924,"latency":0.32,"channelID":4,"frequency":"146"},{"type":"256QAM","corrErrors":59630,"mse":"-38.6","powerLevel":"13.8","channel":2,"nonCorrErrors":1323,"latency":0.32,"channelID":2,"frequency":"130"},{"type":"256QAM","corrErrors":64558,"mse":"-38.6","powerLevel":"12.4","channel":3,"nonCorrErrors":1554,"latency":0.32,"channelID":3,"frequency":"138"},{"type":"256QAM","corrErrors":13389,"mse":"-37.4","powerLevel":"13.9","channel":4,"nonCorrErrors":1553,"latency":0.32,"channelID":1,"frequency":"114"},{"type":"256QAM","corrErrors":181,"mse":"-37.6","powerLevel":"18.7","channel":5,"nonCorrErrors":0,"latency":0.32,"channelID":5,"frequency":"602"},{"type":"256QAM","corrErrors":223,"mse":"-40.4","powerLevel":"18.8","channel":6,"nonCorrErrors":0,"latency":0.32,"channelID":6,"frequency":"618"},{"type":"256QAM","corrErrors":221,"mse":"-40.9","powerLevel":"19.4","channel":7,"nonCorrErrors":0,"latency":0.32,"channelID":7,"frequency":"626"},{"type":"256QAM","corrErrors":132,"mse":"-40.9","powerLevel":"19.3","channel":8,"nonCorrErrors":0,"latency":0.32,"channelID":8,"frequency":"642"},{"type":"256QAM","corrErrors":38,"mse":"-40.9","powerLevel":"19.0","channel":9,"nonCorrErrors":0,"latency":0.32,"channelID":9,"frequency":"650"},{"type":"256QAM","corrErrors":63,"mse":"-40.4","powerLevel":"19.1","channel":10,"nonCorrErrors":0,"latency":0.32,"channelID":10,"frequency":"658"},{"type":"256QAM","corrErrors":94,"mse":"-38.6","powerLevel":"18.9","channel":11,"nonCorrErrors":0,"latency":0.32,"channelID":11,"frequency":"666"},{"type":"256QAM","corrErrors":115,"mse":"-40.4","powerLevel":"18.9","channel":12,"nonCorrErrors":0,"latency":0.32,"channelID":12,"frequency":"674"},{"type":"256QAM","corrErrors":33,"mse":"-40.9","powerLevel":"18.8","channel":13,"nonCorrErrors":14,"latency":0.32,"channelID":13,"frequency":"682"},{"type":"256QAM","corrErrors":18,"mse":"-40.4","powerLevel":"18.9","channel":14,"nonCorrErrors":19,"latency":0.32,"channelID":14,"frequency":"690"},{"type":"64QAM","corrErrors":70,"mse":"-36.6","powerLevel":"12.9","channel":15,"nonCorrErrors":12,"latency":0.32,"channelID":15,"frequency":"698"},{"type":"64QAM","corrErrors":69,"mse":"-36.6","powerLevel":"12.9","channel":16,"nonCorrErrors":0,"latency":0.32,"channelID":16,"frequency":"706"},{"type":"64QAM","corrErrors":10,"mse":"-35.7","powerLevel":"12.0","channel":17,"nonCorrErrors":0,"latency":0.32,"channelID":17,"frequency":"714"},{"type":"64QAM","corrErrors":112,"mse":"-36.6","powerLevel":"12.8","channel":18,"nonCorrErrors":0,"latency":0.32,"channelID":18,"frequency":"722"},{"type":"64QAM","corrErrors":112,"mse":"-36.6","powerLevel":"12.6","channel":19,"nonCorrErrors":0,"latency":0.32,"channelID":19,"frequency":"730"},{"type":"64QAM","corrErrors":49,"mse":"-36.6","powerLevel":"12.3","channel":20,"nonCorrErrors":0,"latency":0.32,"channelID":20,"frequency":"738"}]},"oem":"avm","channelUs":{"docsis30":[{"powerLevel":"35.7","type":"16QAM","channel":1,"multiplex":"ATDMA","channelID":3,"frequency":"37"},{"powerLevel":"38.5","type":"32QAM","channel":2,"multiplex":"ATDMA","channelID":4,"frequency":"31"},{"powerLevel":"32.5","type":"32QAM","channel":3,"multiplex":"ATDMA","channelID":1,"frequency":"51"},{"powerLevel":"35.7","type":"16QAM","channel":4,"multiplex":"ATDMA","channelID":2,"frequency":"45"}]}},"sid":"302183fcdf95e093"}'
      import json
      return json.loads(v)

    def sortChannels(self, inl):
        # print(inl)

        maxChannel = 0
        for i in inl:
          if i['channelID'] > maxChannel: maxChannel = i['channelID']

        outl = [{}]
        for i in range(maxChannel):
          outl.append({})

        for i in inl:
          # print(i['channelID'])
          outl[i['channelID']] = i

        return outl

    def fixEntry(self, d):
        d['powerLevel'] = float(d['powerLevel'])
        #d['frequency'] = int(d['frequency'])
        if 'mse' in d:
            d['mse'] = float(d['mse']) * -1
        #m = self.QAMrex.search(d['type'])
        #if m != None:
        #    d['type'] = int(m.group(1))
        del(d['channel'])
        return d

    def typeChannels(self, data):
        for d in data: self.fixEntry(d)

    def getDocInfo(self):
        if self.debug:
            data = self.getTestData()
        else:
            data = self.getData('docInfo')

        #del(data['pid']); del(data['hide']); del(data['sid']); del(data['time']); del(data['data'])
        data = data['data']
        if 'channelDs' not in data:
            print('Wrong data')
            return []

        #self.typeChannels(data['channelDs']['docsis30'])
        #self.typeChannels(data['channelUs']['docsis30'])
        #data['chDs30'] = self.sortChannels(data['channelDs']['docsis30'])
        #del(data['channelDs'])
        #data['chUs30'] = self.sortChannels(data['channelUs']['docsis30'])
        #del(data['channelUs'])
        #del(data['oem'])

        out = []

        for d in data['channelDs']['docsis30']:
            d = self.fixEntry(d)
            d['mode'] = 'Ds'
            d['Time'] = self.time
            out.append(d)
        if 'docsis31' in data['channelDs']:
          for d in data['channelDs']['docsis31']:
            d = self.fixEntry(d)
            d['mode'] = 'Ds'
            d['Time'] = self.time
            out.append(d)
        for d in data['channelUs']['docsis30']:
            d = self.fixEntry(d)
            d['mode'] = 'Us'
            d['Time'] = self.time
            out.append(d)
        if 'docsis31' in data['channelUs']:
          for d in data['channelUs']['docsis31']:
            d = self.fixEntry(d)
            d['mode'] = 'Us'
            d['Time'] = self.time
            out.append(d)
        return out

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='FritzBox Doc Reader')
    parser.add_argument('-H', '--host', default='fritz.box', help='FritzBox hostname')
    parser.add_argument('--no-debug', action='store_true', help='Debug OFF')
    args = parser.parse_args()

    fha = FritzDoc(args.host)
    fha.debug = not args.no_debug
    data = fha.getDocInfo()
    import json
    print(json.dumps(data))
