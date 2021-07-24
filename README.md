# Rainman
 API cache backed by a DB

## Usage
### RDD
```python
>>> # Define a DB
>>> import os
>>> os.environ['RAINMAN_DATABASE_URL'] = 'sqlite:///rainman.db'
>>>
>>>
>>> # Either, use the decorator
>>> from rainman import cache
>>>
>>> @cache()
>>> def get_google_results(query):
...     print('querying google')
...     # do something and return a JSON encodeable obj
...     return []
>>>
>>>
>>> get_google_results('rain man dustin hoffman')
querying google
[]
>>> get_google_results('rain man dustin hoffman')
[]
>>>
>>>
>>> # Or for greater flexibility, subclass BaseFetcher
>>> from rainman.fetcher import BaseFetcher
>>> class GoogleFetcher(BaseFetcher):
...     PREFIX = 'goog'
...
...     @classmethod
...     def fetch(cls, *key_parts):
...         print('querying google')
...         # do something and return a JSON encodeable obj
...         return []
>>>
>>>
>>> GoogleFetcher.get('rain man dustin hoffman')
[]
```
