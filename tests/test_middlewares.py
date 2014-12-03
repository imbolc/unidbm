import os
import sys
import copy
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import unidbm.middlewares.json
import unidbm.middlewares.pickle
import unidbm.middlewares.string
import unidbm.middlewares.compress


if sys.version_info < (3, ):
    bytes = str

DATA = [1, 2, {'foo': None}, True]


def test():
    for name, data in [('pickle', DATA), ('json', DATA), ('string', u'ыыы'),
                       ('compress', u'foo'.encode('utf-8'))]:
        dumper = getattr(unidbm.middlewares, name).Middleware()

        dump = dumper.dump(copy.deepcopy(data))
        assert isinstance(dump, bytes)

        loaded = dumper.load(dump)
        assert loaded == data


if __name__ == '__main__':
    test()
