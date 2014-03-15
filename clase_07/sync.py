from tornado.httpclient import HTTPClient


client = HTTPClient()
response = client.fetch('http://google.com')
print response.body[:100]
print 'Esto se ejecuto despues del fetch'
client.close()
