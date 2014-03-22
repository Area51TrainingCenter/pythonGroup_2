from twisted.internet import reactor, protocol
from twisted.protocols import basic

from time import time


class PubProtocol(basic.LineReceiver):

    def __init__(self, factory):
        self.factory = factory
        self.username = 'Anonymous-%s' % int(time())

    def broadcast(self, msg):
        for c in self.factory.clients:
            c.sendLine('<{}> {}'.format(
                self.username,
                msg
            ))

    def connectionMade(self):
        self.factory.clients.add(self)
        self.broadcast('Usuario conectado: %s' % self.username)

    def connectionLost(self, reason):
        self.broadcast('Usuario desconectado: %s' % self.username)
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        if line.startswith('/nick'):
            _ = self.username
            self.username = line.split(' ')[1]
            self.broadcast('%s ahora se llama %s' % (_, self.username))
        else:
            self.broadcast(line)


class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return PubProtocol(self)


if __name__ == '__main__':
    reactor.listenTCP(1234, PubFactory())
    reactor.run()
