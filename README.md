# Rainman
 Python implementation of Apache Spark

## Usage
### RDD
```python
>>> # define a DB
>>> import os
>>> os.environ['RAINMAN_DATABASE_URL'] = 'sqlite:///rainman.db'
>>>
>>> # define fetchers
>>> # make sure these are imported before importing rainman.models.Cache
>>> # to be able to discover subclasses of BaseFetcher
>>> from rainman.fetcher import BaseFetcher
>>> class GoogleFetcher(BaseFetcher):
...     PREFIX = 'goog'
...     @classmethod
...     def fetch(cls, *key_parts):
...         print('querying google')
...         # do something and return a JSON encodeable obj
...         return []
...
>>>
>>> class BingFetcher(BaseFetcher):
...     PREFIX = 'bing'
...     @classmethod
...     def fetch(cls, *key_parts):
...         print('querying bing')
...         # do something and return a JSON encodeable obj
...         return []
...
>>>
>>> # query the cache
>>> from rainman.models import Cache
>>> print(Cache.get('goog', 'rain man dustin hoffman'))
querying google
[]
>>> print(Cache.get('goog', 'rain man dustin hoffman'))
[]
```
