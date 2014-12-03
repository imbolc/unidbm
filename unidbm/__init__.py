'''
Dict-style key value wrapper around some embeded databases
==========================================================

Usage
=====

    >>> import unidbm
    >>> db = unidbm.open('sqlite', path=':memory:')

Set and get data:

    >>> db['foo'] = ['bar', {'baz': 1}]
    >>> db['foo']
    ['bar', {'baz': 1}]

Iterate:

    >>> [str(key) for key in db]
    ['foo']

Delete:

    >>> del db['foo']
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


__version__ = '0.0.1'


if sys.version_info < (3, ):
    bytes = str
else:
    unicode = str


class DBM(DictMixin):
    def __init__(self, backend, *args, **kwargs):
        '''
        :param backend:         string or object of backend
        :param middlewrares:    (optional) list of middlewares
        :param **kwargs:        (optional) arguments that backend takes
        '''
        middlewares = kwargs.pop('middlewares', [])
        self.set_middlewares = [name_to_object(m) for m in middlewares]
        self.get_middlewares = reversed(self.set_middlewares)
        self.backend = name_to_object(backend)(**kwargs)

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

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    @staticmethod
    def _encode_key(key):
        if not isinstance(key, unicode):
            raise TypeError('unidbm key should be an unicode string')
        return key.encode('utf-8')


def open(backend, serialize=True, dumper='pickle',
         compress=False, compress_level=9,
         **backend_kwargs):
    mdl = backend_kwargs['middlewares'] = []
    if serialize:
        mdl.append(
            middlewares.SerializeMiddleware(dumper=dumper))
    if compress:
        mdl.append(
            middlewares.CompressMiddleware(compress_level=compress_level))
    backend = backends.NAMES.get(backend, backend)
    return DBM(backend, **backend_kwargs)
