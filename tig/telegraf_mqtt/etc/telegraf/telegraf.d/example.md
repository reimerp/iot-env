# V1
```
[[inputs.file]]
  files = ["/tmp/input/fritz_docsis.json"]
  data_format = "json"
#  json_query = "data"
```

# V2
```
[[inputs.file]]
  files = ["tmp/input/dns.json"]
  data_format = "json_v2"
```

# root object
```
[[inputs.mqtt_consumer.json_v2.object]]
  path = "@this"
  included_keys = [ "hits", "miss" ]
  tags = [ "server", "size" ]
```
