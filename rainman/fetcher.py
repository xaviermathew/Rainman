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
        return cls.DELIMITER.join([s.replace(cls.DELIMITER, cls.ESCAPE_CHAR + cls.DELIMITER) for s in key_parts])

    @classmethod
    def split_key(cls, key):
        parts = re.split(r'(?<!\\)%s' % cls.DELIMITER, key)
        parts = [p.replace(cls.ESCAPE_CHAR + cls.DELIMITER, cls.DELIMITER) for p in parts]
        return parts

    @classmethod
    def is_valid(cls, cache_obj):
        return True

    @classmethod
    def fetch(cls, *key_parts):
        raise NotImplementedError

    @classmethod
    def fetch_bulk(cls, list_of_key_parts):
        for key_parts in list_of_key_parts:
            yield key_parts, cls.fetch(*key_parts)

    @classmethod
    def to_python(cls, d):
        return d

    @classmethod
    def from_python(cls, d):
        return d
