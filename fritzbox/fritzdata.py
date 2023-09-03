#!/usr/bin/env -S -i python3
#

import requests
from fritz import Fritz

class FritzData(Fritz):
    def __init__(self, host):
      super().__init__(host)

    def getData(self, page):
      data = dict(
        sid=self.sid,
        page=page
      )
      resp = requests.post(url=self.fritzurl + '/data.lua' , data=data)
      return resp.json() # Check the JSON Response Content documentation below

# only debug
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='FritzBox Data Helper')
    parser.add_argument('-H', '--host', default='fritz.box', help='FritzBox hostname')
    args = parser.parse_args()

    fd = FritzData(args.host)
    data = fd.getData('docInfo')
    import json
    print(json.dumps(data))
