#!/usr/bin/env -S -i python3
#

from hashlib import md5 as md5func
from urllib.request import urlopen
from xml.etree.ElementTree import parse
import netrc

class Fritz:
    def __init__(self, host='fritz.box'):
        """Create a connection to the Fritz!Box with the given user and password."""

        if not (host.startswith('http://') and host.startswith('https://')):
            self.fritzurl = 'http://' + host
        if self.fritzurl.endswith('/'):
            self.fritzurl = self.fritzurl[0:-1]

        # uses ~/.netrc mechanism: "machine fritz.box login xxx password yyy"
        n = netrc.netrc()
        user = n.authenticators(host)[0]
        password = n.authenticators(host)[2]

        self.debug = False

        if not self.debug:    # TODO lässt sich nicht abschalten
            self.sid = self.get_sid(user, password)

    def get_sid(self, user, password):
        """Authenticate and get a Session ID"""
        with urlopen(self.fritzurl + '/login_sid.lua') as f:
            dom = parse(f)
            sid = dom.findtext('./SID')
            challenge = dom.findtext('./Challenge')

        if sid == '0000000000000000':
            md5 = md5func()
            md5.update(challenge.encode('utf-16le'))
            md5.update('-'.encode('utf-16le'))
            md5.update(password.encode('utf-16le'))
            response = challenge + '-' + md5.hexdigest()
            uri = self.fritzurl + '/login_sid.lua?username=' + user + '&response=' + response
            with urlopen(uri) as f:
                dom = parse(f)
                sid = dom.findtext('./SID')

        if sid == '0000000000000000':
            raise PermissionError('access denied')

        return sid

# only debug
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='FritzBox Sid Helper')
    parser.add_argument('-H', '--host', default='fritz.box', help='FritzBox hostname')
    parser.add_argument('--no-debug', action='store_true', help='Debug OFF')
    args = parser.parse_args()

    f = Fritz(args.host)
    f.debug = not args.no_debug
    print(f.sid)


