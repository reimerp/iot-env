#!/usr/bin/env -S -i python3
#

import re
from fritzdata import FritzData
from basemqtt import MqttBase
getTime = MqttBase.getUTCTime

class FritzDoc(FritzData):
    def __init__(self, host='fritz.box'):
        super().__init__(host)
        self.time = getTime()
        self.debug = False
        self.QAMrex = re.compile('^(\d+)QAM$')

# TODO: alte fb (firmware ?) lieferte frequency "650" statt "650.000" und 4K statt 4096QAM

    def getTestData(self) -> dict:
# ver 7.29      v = '{"pid":"docInfo","hide":{"ssoSet":true,"shareUsb":true,"mobile":true,"liveTv":true},"time":[],"data":{"channelDs":{"docsis31":[{"powerLevel":"9.6","type":"4K","channel":1,"channelID":0,"frequency":"135 - 325"}],"docsis30":[{"type":"256QAM","corrErrors":4092,"mse":"-38.6","powerLevel":"12.0","channel":1,"nonCorrErrors":924,"latency":0.32,"channelID":4,"frequency":"146"},{"type":"256QAM","corrErrors":59630,"mse":"-38.6","powerLevel":"13.8","channel":2,"nonCorrErrors":1323,"latency":0.32,"channelID":2,"frequency":"130"}]},"oem":"avm","channelUs":{"docsis30":[{"powerLevel":"35.7","type":"16QAM","channel":1,"multiplex":"ATDMA","channelID":3,"frequency":"37"},{"powerLevel":"38.5","type":"32QAM","channel":2,"multiplex":"ATDMA","channelID":4,"frequency":"31"},{"powerLevel":"32.5","type":"32QAM","channel":3,"multiplex":"ATDMA","channelID":1,"frequency":"51"},{"powerLevel":"35.7","type":"16QAM","channel":4,"multiplex":"ATDMA","channelID":2,"frequency":"45"}]}},"sid":"302183fcdf95e093"}'
      v = '{"pid": "docInfo", "hide": {"liveTv": true, "tvsd": true, "provServ": true, "rrd": true, "mobile": true, "dvbSet": true, "tvhd": true, "ssoSet": true, "dvbSig": true, "dvbradio": true}, "timeTillLogout": "1200", "time": [], "data": {"channelDs": {"docsis31": [{"powerLevel": "8.7", "nonCorrErrors": 78, "modulation": "4096QAM", "plc": "264", "mer": "43", "fft": "4K", "channelID": 33, "frequency": "134.975 - 324.975"}], "docsis30": [{"powerLevel": "10.2", "nonCorrErrors": 8, "modulation": "256QAM", "corrErrors": 53, "latency": 0.32, "mse": "-40.9", "channelID": 7, "frequency": "602.000"}, {"powerLevel": "10.9", "nonCorrErrors": 5, "modulation": "256QAM", "corrErrors": 85, "latency": 0.32, "mse": "-37.6", "channelID": 3, "frequency": "570.000"}]}, "oem": "avm", "readyState": "ready", "channelUs": {"docsis31": [{"powerLevel": "36.0", "modulation": "64QAM", "activesub": "640", "fft": "2K", "channelID": 9, "frequency": "29.775 - 64.775"}], "docsis30": [{"powerLevel": "43.0", "modulation": "64QAM", "multiplex": "ATDMA", "channelID": 1, "frequency": "51.000"}, {"powerLevel": "43.0", "modulation": "32QAM", "multiplex": "ATDMA", "channelID": 4, "frequency": "30.800"}, {"powerLevel": "43.0", "modulation": "32QAM", "multiplex": "ATDMA", "channelID": 3, "frequency": "37.200"}, {"powerLevel": "43.0", "modulation": "64QAM", "multiplex": "ATDMA", "channelID": 2, "frequency": "44.600"}]}}, "sid": "4c624a69569a618c"}'
      import json
      return json.loads(v)

    def sortChannels(self, inl:list) -> list:
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

    def fixEntry(self, d:dict) -> dict:
        d['powerLevel'] = float(d['powerLevel'])
        #d['frequency'] = int(d['frequency'])
        if 'mse' in d:
            d['mse'] = float(d['mse']) * -1
        if 'modulation' in d:
            d['type'] = d['modulation']
            del(d['modulation'])
        #m = self.QAMrex.search(d['type'])
        #if m != None:
        #    d['type'] = int(m.group(1))
        if 'channel' in d:
            del(d['channel'])
        return d

    def typeChannels(self, data:list):
        for d in data: self.fixEntry(d)

    def getDocArr(self) -> list:
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
            out.append(d)
        if 'docsis31' in data['channelDs']:
          for d in data['channelDs']['docsis31']:
            d = self.fixEntry(d)
            d['mode'] = 'Ds'
            out.append(d)
        for d in data['channelUs']['docsis30']:
            d = self.fixEntry(d)
            d['mode'] = 'Us'
            out.append(d)
        if 'docsis31' in data['channelUs']:
          for d in data['channelUs']['docsis31']:
            d = self.fixEntry(d)
            d['mode'] = 'Us'
            out.append(d)
        return out

    def getDocInfo(self) -> list:
       out = {}
       out['Time'] = self.time
       out['docinfo'] = self.getDocArr()
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
