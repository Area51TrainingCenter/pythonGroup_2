import sqlite3


CONN = sqlite3.connect('test.db')

def setup():
    cursor = CONN.cursor()
    _tabla_contactos = 'create table contactos (' \
        'id integer primary key autoincrement, ' \
        'nombres varchar(200) not null, ' \
        'apellidos varchar(200) not null, ' \
        'email varchar(200) not null, ' \
        'fecha_nacimiento date not null' \
        ')'
    cursor.execute(_tabla_contactos)
    CONN.commit()


def main():
    cursor = CONN.cursor()
    cursor.execute('select count(*) from sqlite_master where type = "table"')
    data = cursor.fetchone()
    if data[0] == 0:
        setup()


def add_user(nombres, apellidos, email, fecha_nacimiento):
    cursor = CONN.cursor()
    cursor.executemany('insert into contactos (nombres, apellidos, email, fecha_nacimiento) values (?, ?, ?, ?)', [(nombres, apellidos, email, fecha_nacimiento), (nombres, apellidos, email, fecha_nacimiento)])
    CONN.commit()
    cursor.execute('select * from contactos')
    print cursor.fetchall()


def remove_user(id):
    cursor = CONN.cursor()
    cursor.execute('delete from contactos where id = ?', str(id))
    CONN.commit()
    cursor.execute('select * from contactos')
    print cursor.fetchall()


def update_user(id, nombres, apellidos, email, fecha_nacimiento):
    cursor = CONN.cursor()
    cursor.execute('update contactos set nombres = ?, apellidos = ?, email = ?, fecha_nacimiento = ? where id = ?', (nombres, apellidos, email, fecha_nacimiento, str(id)))
    CONN.commit()
    cursor.execute('select * from contactos')
    print cursor.fetchall()

if __name__ == '__main__':
    main()
    add_user('area51', 'training center', 'info@area51.pe', '2014-02-15')
    #update_user(1, 'area512', 'training center2', 'info@area51.pe2', '2014-12-31')
    #remove_user(2)
    CONN.close()
