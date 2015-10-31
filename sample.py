from index import FlexibleIndex
from navcategory import NavTree, NavCategory
from offer import Offer
from hypercategory import HyperCategory
from region import Region

class GLParam(object):
    def __init__(self, id, value, type='numeric'):
        self.id = id
        self.value = value
        self.type = type


class RegionalModel(object):
    def __init__(self, hyper, regions, price_min=5, price_max=5):
        self.hyper = hyper
        self.price_min = price_min
        self.price_max = price_max
        self.regions = regions

def test1():
    with FlexibleIndex() as data:
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
    index = FlexibleIndex()

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

    index.regional_models = [
        RegionalModel(
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

    # if price is less than minimal for model by statistics -- error
    index.offers += [Offer(cpa=True, hyper=123, shop=111, price=123, hid=333) for _ in xrange(5)]

    index.commit()


if __name__ == '__main__':
    # test1()
    test2()
