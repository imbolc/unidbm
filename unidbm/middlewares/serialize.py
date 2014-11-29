import sys
import json
import pickle
import marshal


if sys.version_info < (3, ):
    pickle_loads = pickle.loads
    bytes = str
else:
    pickle_loads = lambda *a, **k: pickle.loads(*a, encoding='bytes', **k)


class SerializeMiddleware(object):
    def __init__(self, dumper='pickle', pickle_protocol=2):
        self.pickle_protocol = pickle_protocol
        assert dumper in ['pickle', 'json', 'marshal'], 'unknown dumper'
        if dumper == 'pickle':
            self.load = pickle_loads
            self.dump = lambda data: pickle.dumps(
                data, protocol=self.pickle_protocol)
        elif dumper == 'json':
            self.load = lambda data: json.loads(data.decode('utf-8'))
            self.dump = lambda data: json.dumps(data).encode('utf-8')
        elif dumper == 'marshal':
            self.load = marshal.loads
            self.dump = marshal.dumps
