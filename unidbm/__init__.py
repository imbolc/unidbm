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
========
- sqlite
- kyoto cabinet
- semidbm


'''
from __future__ import absolute_import
try:
    from UserDict import DictMixin
except ImportError:
    from collections import MutableMapping as DictMixin

from . import backends
from . import middlewares
from .utils import name_to_object


__version__ = '0.0.1'


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
        value = self.backend[key]
        for middleware in self.get_middlewares:
            value = middleware.load(value)
        return value

    def __setitem__(self, key, value):
        for middleware in self.set_middlewares:
            value = middleware.dump(value)
        self.backend[key] = value

    def __delitem__(self, key):
        del self.backend[key]

    def __len__(self):
        return len(self.backend)

    def __iter__(self):
        return (k for k in self.backend)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


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
