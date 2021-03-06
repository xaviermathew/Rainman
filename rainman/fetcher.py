import hashlib
import re

from sqlalchemy.util import classproperty


class BaseFetcher(object):
    DELIMITER = '~'
    ESCAPE_CHAR = '\\'
    BULK_CHUNK_SIZE = 10
    PREFIX = None
    IS_ABSTRACT = False

    @classproperty
    def NAME(cls):
        return cls.__name__

    @classmethod
    def get_key(cls, *key_parts):
        return cls.DELIMITER.join([str(s).replace(cls.DELIMITER, cls.ESCAPE_CHAR + cls.DELIMITER) for s in key_parts])

    @classmethod
    def split_key(cls, key):
        parts = re.split(r'(?<!\\)%s' % cls.DELIMITER, key)
        parts = [p.replace(cls.ESCAPE_CHAR + cls.DELIMITER, cls.DELIMITER) for p in parts]
        return parts

    @classmethod
    def get_hash(cls, prefix, key):
        s = '%s-%s' % (prefix, key)
        return hashlib.sha256(s.encode('utf-8')).hexdigest()

    @classmethod
    def is_valid(cls, cache_obj):
        return True

    @classmethod
    def to_python(cls, d):
        return d

    @classmethod
    def fetch(cls, *key_parts):
        raise NotImplementedError

    @classmethod
    def fetch_bulk(cls, list_of_key_parts):
        for key_parts in list_of_key_parts:
            yield key_parts, cls.fetch(*key_parts)

    @classmethod
    def _get(cls, *key_parts):
        from rainman.models import Cache
        from rainman.utils import create_session

        key = cls.get_key(*key_parts)
        key_hash = cls.get_hash(cls.PREFIX, key)
        session = create_session()
        instance = session.query(Cache).filter_by(key_hash=key_hash).one_or_none()
        if instance:
            if cls.is_valid(instance):
                return instance.value
            else:
                return instance.fetch(cls, session)
        else:
            instance = Cache(prefix=cls.PREFIX, key=key, key_hash=key_hash)
            return instance.fetch(cls, session)

    @classmethod
    def get(cls, *key_parts):
        value = cls._get(*key_parts)
        return cls.to_python(value)

    @classmethod
    def paginated_get(cls, *key_parts):
        next_page = -1
        curr_key_parts = key_parts
        while next_page == -1 or next_page is not None:
            if next_page != -1 and next_page is not None:
                curr_key_parts = list(key_parts) + [next_page]
            curr_value, next_page = cls._get(*curr_key_parts)
            yield from cls.to_python(curr_value)
