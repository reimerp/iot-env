#!/bin/sh
docker run --rm -it -v ./:/opt/python -v ~/.netrc:/home/python/.netrc:ro tig-rtl433 python netgear.py
