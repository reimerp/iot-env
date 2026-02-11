#!/bin/sh
docker run --rm -it -v ./:/opt/python -v ~/.netrc:/home/python/.netrc:ro tig-rtl433 python3 fritztemp2mqtt.py
docker run --rm -it -v ./:/opt/python -v ~/.netrc:/home/python/.netrc:ro tig-rtl433 python3 fritzdoc2mqtt.py
