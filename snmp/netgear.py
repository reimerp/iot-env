#!/bin/sh
"true" '''\'
if [ -n "${VIRTUAL_ENV}" ]; then
P="${VIRTUAL_ENV}/bin"
else
P="$(dirname "$(readlink -f "$0")")"/.direnv/python-3.11.6/bin
fi
[ -d $P ] || P="/usr/bin"
exec "$P/python3" "$0" "$@"
'''

from datetime import datetime
import re
import json
from sys import exit
import os

from jsontemplate import JsonTemplates
from snmp import Snmp
from mqtt_pub import MqttPub

__port_regex = re.compile(r'\.1\s*}}')
__oid_regex = re.compile(r'{{\s*(?P<oid>[.0-9]+)\s*}}')

"""
Hinzufügen aller oids aus d zu l
"""
def add_oid(r: list, d: dict):
  for i in d.values():
    if not isinstance(i, str): continue
    m = __oid_regex.search(i)
    if m:
      r.append((str(m.group('oid')), None))
  return r

"""

"""
def build_arr(r, a):
  ports = json_tmp.get('Ports')
  r = add_oid(r, a[0])
  i = 2
  while i <= ports:
    l = a[0].copy()
    for k, v in l.items():
      l[k] = re.sub(__port_regex, '.'  + str(i) + ' }}', v)
    r = add_oid(r, l)
    a.append(l)
    i += 1
  return a

json_tmp = JsonTemplates()

result = json_tmp.load(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'netgear.json'))
if not result[0]:
  print('Error with template')
  exit()

r = []
r = add_oid(r, result[1])   # root level hinzu

build_arr(r, json_tmp.get('snmp'))

s = Snmp()
s.req(r)
repl = s.result
repl['Time'] = MqttPub.getUTCTime()

# ifOperStatus ist egal, if ist down wenn speed 0
new_dict = json_tmp.generate(repl)

m = MqttPub()
m.topic = 'metrics/snmp/netgear'
m.do_publish(json.dumps(new_dict[1]))
