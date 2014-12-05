'''
aptitude install libkyotocabinet-dev
pip install kyotocabinet
'''
from __future__ import absolute_import
from kyotocabinet import DB


class Backend(object):
    def __init__(self, path):
        self.path = path
        self.open()

    def __getitem__(self, key):
        value = self.db[key]
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.db[key] = value

    def __delitem__(self, key):
        del self.db[key]

    def __len__(self):
        return len(self.db)

    def __iter__(self):
        return (key for key in self.db)

    def open(self):
        assert self.path.split('.')[-1] == 'kch', 'Excension should be "kch"'
        self.db = db = DB()
        assert db.open(self.path, DB.OWRITER | DB.OCREATE), db.error()

    def close(self):
        self.db.close()
