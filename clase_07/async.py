from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop


client = AsyncHTTPClient()
def callback(res):
    print res.body[:100]

client.fetch('http://google.com', callback)
print 'Esto se ejecuto despues del fetch'
IOLoop.instance().start()
