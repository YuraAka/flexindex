from autogen import Autogen
__author__ = 'Yura'

class Model(object):
    def __init__(self, hyper, title=None):
        self.hyper = hyper
        self.title = title if title else 'HYPER-{0}'.format(self.hyper)

    def __eq__(self, other):
        return self.hyper == other

    def save(self, out):
        out.write('hyper:G={0}\n'.format(self.hyper))
        out.write('hyper_model_id:S={0}\n'.format(self.hyper))
        out.write('_Title={0}\n'.format(self.title))

class ModelStat(object):
    def __init__(self, hyper, regions=None, price_min=100, price_max=150, price_med=200):
        self.hyper = hyper
        self.price_min = price_min
        self.price_max = price_max
        self.price_med = price_med
        self.regions = regions

    def save(self, out):
        self.regions = self.regions if self.regions else [Autogen.default_region]

        out.write('hyper={0}\n'.format(self.hyper))
        out.write('price-min={0}\n'.format(self.price_min))
        out.write('price-max={0}\n'.format(self.price_max))
        out.write('price-med={0}\n'.format(self.price_med))

