import zlib


class Middleware(object):
    def __init__(self, compress_level=9):
        self.compress_level = compress_level

    def load(self, data):
        return zlib.decompress(data)

    def dump(self, data):
        return zlib.compress(data, self.compress_level)
