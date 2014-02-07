import feedparser


CURRENT_FEED = None


def add_feed():
    global CURRENT_FEED
    while True:
        url = raw_input('Ingrese la url del feed: ').strip()
        if len(url) != 0:
            CURRENT_FEED = feedparser.parse(url)
            display_news()
            break


def display_news():
    print '\n%s\n\n' % CURRENT_FEED['feed']['title']
    for index, item in enumerate(CURRENT_FEED['items']):
        print '%s) %s' % (index + 1, item['title'])
    show_menu()


def show_menu():
    items = (
        ('Leer Noticia', read_news),
        ('Cargar otro feed', add_feed),
        ('Salir', quit)
    )

    print '\n\nMENU\n========\n'
    for index, value in enumerate(items):
        print '%s) %s' % (index + 1, value[0])
    print '\n\n'

    while True:
        opcion = raw_input('Seleccione la opcion del menu: ')
        try:
            opcion = int(opcion) - 1
        except ValueError:
            print 'Opcion incorrecta'
        else:
            if opcion < 0 or opcion >= len(items):
                print 'Option incorrecta'
            else:
                items[opcion][1]()
                break


def read_news():
    while True:
        opcion = raw_input('Seleccione la noticia que desea leer: ')
        try:
            opcion = int(opcion) - 1
        except ValueError:
            print 'Opcion incorrecta'
        else:
            if opcion < 0 or opcion >= len(CURRENT_FEED['items']):
                print 'Opcion incorrecta'
            else:
                print '\n\n%s\n%s' % (
                    CURRENT_FEED['items'][opcion]['title'],
                    CURRENT_FEED['items'][opcion]['description']
                )
                show_menu()
                break


def quit():
    print 'Gracias'


if __name__ == '__main__':
    add_feed()
