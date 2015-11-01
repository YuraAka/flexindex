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
        price=None,
        price_old=None,
        discount=None
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
        self.price, self.price_old, self.discount = Offer.__calc_prices(price, price_old, discount)

        Autogen.use('ts', self.ts)
        Autogen.use('cmagic', self.cmagic)

    @staticmethod
    def __calc_prices(price, old, discount):
        default_price = 100
        if not price and not old and discount: return default_price, default_price*discount/100, discount
        if not price and old and not discount: return default_price, old, (old - default_price) / old
        if not price and old and discount: return old-old*discount/100, old, discount
        if price and not old and not discount: return price, price, 0
        if price and not old and discount: return price, price + price * discount/100, discount
        if price and old and not discount: return price, old, (old - price) / old
        raise RuntimeError('Cannot use price_old and discount simultaneously. Use on of it.')

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

        index.write('price={0}\n'.format(self.price))
        index.write('price_old={0}\n'.format(self.price_old))
        index.write('discount={0}\n'.format(self.discount))
        index.write('\n')

        for p in self.glparams:
            glsc.write('{hid}:{param}:{value}\n'.format(hid=self.hid, param=p.id, value=str(p.value)))


