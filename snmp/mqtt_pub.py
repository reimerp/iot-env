#!/usr/bin/env -S -i python3

import paho.mqtt.publish as publish
import netrc
from json import dumps
from datetime import datetime

""" a simple dict wrapper for json String output, dict uses ', json "
"""
class jsondict(dict):
  def __str__(self):
    return dumps(self)

class MqttPub():

  def __init__(self):
    self.auth = self.getcred('mqtt_remote')
    self.topic = 'test/net'

  @staticmethod
  def getTime() -> str:
    return f'{datetime.now():%Y-%m-%dT%H:%M:%S}'

  @staticmethod
  def getcred(host) -> dict:
    n = netrc.netrc()
    username = n.authenticators(host)[0]
    password = n.authenticators(host)[2]
    return {'username':username, 'password':password}

  """
  2604080109 (in)
  2009012623 (out)
  0 days 10:50:52 h (online) -- (upnp mach interface up) oder -- " 11:42:56 up 20 days, 36 min"
  Fritz!Box
  """
  @staticmethod
  def build_payload():
    dev = 'eth0'
    inp = 1
    out = 2
    up = 3
    return jsondict({'Time':MqttPub.getTime(),'mrtg':{'dev':dev,'in':inp,'out':out,'up':up}})

  def do_publish(self, payload):
    # print(payload)
    publish.single(self.topic, payload=str(payload), qos=1, hostname='hassbian', client_id='cmdline_publisher', auth=self.auth)

if __name__ == '__main__':
  m = MqttPub()
  m.do_publish(m.build_payload())
