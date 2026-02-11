# Credits
https://github.com/bcremer/docker-telegraf-influx-grafana-stack.git

# Example Docker Compose project for Telegraf, InfluxDB and Grafana

This an example project to show the TIG (Telegraf, InfluxDB and Grafana) stack.

also checked https://github.com/nicolargo/docker-influxdb-grafana.git

## Start the stack with docker compose

```bash
$ docker compose stop service
$ docker compose up -d
```

## Services and Ports

### Grafana
- URL: http://localhost:3000
- User: admin
- Password: admin (initial)

If provisioning file is changed, the volume has to be deleted before restarting container.

### Telegraf
- Port: 8125 UDP (StatsD input)

docker run --rm telegraf:1.27-alpine -- config
docker compose exec telegraf_mqtt telegraf config check
both commands needs additional commands: env and volumes

split into 3 instances
- mqtt
- logs
- stats

### InfluxDB
- Port: 8086 (HTTP API)
- User: admin
- Password: admin
- Database: influx

changed to 30 days retention policy for hih resolution data and contionious query aggregation to permanent storage, switch is done automatically in DBs.

### Homeassistant
TBD

# Operations

Run the influx client: (there is a script)

```bash
$ docker compose exec influxdb influx -database sensors -execute 'SHOW DATABASES'
```

Run the influx interactive console:

```bash
$ docker compose exec influxdb influx -precision=rfc3339

Connected to http://localhost:8086 version 1.8.10
InfluxDB shell version: 1.8.10
>
```

[Import data from a file with -import](https://docs.influxdata.com/influxdb/v1.8/tools/shell/#import-data-from-a-file-with-import)

```bash
$ docker compose exec -w /imports influxdb influx -import -path=data.txt -precision=s
```

# get db:
curl -G http://localhost:8086/query?pretty=true --data-urlencode "q=SHOW DATABASES"
# create db:
curl -XPOST 'http://localhost:8086/query' --data-urlencode 'q=CREATE DATABASE mydb'"

# do selects, " have to be thrown away
docker compose exec influxdb influx -database sensors -precision 'rfc3339' -execute "SELECT MT681_Total_in from sensors WHERE (topic = 'strom') AND time >= now() - 48h"

## Run the PHP Example

The PHP example generates random example metrics. The random metrics are beeing sent via UDP to the telegraf agent using the StatsD protocol.

The telegraf agents aggregates the incoming data and perodically persists the data into the InfluxDB database.

Grafana connects to the InfluxDB database and is able to visualize the incoming data.

```bash
$ cd php-example
$ composer install
$ php example.php
Sending Random metrics. Use Ctrl+C to stop.
..........................^C
Runtime:	0.88382697105408 Seconds
Ops:		27
Ops/s:		30.548965899738
Killed by Ctrl+C
```


![Example Screenshot](./example.png?raw=true "Example Screenshot")


# Open Issues
## Influx
- still 1.x, since 2 has different query languauge, aon would change all DBs
- check authorisation

## Grafana
- storage location of annotations
## Telegraf
- cleanup config file re-use between instances: -> hardlinks
- migrate mqtt and stats together: issue is different influx output config (retention policies)
