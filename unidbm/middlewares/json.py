from __future__ import absolute_import
import json


class Middleware(object):
    def __init__(self, protocol=2):
        self.protocol = protocol

    def dump(self, data):
        return json.dumps(data).encode('utf-8')

    def load(self, data):
        return json.loads(data.decode('utf-8'))
