from __future__ import absolute_import
import semidbm


class Backend(object):
    def __init__(self, path):
        self.path = path
        self.open()

    def __getitem__(self, key):
        return self.db[key]

    def __setitem__(self, key, value):
        self.db[key] = value

    def __delitem__(self, key):
        del self.db[key]

    def __len__(self):
        count = 0
        for k in self.db:
            count += 1
        return count

    def __iter__(self):
        return (key for key in self.db)

    def open(self):
        self.db = semidbm.open(self.path, 'c')

    def close(self):
        self.db.close()
