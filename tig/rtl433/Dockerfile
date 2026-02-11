FROM docker.io/alpine:3
#FROM docker.io/python:3-alpine

RUN apk add --update rtl_433 py3-pip py3-paho-mqtt py3-requests py3-snmp && rm -rf /var/cache/apk/*
# py3-paho-mqtt-pyc

RUN adduser -D python -u 990

#COPY rtl433/.netrc rtl433/rtl_pipe.py rtl433/basemqtt.py /home/python
COPY rtl433/requirements.txt /home/python

#COPY rtl433/.netrc /home/python
#RUN chown python /home/python/.netrc && chmod 600 /home/python/.netrc

USER python
RUN touch /home/python/.netrc

WORKDIR /opt/python

RUN pip install --break-system-packages -r ~/requirements.txt

CMD ["python3"]

#/root/.netrc
# rtl_pipe.py
