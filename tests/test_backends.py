import os
import sys
import shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pytest import raises

import unidbm.backends.sqlite
import unidbm.backends.kyotocabinet
import unidbm.backends.semidbm


BACKENDS = [('sqlite', 'test.sqlite'),
            ('kyotocabinet', 'test.kch'),
            ('semidbm', u'test.semidbm')]


def test():
    for backend_name, path in BACKENDS:
        # print(backend_name)
        path = os.path.join(os.path.dirname(__file__), path)
        remove_db_files(path)
        db = getattr(unidbm.backends, backend_name).Backend(path)

        assert len(db) == 0

        # setitem
        k, v = encode('foo', 'bar')
        db[k] = v
        k, v = encode('baz', 'spam')
        db[k] = v

        # len
        assert len(db) == 2

        # getitem
        assert db[k] == v
        with raises(KeyError):
            db['not found']

        # iter
        assert set([x for x in db]) == set(encode('foo', 'baz'))

        # delete
        del db[k]
        assert len(db) == 1


def remove_db_files(path):
    if os.path.isfile(path):
        os.unlink(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


def encode(*seq):
    return [item.encode('utf-8') for item in seq]


if __name__ == '__main__':
    test()
