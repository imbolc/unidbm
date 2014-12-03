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

Run tests
=========
    $ py.test
