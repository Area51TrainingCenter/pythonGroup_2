from twisted.internet import protocol, reactor


class Echo(protocol.Protocol):
    def dataReceived(self, data):
        data = data.upper()
        data = '%s - %s' % (':)', data)
        self.transport.write(data)


class EchoFactory(protocol.Factory):

    def buildProtocol(self, addr):
        return Echo()


if __name__ == '__main__':
    reactor.listenTCP(1234, EchoFactory())
    reactor.run()
