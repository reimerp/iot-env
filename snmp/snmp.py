"""
Fetch two subtrees in parallel
++++++++++++++++++++++++++++++

Send a series of SNMP GETNEXT requests with the following options:

* with SNMPv1, community 'public'
* over IPv4/UDP
* to an Agent at 104.236.166.95:161
* for two OIDs in tuple form
* stop on end-of-mib condition for both OIDs

This script performs similar to the following Net-SNMP command:

| $ snmpwalk -v1 -c public -ObentU 104.236.166.95 1.3.6.1.2.1.1 1.3.6.1.4.1.1

snmpwalk -c public -v1 netgear .1.3.6.1.2.1.16.1.1.1.7

"""
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen
#from pysnmp.proto import rfc1902

class Snmp:
  # Initial OID prefix
  #initialOID = rfc1902.ObjectName('1.3.6.1.2.1.1')
  #initialOID = rfc1902.ObjectName('1.3.6.1.2.1.16.1.1.1.7')

  # Create SNMP engine instance
  def __init__(self):
    self.snmpEngine = engine.SnmpEngine()
    #
    # SNMPv1/2c setup
    #

    # SecurityName <-> CommunityName mapping
    config.addV1System(self.snmpEngine, 'my-area', 'public')

    # Specify security settings per SecurityName (SNMPv1 - 0, SNMPv2c - 1)
    config.addTargetParams(self.snmpEngine, 'my-creds', 'my-area', 'noAuthNoPriv', 0)

    #
    # Setup transport endpoint and bind it with security settings yielding
    # a target name
    #

    # UDP/IPv4
    config.addTransport(
        self.snmpEngine,
        udp.domainName,
        udp.UdpSocketTransport().openClientMode()
    )
    config.addTargetAddr(
        self.snmpEngine, 'my-router',
        udp.domainName, ('192.168.176.15', 161),
        'my-creds'
    )

  # Register a callback to be invoked at specified execution point of
  # SNMP Engine and passed local variables at code point's local scope
  # noinspection PyUnusedLocal,PyUnusedLocal
  def requestObserver(self, snmpEngine, execpoint, variables, cbCtx):
      print('Execution point: %s' % execpoint)
      print('* transportDomain: %s' % '.'.join([str(x) for x in variables['transportDomain']]))
      print('* transportAddress: %s' % '@'.join([str(x) for x in variables['transportAddress']]))
      print('* securityModel: %s' % variables['securityModel'])
      print('* securityName: %s' % variables['securityName'])
      print('* securityLevel: %s' % variables['securityLevel'])
      print('* contextEngineId: %s' % (variables['contextEngineId'] and variables['contextEngineId'].prettyPrint() or '<empty>',))
      print('* contextName: %s' % variables['contextName'].prettyPrint())
      print('* PDU: %s' % variables['pdu'].prettyPrint())

  # snmpEngine.observer.registerObserver(
  #     requestObserver,
  #     'rfc3412.sendPdu',
  #     'rfc3412.receiveMessage:response'
  # )
  def res(self, res: list) -> bool:
    self.result = {}
    for oid, val in res:
      # this works w/o imports, but there should be a global method
      if str(type(val)) == "<class 'pysnmp.proto.rfc1902.OctetString'>":
        out = val.prettyPrint()
      else:
        out = val.prettyIn(val)
      self.result[oid.prettyPrint()] = out
    return True

  def res2(self, res: list) -> bool:
    print('res', type(res), len(res))
    for oid, val in res:
        #if initialOID.isPrefixOf(oid):
            print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
        #else:
        #    return False
    return True

  # Error/response receiver
  # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
  def cbFun(self, snmpEngine, sendRequestHandle, errorIndication,
          errorStatus, errorIndex, varBinds, cbCtx):
    if errorIndication:
        print(errorIndication)
        return
    # SNMPv1 response may contain noSuchName error *and* SNMPv2c exception,
    # so we ignore noSuchName error here
    if errorStatus and errorStatus != 2:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[-1][int(errorIndex) - 1][0] or '?'))
        return  # stop on error

    if type(varBinds[0]) == tuple:
        self.res(varBinds)
        return False

    for varBindRow in varBinds:
        self.res(varBindRow)
#        for oid, val in varBindRow:
#            #if initialOID.isPrefixOf(oid):
#                print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
#            #else:
#            #    return False  # signal dispatcher to stop
    return True  # signal dispatcher to continue


# Prepare initial request to be sent
# cmdgen.NextCommandGenerator().sendVarBinds(
#     snmpEngine,
#     'my-router',
#     None, '',  # contextEngineId, contextName
#     #[((1, 3, 6, 1, 2, 1, 1), None), ((1, 3, 6, 1, 4, 1, 1), None)],
#     [
#         (initialOID, None),
#         #(('1.3.6.1.2.1.16.1.1.1.7'), None)
#     ],
#     cbFun
# )

  def req(self, query: list):
    # Prepare and send a get request
    cmdgen.GetCommandGenerator().sendVarBinds(
        self.snmpEngine,
        'my-router',
        None, '',  # contextEngineId, contextName
        # ein prefix geht hier nicht, aber ein Array
        query,
        self.cbFun
    )
    self.snmpEngine.transportDispatcher.runDispatcher()

  def __del__(self):
    # Error/response receiver
    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal

    # Run I/O dispatcher which would send pending queries and process responses

    self.snmpEngine.observer.unregisterObserver()

if __name__ == '__main__':
  s = Snmp()
  s.req(
      [
        (('1.3.6.1.2.1.16.1.1.1.7.1'), None),
        ('1.3.6.1.2.1.16.1.1.1.7.2', None),
        ('1.3.6.1.2.1.2.2.1.8.7', None),
        ((1, 3, 6, 1, 2, 1, 1, 1, 0), None)  # "GS108Tv2"
      ]
  )
  print(s.result)
