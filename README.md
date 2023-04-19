# My IOT Architecture

I used TIG stack (Telegraf / Grafana / InfluxDB) for mosts of my measurements visualisations.

Starting with a couple of visualisations for some tasmota based sensors (temperature, humidity, ...)
all decoupled by a mosquitto mqtt server running on a raspberry pi 2 (pi 1 was soon replaced, because of too less CPU / Memory)

The architecture grew over the past years, while I added more and more components:
- node-red (pi) for automation task
- homeassistant (pi) visualisisation, automation

And finally the TIG stack, all based on a docker-compose setup, running on my laptop due to memory requirements.
Tons of sensors/actors were also added:
- a couple of shelly 1 plus devices, for controlling fans (behind switches) externally triggered by humidity sensors / time based
- a shelly 1 corridor lights controller (with auto power off inside shelly) and externally triggered by motion detection (via mqtt -> node-red)
- for sure all shelly devices are tasmota based
- some battery powered bluetooth temp/humidity sensors (Xiaomi Mijia) all read by shelly 1 plus (esp32 tasmota) devices
- some zigbee base sensors (motion detection, door switches, tradfri switches) and actors (tradfri lamps) -- the gateway is tasmota based
- some 433Mhz sensors (outdoor temperature and humidity) - gateway is a sdr dongle and a python script which converts to mqtt.
- some 433Mhz sockets controlled by tasmota gw 1)
- a IR gateway (send and receive), tasmota based, to control all IR controlled devices which cannot be controlled over network
- for sure a couple of relais / power outlets (tasmota based) to control lights / other devices
- a IR sensor, adapter and tasmota based exp8266 to get data from electricity meter
- some media devices (sat receiver, tv set, radio) controlled by vendor specific interfaces
- some fun devices, eg led tv backlight, ws2812 led strips for fireplace simulation (tasmota based)
- some sensors which are for free (pi temperature, shelly 1+ temperatures) are added for fun
- fritzbox interface stats / line errors and state / temperature
- some stats for dnsmasq caches for fun
- some other data, eg output ok ookla speedtest cli run every hour

1) unfortunately the sensors were not detected by the GW, so I had to use rtl_433(pi) and a dvb-t stick(pi) for receiving and decoding.

I will add parts of the architecture (configuration and scripts) on demand or when I find time to do so. Same for detailed HW desription / architecture.

I will start with

1. fritzbox

I used a 6490 which was replaced by a 6660 this year, both are cable (docsis) devices. Since I had a lot of trouble with the line state and the bandwith with my former provider, I deceided to long term monitor some of the states you find in the GUI onf the FB.
A couple of python scripts run by systemd.timers on the pi to query values by the web interface (lua scripts on the fb). There was an article in the famous computer magazine c't this year about this, but I've had this running for years now, even on a DSL device 3 years ago.

The scripts in details:
- the login and sessionID stuff required by FB web interface (fritz.py)
- the query lua script which is capable of getting cpu temperature (fritzquery.py)
- fritzdata.py to query the data interface
- fritzdoc.py tha gets docsis info from the data interface and convert the json
- fritzdoc2mqtt.py which is one main component for using other objects an publish the docsis json on an mqtt topic
- basemqtt.py which defines a basic class responsible for mqtt connect, getting credentials and some utility functions like timestamp converting
The secrets for the fritzbox GUI and to mqtt server are stored in a netrc format. I found this very conveniant to use, because
- its supported by python and its also easy to get the data in shell scripts
- credentials are stored in a single location and not spread over all different script places or even hardcoded in the scripts itself
Just create a `~/.netrc` (pi user) file with
```
machine fritz.box login <yourfritz user> password <your fritz pass>
machine mqtt login <your_mqtt user> password <your_mqtt pw>
```

2. ookla speed test

speedtest.sh (hourly timer on pi)
Simply calls the speedtest cli (json output) and pipes output to mosquitto_pub.
Again netrc is used for mqtt password, but now called from a bash script.
Data is sent with QOS 1 to store data when my TIG stack is unavailable (laptop sleeps)

3. mosquitto

plain service on pi
- currently out of scope -

4. TIG

based on
https://github.com/bcremer/docker-telegraf-influx-grafana-stack.git

so docker-compose is used to start the services.

Telegraf fetches data from topics, does very minimal conversion and puts data in influx DB.
Influx is still v.1.8
Grafana displays dashboards.

I added changed telegraf configs / grafana dashboards here, where it differs from the base project.

telegraf is using two instances, one for local statsd dashboard on one for mqtt input, there are also distinct databases for these usecases

