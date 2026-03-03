action: notify.mobile_app_sm_s921b
data:
  message: bratwurst2
  title: gelübke
---
mqtt:
  - name: "Temperatur Raspi"
    unique_id: "sensor.pi.temperature"
    state_topic: "test/pi/temperature"
    unit_of_measurement: "°C"
    device_class: temperature
---
tempate:
- sensor:
  - name: "Total Current Power Production"
    # solar_power_total_current_production:
    unique_id: 9fb71580-0687-434e-96c0-efc58cdc43cd
    unit_of_measurement: "W"
    state: "{{(states('sensor.tasmotastrom_mt681_power_curr')|float) + (states('sensor.tasmotastrom_mt681_power_curr')|float)}}"
--- old syntax
- id: '1592816091306'
  alias: Reimer Mqtt Test
  description: description
  trigger:
  - platform: mqtt
    topic: test/monitor/inet
  condition: []
  action:
  - service: persistent_notification.create
    data:
      title: Inet Status
      message: '# Inet Status

        Your message goes *here*
        {{ trigger.payload_json[''server''] }}

        '
      notification_id: inet_state_notification
... ok
action: media_player.volume_set
data:
  volume_level: 1
target:
  entity_id: media_player.waipu_tv_stick
