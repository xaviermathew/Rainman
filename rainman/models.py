import datetime
import os

from sqlalchemy import Column, JSON, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Cache(Base):
    __tablename__ = 'rainman_cache'

    prefix = Column(String, max_length=50, nullable=False, index=True)
    key = Column(Text, nullable=False, index=True)
    key_hash = Column(String, max_length=100, primary_key=True)
    value = Column(JSON, nullable=True)
    created_on = Column(DateTime, nullable=False, default=datetime.datetime.now)
    modified_on = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def fetch(self, fetcher_class, session=None):
        from rainman.utils import create_session

        key_parts = fetcher_class.split_key(self.key)
        self.value = fetcher_class.fetch(*key_parts)

        if session is None:
            session = create_session()
        session.add(self)
        session.commit()
        return self.value


engine = create_engine(os.environ['RAINMAN_DATABASE_URL'], echo=True)
Base.metadata.create_all(engine)
