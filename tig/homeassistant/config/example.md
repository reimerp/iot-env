action: notify.mobile_app_sm_s921b
data:
  message: bratwurst2
  title: gelübke
---
action: media_player.volume_down
target:
  entity_id: media_player.waipu_tv_stick
--- kein mute, weil icon on screen
service: media_player.volume_mute
target:
  entity_id: media_player.lg_webos_tv_uj6309
data:
  is_volume_muted: true
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
--- Maps measurement to temperature
template:
- sensor:
  - name: ABC Temperature
    unique_id: uniqueid__abc_temperature
    unit_of_measurement: "°C"
    device_class: temperature
    state_class: measurement
    state: "{{ state_attr('climate.heater', 'current_temperature') | int(0) }}"
--- correct measurement
template:
- unique_id: sensor_adjustment_bp_0001
  # name ist "Adjusted Wohnzimmer Luftfeuchtigkeit"
  use_blueprint:
    path: value_correction.yaml
    input:
      reference_entity: sensor.thb1_wohn_2728_luftfeuchtigkeit
      offset: -5.0
      unit: "%"
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
