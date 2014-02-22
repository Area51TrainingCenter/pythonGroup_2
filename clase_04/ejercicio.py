from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, DateTime, create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime

Entity = declarative_base()


class Tweet(Entity):
	__tablename__ = 'tweets'

	id = Column(Integer, primary_key=True)
	usuario = Column(Unicode(100), nullable=False)
	body = Column(Unicode(100), nullable=False)
	created_at = Column(DateTime, default=datetime.now)


class Twitter():

    def __init__(self, engine):
        self._engine = engine

    def get_session(self):
    	return sessionmaker(bind=self._engine)()

    def get_tweets(self):
        session = self.get_session()
        tweets = session.query(Tweet).order_by(-Tweet.created_at).all()

        for tweet in tweets:
			print '%s\n%s - %s\n\n' % (tweet.body, tweet.usuario, tweet.created_at)

        session.close()

    def send_tweet(self, usuario, body):
        session = self.get_session()
        tweet = Tweet()
        tweet.usuario = usuario
        tweet.body = body
        session.add(tweet)

        try:
            session.commit()
        except:
            session.rollback()

    def display_menu(self):
        print '\n\nMENU\n=========\n\n'
        menu = (
            ('leer tweets', self.get_tweets),
            ('enviar tweet', self.prompt_for_tweet)
        )
        for index, option in enumerate(menu):
            print '%s) %s' % (index + 1, option[0])

        option = int(self._prompt_for_input('\nIngrese opcion: ', ('1', '2')))
        menu[option - 1][1]()
        self.display_menu()

    def _prompt_for_input(self, text, valid_options=None):
        while True:
            option = raw_input(text)
            if valid_options is None:
                return option
            elif option in valid_options:
                return option

    def prompt_for_tweet(self):
        usuario = self._prompt_for_input('\nUsuario: ')
        tweet = self._prompt_for_input('\nTweet: ')
        self.send_tweet(usuario, tweet)


if __name__ == '__main__':
    engine = create_engine('sqlite://', echo=True)
    Entity.metadata.create_all(engine)
	
    app = Twitter(engine)
    app.display_menu()
