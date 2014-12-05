Dict-style key value wrapper around some embeded databases
==========================================================

Usage
=====

    >>> import unidbm
    >>> db = unidbm.open('sqlite', path=':memory:')

Set and get data:

    >>> db[u'foo'] = ['bar', {'baz': 1}]
    >>> db[u'foo']
    ['bar', {'baz': 1}]

Iterate:

    >>> [key for key in db] == [u'foo']
    True

Delete:

    >>> del db[u'foo']
    >>> len(db)
    0

Backends
--------
- sqlite
- kyoto cabinet
- semidbm

Custom backend
--------------
Backend works with bytes (str in py2) keys and values.
It should implement next methods:

- __init__(self, path, **any_options)
- def __getitem__(self, key):
- def __setitem__(self, key, value):
- def __len__(self):
- def __iter__(self):
- def close(self):