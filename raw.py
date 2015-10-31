__author__ = 'Yura'

class RawDataFallback(object):
    def __init__(self):
        self.data = str()

    def save(self, out):
        out.write(self.data + '\n')
