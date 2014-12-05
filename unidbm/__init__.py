'''
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


'''
from __future__ import absolute_import
import sys
try:
    from UserDict import DictMixin
except ImportError:
    from collections import MutableMapping as DictMixin

from . import backends
from . import middlewares
from .utils import name_to_object


__version__ = '0.1.1'


if sys.version_info < (3, ):
    bytes = str
else:
    unicode = str


class DBM(DictMixin):
    def __init__(self, backend, middlewares=None):
        middlewares = middlewares or []
        self.backend = backend
        self.set_middlewares = middlewares
        self.get_middlewares = self.set_middlewares[::-1]

    def __getitem__(self, key):
        key = self._encode_key(key)
        value = self.backend[key]
        for middleware in self.get_middlewares:
            value = middleware.load(value)
        return value

    def __setitem__(self, key, value):
        key = self._encode_key(key)
        for middleware in self.set_middlewares:
            value = middleware.dump(value)
        self.backend[key] = value

    def __delitem__(self, key):
        key = self._encode_key(key)
        del self.backend[key]

    def __len__(self):
        return len(self.backend)

    def __iter__(self):
        return (k.decode('utf-8') for k in self.backend)

    @staticmethod
    def _encode_key(key):
        if not isinstance(key, unicode):
            raise TypeError('unidbm key should be an unicode string')
        return key.encode('utf-8')


def open(backend, serialize=True, dumper='pickle',
         compress=False, compress_level=9,
         **backend_kwargs):
    mdls = []
    if serialize:
        mdls.append(get_dumper(dumper)())
    if compress:
        middleware = name_to_object(middlewares.NAMES['compress'])
        mdls.append(middleware(compress_level=compress_level))
    backend = get_backend(backend)(**backend_kwargs)
    return DBM(backend, middlewares=mdls)


def get_dumper(name):
    name = middlewares.NAMES.get(name, name)
    try:
        return name_to_object(name)
    except ImportError:
        raise ImportError('Unknown dumper: {}'.format(name))


def get_backend(name):
    name = backends.NAMES.get(name, name)
    try:
        return name_to_object(name)
    except ImportError:
        raise ImportError('Unknown backend: {}'.format(name))
