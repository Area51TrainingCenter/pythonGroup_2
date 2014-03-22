import tornado.web
import tornado.ioloop
import tornado.platform.twisted
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models

tornado.platform.twisted.install()

class Index(tornado.web.RequestHandler):

    def get(self):
        db = sessionmaker(bind=self.application._db_engine)()
        entries = db.query(models.Entry).order_by(-models.Entry.created_at).all()

        db.close()
        self.finish(self.application._template_env.get_template('index.html').render(
            entries=entries,
            handler=self
        ))


class Detalle(tornado.web.RequestHandler):

    def get(self, uri):
        db = sessionmaker(bind=self.application._db_engine)()
        res = db.query(models.Entry).filter(models.Entry.uri == uri).first()

        db.close()
        self.finish(self.application._template_env.get_template('detalle.html').render(
            entry=res,
            uri=uri,
            handler=self
        ))


class Edit(tornado.web.RequestHandler):

    def get(self, uri):
        db = sessionmaker(bind=self.application._db_engine)()
        entry = db.query(models.Entry).filter(models.Entry.uri == uri).first()

        db.close()
        self.finish(self.application._template_env.get_template('edit.html').render(
            entry=entry,
            handler=self
        ))

    def post(self, uri):
        db = sessionmaker(bind=self.application._db_engine)()
        entry = db.query(models.Entry).filter(models.Entry.uri == uri).first()

        if entry is None:
            entry = models.Entry()
            entry.uri = uri

        entry.body = self.get_argument('body')
        db.add(entry)
        try:
            db.commit()
        except:
            db.rollback()
        else:
            self.redirect(self.reverse_url('detalle', entry.uri))
        finally:
            db.close()

class MyApplication(tornado.web.Application):

    def __init__(self, handlers=None, default_host='', transforms=None,
                 wsgi=False, **settings):
        super(MyApplication, self).__init__(handlers, default_host, transforms,
                                           wsgi, **settings)
        self._template_env = Environment(
            loader=FileSystemLoader('templates'),
            auto_reload=True
        )
        self._db_engine = create_engine('sqlite:///wiki.db')

app = MyApplication([
    tornado.web.url('/', Index, name='index'),
    tornado.web.url(r'/detalle/(?P<uri>.*)/edit', Edit, name='edit'),
    tornado.web.url(r'/detalle/(?P<uri>.*)', Detalle, name='detalle'),
], static_path='static', static_url_prefix='/static/')


if __name__ == '__main__':
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
