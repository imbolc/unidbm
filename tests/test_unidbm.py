import os
import sys
import copy
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest

import unidbm


if sys.version_info < (3, ):
    bytes = str

DATA = [1, 2, {'foo': None}, True]


def test():
    db = unidbm.open('sqlite', path=':memory:')

    assert len(db) == 0

    # setitem
    db[u'foo'] = copy.deepcopy(DATA)
    db[u'bar'] = 'baz'

    # len
    assert len(db) == 2

    # getitem
    assert db[u'foo'] == DATA
    with pytest.raises(KeyError):
        db[u'not found']

    # iter
    assert set([key for key in db]) == set([u'foo', u'bar'])

    # get
    assert db.get(u'foo') == DATA
    assert db.get(u'not found') is None
    assert db.get(u'not found', 'default') == 'default'


if __name__ == '__main__':
    test()
