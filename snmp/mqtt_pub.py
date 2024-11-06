#!/usr/bin/env -S -i python3

import paho.mqtt.publish as publish
from json import dumps
from datetime import datetime
import platform

""" a simple dict wrapper for json String output, dict uses ', json "
"""
class jsondict(dict):
  def __str__(self):
    return dumps(self)

class MqttPub():

  def __init__(self, user='mqtt_remote', topic='test/net'):
    self.auth = self.getcred(user)
    self.topic = topic

  @staticmethod
  def getTime() -> str:
    return f'{datetime.now():%Y-%m-%dT%H:%M:%S}'

  @staticmethod
  def getcred(param: str) -> dict:
    if 'probook' == platform.node():
        try:
          from pykeypass import KeePass
        except ImportError:
          from pathlib import Path
          import sys
          sys.path.insert(0, str(Path.home()) + '/projects/python')
          from pykeypass import KeePass
        if param.startswith('mqtt_'): param=param[5:]
        keepass = KeePass('mosquitto', param)
        keepass.parse()
        return {'username':keepass.username, 'password':keepass.password}
    import netrc
    n = netrc.netrc()
    username = n.authenticators(param)[0]
    password = n.authenticators(param)[2]
    return {'username':username, 'password':password}

  """
  2604080109 (in)
  2009012623 (out)
  0 days 10:50:52 h (online) -- (upnp mach interface up) oder -- " 11:42:56 up 20 days, 36 min"
  Fritz!Box
  """
  @staticmethod
  def build_payload():
    # just demonstration
    dev = 'eth0'
    inp = 1
    out = 2
    up = 3
    return jsondict({'Time':MqttPub.getTime(),'mrtg':{'dev':dev,'in':inp,'out':out,'up':up}})

  def do_publish(self, payload):
    #print(payload, self.auth)
    # qos1 ??
    publish.single(self.topic, payload=str(payload), qos=1, hostname='hassbian', client_id='cmdline_publisher', auth=self.auth)

if __name__ == '__main__':
    m = MqttPub()
    m.do_publish(m.build_payload())
