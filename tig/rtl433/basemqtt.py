#!/usr/bin/env -S -i python3
# 150k Ram
import paho.mqtt.client as mqtt
from os import path
from inspect import getfile
import signal
from sys import stderr, stdout
from time import asctime, sleep
from datetime import datetime, timedelta, timezone
import netrc

class MqttBase(object):

    mqttc = None
    topics = None               # ein dict
    run = 70       # 70s, get at least one ping
    verbose = False

    def __init__(self):
        self.getcred('mqtt_rrd')

    def getcred(self, host):
        n = netrc.netrc()
        self.username = n.authenticators(host)[0]
        self.password = n.authenticators(host)[2]

    @staticmethod
    def getTime() -> str:
        return f'{datetime.now():%Y-%m-%dT%H:%M:%S}'

    @staticmethod
    def getUTCTime() -> str:
        return f'{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%SZ}'

    @staticmethod
    def getTs(isotimestring: str) -> datetime:
        return datetime.strptime(isotimestring, '%Y-%m-%dT%H:%M:%S')

    @staticmethod
    def checkTs(ts: datetime, hours=1) -> bool:
        delta = abs(ts - datetime.now())
        return delta > timedelta(hours=hours)

    @staticmethod
    def eprint(*args, **kwargs) -> None:
        print(*args, file=stderr, **kwargs)

    @staticmethod
    def status(status='Online') -> str:
        return f'{{"Time":"{datetime.now():%Y-%m-%dT%H:%M:%S}","Status":"{status}"}}'

    def name(self) -> str:
        '''final'''
        return str(path.splitext(path.basename(getfile(self.__class__)))[0])

    def warn(self, *objs) -> None:
        '''final'''
        print('WARN:', *objs, file=stderr)
        self.mqttc.publish(f'log/{self.name()}', payload=str(*objs))

    # 4:bad user/pass 5:not auth
    def on_connect(self, client, userdata, flags, rc):
        '''final'''
        if self.verbose: print(f'Connected: {client} {userdata} {flags} {rc}')
        if rc != mqtt.CONNACK_ACCEPTED:
            self.eprint(f'Error in connect: {mqtt.connack_string(rc)}')
            raise SystemExit(rc)
        self.mqttc.publish(f'lwt/{self.name()}', payload='Online', retain=True)
        # client.subscribe('$SYS/broker/messages/+')         // das geht nicht so
        if self.topics is not None:
            subscriptions = []
            for item in self.topics.keys(): subscriptions.append((item, 0))
            if self.verbose: print(f'Subscribed to {subscriptions}')
            client.subscribe(subscriptions)

    def addTopic(self, topic: dict) -> None:
        '''final adds topic to dict'''
        if self.topics == None: self.topics = {}
        self.topics.update({topic: None})

    def on_message(self, client, userdata, msg):
        '''convert to String, alway call with super'''
        msg.payload = msg.payload.decode('utf8')	# py3
        if self.verbose:
            print(f'{asctime()} on_msg: {msg.topic} {msg.payload}')

    def disconnect(self) -> None:
        '''final'''
        self.mqttc.loop_stop()
        self.mqttc.publish(f'lwt/{self.name()}', 'Offline', retain=True)
        self.mqttc.disconnect()

    def check_in(self) -> None:
        self.run -= 1

    def loop(self) -> None:
        '''final'''
        self.mqttc.loop_start()
        while self.run > 0:
            if self.verbose: stdout.write('Sleep\r')
            sleep(1)
            self.check_in()
            if self.verbose: stdout.write(f'Next  {self.run}...\r')
        self.disconnect()

    def connect_mqtt(self, logging=False):
        '''final'''
        self.mqttc = mqtt.Client()
        self.mqttc.username_pw_set(self.username, password=self.password)
        # tls_set(ca_certs, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
        self.mqttc.will_set(f'lwt/{self.name()}', payload='Offline', retain=True)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        if logging:
            import logging
            logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
            logger = logging.getLogger(__name__)
            self.mqttc.enable_logger(logger)
        self.mqttc.connect('mqtt', 1883, 60)
        signal.signal(signal.SIGINT, self._sigint_handler)
        self.loop()

    def _sigint_handler(self, signal, frame) -> None:
        '''final
          Catch SIGINT (Ctrl+C).'''
        if self.verbose: print('SIGINT received.')
        self.run = -1

if __name__ == '__main__':
    sensor = MqttBase()
    sensor.verbose = True
    #sensor.run = 100
    MqttBase.eprint('Go.')
    #sensor.addTopic('tasmota/+/tele/SENSOR')
    #sensor.addTopic('test/#')
    #sensor.addTopic('$SYS/broker/+/+')
    sensor.addTopic('$SYS/broker/messages/received')
    #warn(sensor.topics)
    sensor.connect_mqtt(logging=True)
    # this comes after signal
    sensor.warn(f'Running {sensor.run} rounds')
