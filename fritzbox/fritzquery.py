#!/usr/bin/env -S -i python3
#

import requests
from fritz import Fritz

class FritzQuery(Fritz):
    def __init__(self, host='fritz.box'):
      super().__init__(host)
      if self.debug: print(self.sid)

    def getData(self, name, val):
#      data = dict(
#        sid=self.sid,
#        page=page
#      )
      params={'sid':self.sid, name:val}
      resp = requests.get(url=self.fritzurl + '/query.lua' , params=params)
      # resp.headers['Content-Type'] 'text/html -> error
      if self.debug: print(vars(resp))
      return resp.json()
      #return resp.text

    def getTemp(self):
      data = self.getData('CPUTEMP', 'cpu:status/StatTemperature')
      return data['CPUTEMP'][:data['CPUTEMP'].index(',')]

# only debug
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='FritzBox Query Helper')
    parser.add_argument('-H', '--host', default='fritz.box', help='FritzBox base hostname')
    parser.add_argument('--no-debug', action='store_true', help='Debug OFF')
    args = parser.parse_args()

    fq = FritzQuery(args.host)
    fq.debug = not args.no_debug
    temp = fq.getTemp()
    print(temp)

# 240 Werte für 24h -> alle 6 Min
#0 5 10 15 20 25 30 35 40 45 50 55
#0  6  12 18 24  30   36 42 48 54
