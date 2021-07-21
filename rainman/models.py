import hashlib
import os

from sqlalchemy import Column, JSON, String, Text, DateTime, create_engine
from sqlalchemy_utils import ChoiceType
from sqlalchemy.ext.declarative import declarative_base

from rainman.utils import discover_fetchers

Base = declarative_base()


class Cache(Base):
    __tablename__ = 'rainman_cache'

    FETCHERS = discover_fetchers()
    FETCHER_MAP = {klass.PREFIX: klass for klass in FETCHERS}
    PREFIX_CHOICES = {klass.PREFIX: klass.NAME for klass in FETCHERS}

    prefix = Column(ChoiceType(PREFIX_CHOICES, impl=String(50)))

    key = Column(Text, nullable=False, index=True)
    key_hash = Column(String, max_length=100, primary_key=True)
    value = Column(JSON, nullable=True)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)

    @classmethod
    def get_fetcher_class(cls, prefix):
        return cls.FETCHER_MAP[prefix]

    @property
    def fetcher_class(self):
        return self.get_fetcher_class(self.prefix)

    @classmethod
    def get_hash(cls, prefix, key):
        s = '%s-%s' % (prefix, key)
        return hashlib.sha256(s).hexdigest()

    def fetch(self):
        fetcher_class = self.fetcher_class
        key_parts = fetcher_class.split_key(self.key)
        value = fetcher_class.fetch(*key_parts)
        self.value = fetcher_class.to_python(value)

    @property
    def data(self):
        return self.fetcher_class.from_python(self.value)

    @classmethod
    def get(cls, prefix, *key_parts):
        from rainman.utils import create_session

        fetcher_class = cls.get_fetcher_class(prefix)
        key = fetcher_class.get_key(key_parts)
        key_hash = cls.get_hash(prefix, key)
        session = create_session()
        instance = session.query(cls).filter_by(key_hash=key_hash).one_or_none()
        if instance:
            if fetcher_class.is_valid(instance):
                return instance.data
            else:
                instance.fetch()
                session.add(instance)
                session.commit()
                return instance.data
        else:
            instance = cls(prefix=prefix, key=key, key_hash=key_hash)
            instance.fetch()
            session.add(instance)
            session.commit()
            return instance.data


engine = create_engine(os.environ['RAINMAN_DATABASE_URL'], echo=True)
Base.metadata.create_all(engine)
