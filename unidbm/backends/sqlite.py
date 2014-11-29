import sys
import sqlite3


if sys.version_info < (3, ):
    bytes = str


class Backend(object):
    def __init__(self, path, auto_commit=True):
        self.path = path
        self.auto_commit = auto_commit
        self.open()

    def __getitem__(self, key):
        self.cur.execute('SELECT * FROM kv WHERE id=?', (key, ))
        data = self.cur.fetchone()
        if not data:
            raise KeyError(key)
        return bytes(data[1])

    def __setitem__(self, key, value):
        q = 'REPLACE INTO kv (id, value) VALUES (?, ?)'
        self.cur.execute(q, (key, sqlite3.Binary(value)))
        if self.auto_commit:
            self.commit()

    def __delitem__(self, key):
        self.cur.execute('DELETE FROM kv WHERE id=?', (key, ))
        if self.auto_commit:
            self.commit()

    def __len__(self):
        self.cur.execute('SELECT count(*) FROM kv')
        return self.cur.fetchone()[0]

    def __iter__(self):
        self.cur.execute('SELECT id FROM kv')
        return (r[0] for r in self.cur.fetchall())

    def open(self):
        self.conn = sqlite3.connect(self.path)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS kv ('
                         '  id      VARCHAR PRIMARY KEY,'
                         '  value   BLOB );')
        self.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.execute("VACUUM")
        self.conn.close()
