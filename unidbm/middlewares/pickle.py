from __future__ import absolute_import
import sys
import pickle

if sys.version_info < (3, ):
    pickle_loads = pickle.loads
else:
    pickle_loads = lambda *a, **k: pickle.loads(*a, encoding='bytes', **k)


class Middleware(object):
    def __init__(self, protocol=2):
        self.protocol = protocol

    def load(self, data):
        return pickle_loads(data)

    def dump(self, data):
        return pickle.dumps(data, protocol=self.protocol)
