#!/bin/sh
D=$(dirname $0)

docker run --rm -t -v $D/:/opt/python -v ~/.netrc:/home/python/.netrc:ro tig-rtl433 python netgear.py
