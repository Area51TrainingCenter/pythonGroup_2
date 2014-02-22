from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Unicode, String, Integer

from datetime import datetime

Entity = declarative_base()


class Contacto(Entity):
    __tablename__ = 'contactos'

    id = Column(Integer, primary_key=True)
    nombre_completo = Column(Unicode(100), nullable=False)
    email = Column(String(200), nullable=False)
    creado = Column(DateTime, default=datetime.now)


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite://', echo=True)
    Entity.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()
    print 'Cantidad de contactos: %s' % session.query(Contacto).count()

    contacto1 = Contacto()
    contacto1.nombre_completo = 'area51 training center'
    contacto1.email = 'info@area51.pe'

    contacto2 = Contacto()
    contacto2.nombre_completo = 'nombre apellidos'
    contacto2.email = 'info@hotmail.com'

    session.add(contacto1)
    session.add(contacto2)
    try:
        session.commit()
    except:
        session.rollback()

    print 'Cantidad de contactos: %s' % session.query(Contacto).count()

    contacto1 = session.query(Contacto).filter(Contacto.email == 'info@area51.pe').first()
    print 'Email: %s' % contacto1.email

    contacto1.email = 'info@area51.com.pe'
    session.add(contacto1)
    try:
        session.commit()
    except:
        session.rollback()

    contacto_no_existente = session.query(Contacto.email).filter(Contacto.email.like('%microsoft%')).first()

    print contacto_no_existente

    contacto2 = session.query(Contacto).filter(Contacto.email == 'info@hotmail.com').all()
    session.delete(contacto2[0])
    try:
        session.commit()
    except:
        session.rollback()
    
    print 'Cantidad de contactos: %s' % session.query(Contacto).count()

    # session.query(Contacto).order_by(-Contacto.nombre_completo).all()
    # session.query(Contacto).group_by(Contacto.email).all()
    # from sqlalchemy import and_, or_
    # session.query(Contacto).filter(and_(Contacto.nombre_completo == 'xx', Contacto.email == 'ds')).all()
    # session.query(Contacto).filter(or_(Contacto.nombre_completo == 'xx', Contacto.email == 'ds')).all()
