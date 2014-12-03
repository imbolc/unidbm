class Middleware(object):
    def dump(self, data):
        return data.encode('utf-8')

    def load(self, data):
        return data.decode('utf-8')
