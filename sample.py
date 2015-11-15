from index import IndexFrontend
from navcategory import NavTree, NavCategory
from offer import Offer
from hypercategory import HyperCategory
from region import Region
from model import Model, ModelStat
from glparam import GLParam
from report import Report
import unittest


class FlexTestCase(unittest.TestCase):
    def setUp(self):
        self.index = IndexFrontend()
        self.report = Report()

    def tearDown(self):
        self.report.stop()
        self.index.remove()

class MyTestCase(FlexTestCase):
    def setUp(self):

        pass

    def test_one(self):
        pass

def test1():
    with IndexFrontend() as data:
        data.navforest = {
            NavTree(id=123, nid=123): {
                NavCategory(nid=345): {}
            }
        }

        data.navtree_default = {
            NavCategory(nid=111): {},
            NavCategory(nid=222): {
                NavCategory(nid=333): {},
                NavCategory(nid=2, link={'how': 'aprice', 'hid': 123}): {},
                NavCategory(nid=3, hid=222, primary=True): {}
            }
        }

        data.offers = [
            Offer(title='mom', hid=12),
            Offer(
                hid=111,
                title='yura',
                glparams=[
                    GLParam(id=111, value=False, type='bool'),
                    GLParam(id=222, value=5, type='enum')
                ]
            )
        ]

        data.categories = {
            HyperCategory(hid=123, name='yura'): {
                HyperCategory(hid=456): {},
                HyperCategory(hid=555): {},
                HyperCategory(hid=222, name='leaf'): {
                    HyperCategory(hid=111): {}
                }
            }
        }


def test2():
    index = IndexFrontend()

    index.categories = {
        HyperCategory(hid=1): {
            HyperCategory(hid=2): {}
        }
    }

    index.navtree_default = {
        NavCategory(nid=33, hid=2, primary=True): {}
    }

    index.offers = [
        Offer(title='yura', ts=3)
    ]

    index.model_stats = [
        ModelStat(
            hyper=111,
            regions=[213, 225],
            price_min=234,
            price_max=123
        )
    ]

    index.regions = {
        Region(name='Moscow', rid=1) : {
            Region(name='Lubertsy', rid=2) : {}
        }
    }

    index.offers += [Offer(cpa=True, hyper=123, shop=111, price=123, hid=333) for _ in xrange(5)]
    index.commit()

def test3():
    index = IndexFrontend()

    index.model_stats = [
        ModelStat(hyper=1, price_min=100, price_max=300, price_med=150)
    ]

    index.offers = [
        Offer(cpa=True, hyper=1, price=100, discount=20),
        Offer(cpa=True, hyper=1, price_old=140, discount=20),
        Offer(cpa=True, hyper=1, price=200, discount=20),
        Offer(cpa=True, hyper=1, price=300, discount=20)
    ]

    index.commit()

if __name__ == '__main__':
    # test1()
    # test2()
    #test3()
    unittest.main()
