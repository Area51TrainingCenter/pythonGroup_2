from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UnicodeText, DateTime, Integer, String

from datetime import datetime


Entity = declarative_base()


class Entry(Entity):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    uri = Column(String(255), nullable=False)
    body = Column(UnicodeText, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///wiki.db', echo=True)
    Entity.metadata.create_all(engine)
