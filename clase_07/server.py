import tornado.web
import tornado.ioloop
import tornado.httpclient
import tornado.gen


class Main(tornado.web.RequestHandler):

    def termina(self):
        self.finish()

    def respuesta(self, res):
        self.finish(res.body)

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self):
        #self.write('Hola mundo!')
        #tornado.ioloop.IOLoop.instance().add_timeout(
        #    tornado.ioloop.IOLoop.instance().time() + 2,
        #    self.termina
        #)
        client = tornado.httpclient.AsyncHTTPClient()
        #client.fetch('http://google.com', self.respuesta)
        respuesta = yield client.fetch('http://google.com')
        self.finish(respuesta.body)

    def post(self):
        self.finish('Hola mundo (POST)')


app = tornado.web.Application([
    ('/', Main),
])


if __name__ == '__main__':
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
