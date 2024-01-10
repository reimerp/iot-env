from datetime import datetime
import re
import json

from jsontemplate import JsonTemplates
from snmp import Snmp
from mqtt_pub import MqttPub

__port_regex = re.compile(r'\.1\s*}}')
__oid_regex = re.compile(r'{{\s*(?P<oid>[.0-9]+)\s*}}')

def add_oid(r: list, d: dict):
  for i in d.values():
    if not isinstance(i, str): continue
    m = __oid_regex.search(i)
    if m:
      oid = m.group('oid')
      r.append((str(oid), None))

def build_arr(a):
  ports = json_tmp.get('Ports')
  add_oid(r, a[0])
  i = 2
  while i<=ports:
    l = a[0].copy()
    for k, v in l.items():
      replaced = re.sub(__port_regex, '.'  + str(i) + ' }}', v)
      l[k] = replaced
    add_oid(r, l)
    a.append(l)
    i+=1
  return a

json_tmp = JsonTemplates()
result = json_tmp.load('netgear.json')
if not result[0]:
  print("Error with template")
  # Exit here

r = []
add_oid(r, result[1])

a = json_tmp.get('snmp')

build_arr(a)

s = Snmp()
s.req(r)
repl = s.result
repl['Time'] = MqttPub.getTime()

# ifOperStatus ist egal, if ist down wenn speed 0
new_dict = json_tmp.generate(repl)

m = MqttPub()
m.topic = 'metrics/snmp/netgear'
m.do_publish(json.dumps(new_dict[1]))
