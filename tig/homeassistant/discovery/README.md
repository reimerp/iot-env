# Read
`mos_sub -W 2 -v -t homeassistant/#`

# Delete
`mos_pub -t homeassistant/switch/kerze/config -r -n`

# ...

device.name -> name

o: origin

- discovery von energiemessdosen ist wg der vielzahl an sensoren nervig
  -> trotzdem POC versuchen
- audiscover von lights ist viel einfacher als via template



  "brightness": true,

delete: mos_pub -t homeassistant/device/atc/config -n -r

entity_ids:
dev.name": "Bad ATC", sensor.name "Temperatur -> "bad_atc_temperatur"


# zigbee
- Topic tasmota/zigbee/tele/SENSOR

on contact:
{"ZbReceived":{"Terrasse":{"Device":"0xA8DA","Name":"Terrasse","Contact":1,"Endpoint":1,"LinkQuality":3}}}
from time to time to time:
{"ZbReceived":{"Terrasse":{"Device":"0xA8DA","Name":"Terrasse","BatteryVoltage":3.01,"BatteryPercentage":100,"AqaraTemperature":33,"Contact":1,"Endpoint":1,"LinkQuality":8}}}

{"ZbReceived":{"Tripod":{"Device":"0xA5D7","Name":"Tripod","Power":1,"Endpoint":1,"LinkQuality":0}}} # bei an
"Dimmer":254 # nur periodisch

{"ZbReceived":{"Motion":{"Device":"0x785F","Name":"Motion","BatteryVoltage":2.99,"BatteryPercentage":92,"AqaraTemperature":34,"Xiaomi_64":0,"Endpoint":1,"LinkQuality":0}}}
"Illuminance":6,"Occupancy":1, # bei Bewegung

{"ZbReceived":{"Terrasse":{"Device":"0xA8DA","Name":"Terrasse","BatteryVoltage":3.01,"BatteryPercentage":100,"AqaraTemperature":31,"Contact":1,"Endpoint":1,"LinkQuality":16}}}


{"ZbReceived":{"TradMotion":{"Device":"0x8E42","Name":"TradMotion","Power":1,"PowerOnlyWhenOn":0,"PowerOnTime":180,"PowerOffWait":0,"Endpoint":1,"LinkQuality":8}}}


LinkQuality:0-16 ?

# TODO
- abbreveation not working (nicht: door, aber bei Kerze)
- kerze ist ein Switch kein Light
