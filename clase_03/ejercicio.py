import sqlite3
from datetime import datetime


CONN = sqlite3.connect('ejercicio.db')


def setup():
    c = CONN.cursor()
    _tabla_usuarios = 'create table if not exists usuarios (' \
        'id integer primary key autoincrement, ' \
        'nombre varchar(100) not null, ' \
        'fecha_nacimiento date not null, ' \
        'edad integer not null)'
    c.execute(_tabla_usuarios)
    CONN.commit()


def _prompt(label):
    while True:
        data = raw_input(label)
        if len(data) > 0:
            return data


def agregar_usuario(nombre, fecha_nacimiento):
    c = CONN.cursor()
    c.execute('insert into usuarios (nombre, fecha_nacimiento, edad) values (?, ?, ?)', (
        nombre,
        fecha_nacimiento.strftime('%Y-%m-%d'),
        calculo_edad(fecha_nacimiento)
    ))
    CONN.commit()

def calculo_edad(fecha_nacimiento):
    edad = datetime.now() - fecha_nacimiento
    return int(edad.days / 365)

def get_avg_users():
    c = CONN.cursor()
    c.execute('select avg(edad) from usuarios')
    try:
        return int(c.fetchone()[0])
    except IndexError:
	return 0

def get_max_age():
    c = CONN.cursor()
    c.execute('select max(edad) from usuarios')
    try:
        return c.fetchone()[0]
    except IndexError:
        return 0

def get_min_age():
    c = CONN.cursor()
    c.execute('select min(edad) from usuarios')
    try:
        return c.fetchone()[0]
    except IndexError:
        return 0


if __name__ == '__main__':
    setup()
    nombre = _prompt('Cual es tu nombre: ')
    fecha_nacimiento = _prompt('Fecha nacimiento: ')
    while True:
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
        except ValueError:
            print 'Fecha incorrecta (YYYY-MM-DD)'
            fecha_nacimiento = _prompt('Fecha nacimieto: ')
        else:
            break
    agregar_usuario(nombre, fecha_nacimiento)	
    print 'Tienes %s anios' % calculo_edad(fecha_nacimiento)
    print 'En promedio los usuarios tienen %s anios' % get_avg_users()
    print 'La edad maxima es %s anios' % get_max_age()
    print 'La edad minima es %s anios' % get_min_age()
