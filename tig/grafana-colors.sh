cat grafana/dashboards/bandwidth.json | jq '.panels[]|select(.title|match("^Download")).fieldConfig.overrides|sort_by(.matcher.option)'
