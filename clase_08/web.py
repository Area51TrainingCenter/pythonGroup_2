from twisted.web import server, resource
from twisted.internet import reactor


class Main(resource.Resource):

    isLeaf = True

    def render_GET(self, request):
        request.setHeader('content-type', 'text/plain')
        return 'Hola Mundo!\n'


if __name__ == '__main__':
    reactor.listenTCP(8080, server.Site(Main()))
    reactor.run()
