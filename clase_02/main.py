import feedparser

import os
import json
import urllib2
import uuid


FEEDS = None
CURRENT_FEED_INDEX = None


def load_feeds():
    global FEEDS
    if FEEDS is None:
        _feeds = []
        for item in os.listdir('cache'):
            item = os.path.join('cache', item)
            if os.path.isfile(item) and item.endswith('.json'):
                try:
                    _file = open(item, 'r+')
                except IOError:
                    pass
                else:
                    data = json.loads(_file.read())
                    _file.close()
                    _feeds.append(data)
        FEEDS = _feeds


def show_menu():
    items = (
        ('Ver lista de feeds', view_feeds),
        ('Leer feed', view_feed),
        ('Agregar feed', add_feed),
        ('Salir', quit)
    )

    print '\nMENU\n===========\n\n'
    for index, item in enumerate(items):
        print '%s) %s' % (index + 1, item[0])

    while True:
        try:
            opcion = int(raw_input('\nIngrese opcion: ')) - 1
        except ValueError:
            print 'Opcion incorrecta'
        else:
            if opcion < 0 or opcion >= len(items):
                print 'Opcion incorrecta'
            else:
                items[opcion][1]()
                break


def view_feeds():
    print '\nFEEDS\n===========\n\n'
    for index, item in enumerate(FEEDS):
        print '%s) %s' % (index + 1, item.get('title'))
    print '\n'

    show_menu()


def view_feed():
    global CURRENT_FEED_INDEX
    while True:
        try:
            opcion = int(
                raw_input('\nSeleccione el feed que desea leer: ')) - 1
        except ValueError:
            print 'Opcion incorrecta'
        else:
            try:
                print '\n\nNoticias\n=============\n\n'
                for index, item in enumerate(FEEDS[opcion]['items']):
                    print '%s%s) %s' % (
                        '* ' if item['unread'] is True else '  ',
                        index + 1,
                        item['title']
                    )
                CURRENT_FEED_INDEX = opcion
            except IndexError:
                print 'Opcion incorrecta'
            else:
                break
    show_inner_menu()


def show_inner_menu():
    items = (
        ('Leer noticia', read_news),
        ('Regresar', show_menu)
    )

    print '\nMENU\n===========\n\n'
    for index, item in enumerate(items):
        print '%s) %s' % (index + 1, item[0])

    while True:
        try:
            opcion = int(raw_input('\nIngrese opcion: ')) - 1
        except ValueError:
            print 'Opcion incorrecta'
        else:
            if opcion < 0 or opcion >= len(items):
                print 'Opcion incorrecta'
            else:
                items[opcion][1]()
                break


def read_news():
    while True:
        try:
            opcion = int(raw_input('Ingrese opcion de noticia: ')) - 1
        except ValueError:
            print 'Opcion incorrecta'
        else:
            try:
                print '\n\n%s\n\n%s' % (
                    FEEDS[CURRENT_FEED_INDEX]['items'][opcion]['title'],
                    FEEDS[CURRENT_FEED_INDEX]['items'][opcion]['description']
                )
            except IndexError:
                'Opcion incorrecta'
            else:
                FEEDS[CURRENT_FEED_INDEX]['items'][opcion].update({
                    'unread': False
                })
                _file = os.path.join(
                    'cache',
                    FEEDS[CURRENT_FEED_INDEX]['filename']
                )
                _file = open(_file, 'w')
                _file.write(json.dumps(FEEDS[CURRENT_FEED_INDEX]))
                _file.close()
                show_inner_menu()
                break


def add_feed():
    while True:
        url = raw_input('\nIngrese url del feed: ')
        try:
            data = urllib2.urlopen(url)
        except urllib2.URLError:
            print 'URL incorrecta'
        else:
            data = feedparser.parse(data.read())
            _feed = {'title': data['feed']['title']}
            _items = []
            _name = str(uuid.uuid4())
            for item in data['items']:
                _items.append({
                    'title': item['title'],
                    'description': item['description'],
                    'unread': True
                })
            _feed.update({'items': _items, 'filename': _name})
            _file = os.path.join('cache', '%s.json' % _name)
            _file = open(_file, 'w+')
            _file.write(json.dumps(_feed))
            _file.close()
            break
    print '\n\nAgregado satisfactoriamente!\n\n'
    load_feeds()
    show_menu()


def quit():
    print 'Gracias!'


if __name__ == '__main__':
    load_feeds()
    show_menu()
