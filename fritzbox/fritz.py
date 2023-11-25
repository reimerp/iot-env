#!/usr/bin/env -S -i DBUS_SESSION_BUS_ADDRESS=${DBUS_SESSION_BUS_ADDRESS} python3
#

import sys
from hashlib import md5 as md5func
from urllib.request import urlopen
from xml.etree.ElementTree import parse

class Fritz:
    def __init__(self, host='fritz.box'):
        """Create a connection to the Fritz!Box with the given user and password."""

        if not (host.startswith('http://') and host.startswith('https://')):
            self.fritzurl = 'http://' + host
        if self.fritzurl.endswith('/'):
            self.fritzurl = self.fritzurl[0:-1]

        if 1==1:
            sys.path.insert(0, '../../../python')
            from pykeypass import KeePass
            keepass = KeePass('Fritzbox')
            keepass.parse()
            user = keepass.username
            password = keepass.password
        else:
            import netrc
            # uses ~/.netrc mechanism: "machine fritz.box login xxx password yyy"
            n = netrc.netrc()
            user = n.authenticators(host)[0]
            password = n.authenticators(host)[2]

        for attempt in range(2, 0, -1):
            try:
                self.sid = self.get_sid(user, password)
                break
            except PermissionError as e:
                if attempt == 1: raise e

    """
       Authenticate and get a Session ID
    """
    def get_sid(self, user, password):
        sid = '0000000000000000'
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

        if sid != '0000000000000000':
          return sid

        raise PermissionError('access denied')

# only debug
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='FritzBox Sid Helper')
    parser.add_argument('-H', '--host', default='fritz.box', help='FritzBox hostname')
    args = parser.parse_args()

    f = Fritz(args.host)
    print(f.sid)
