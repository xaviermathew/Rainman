def _cache(fetch_func, get_func_name, **kwargs):
    from rainman.fetcher import BaseFetcher

    attrs = {
        'PREFIX': fetch_func.__name__,
        'fetch': staticmethod(fetch_func),
        '__doc__': fetch_func.__doc__,
        '__call__': lambda self, *key_parts: getattr(self, get_func_name)(*key_parts),
        '__repr__': lambda x: '<Rainman:%s>' % fetch_func.__name__,
    }
    for k, v in kwargs.items():
        if callable(v):
            attrs[k] = classmethod(v)
        else:
            attrs[k] = v
    cls = type(fetch_func.__name__, (BaseFetcher,), attrs)
    return cls()


def cache(**kwargs):
    def inner(fetch_func):
        return _cache(fetch_func, 'get', **kwargs)
    return inner


def paginated_cache(**kwargs):
    def inner(fetch_func):
        return _cache(fetch_func, 'paginated_get', **kwargs)
    return inner
