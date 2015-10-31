from autogen import Autogen
from model import Model

__author__ = 'Yura'

class Offer(object):
    def __init__(
        self,
        hid=None,
        bid=0,
        ts=None,
        title='Apple iPhone',
        descr='Apple iPhone 128Gb with Retina display',
        cmagic=None,
        glparams=[],
        cpa=False,
        hyper=None,
        price=100,
        price_old=100
    ):
        self.hid = hid
        self.bid = bid
        self.ts = ts
        self.title = title
        self.descr = descr
        self.cmagic = cmagic
        self.glparams = glparams
        self.cpa = cpa
        self.hyper = hyper
        self.price = price
        self.price_old = price_old

        Autogen.use('ts', self.ts)
        Autogen.use('cmagic', self.cmagic)

    def save(self, index, glsc, categories, models):
        self.ts = self.ts if self.ts else Autogen.get('ts')
        self.cmagic = self.cmagic if self.cmagic else Autogen.get('cmagic')
        self.hid = self.hid if self.hid else Autogen.default_hid

        index.write('ts:G={0}\n'.format(self.ts))
        index.write('cmagic:G={0}\n'.format(self.cmagic))
        index.write('_Title={0}\n'.format(self.title))
        index.write('Descrutf8={0}\n'.format(self.descr))
        index.write('hidd:G={0}\n'.format(self.hid))

        categories.add_one(self.hid)
        for p in categories.get_parents(self.hid):
            index.write('hyper_categ_id:S={0}\n'.format(p))

        if self.hyper:
            if self.hyper not in models:
                models.append(Model(hyper=self.hyper))
            index.write('hyper:G={0}\n'.format(self.hyper))

        index.write('\n')

        for p in self.glparams:
            glsc.write('{hid}:{param}:{value}\n'.format(hid=self.hid, param=p.id, value=str(p.value)))

        #write prices
