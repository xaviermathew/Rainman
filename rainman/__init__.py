def cache(**kwargs):
    def inner(fetch_func):
        from rainman.fetcher import BaseFetcher

        attrs = {
            'PREFIX': fetch_func.__name__,
            'fetch': staticmethod(fetch_func),
            '__doc__': fetch_func.__doc__,
            '__call__': lambda self, *key_parts: self.get(*key_parts),
            '__repr__': lambda x: '<Rainman:%s>' % fetch_func.__name__,
        }
        for k, v in kwargs.items():
            attrs[k] = classmethod(v)
        cls = type(fetch_func.__name__, (BaseFetcher,), attrs)
        return cls()
    return inner
