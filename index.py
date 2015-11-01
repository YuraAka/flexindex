import sys
from hypercategory import HyperCategoryTree
from region import RegionTree
from navcategory import NavForest
from raw import RawDataFallback

__author__ = 'Yura'

"""
RULE OF THUMB: ALL AUTOGENERATION IS IN SAVE-METHODS, NOT EARLIER
"""
class FlexibleIndex(object):
    @property
    def categories(self):
        return self.__categories

    @property
    def navforest(self):
        return self.__navforest

    @property
    def navtree_default(self):
        return self.__navforest.default_tree

    @property
    def bids(self):
        return self.__bids

    @property
    def regions(self):
        return self.__regions

    @categories.setter
    def categories(self, value):
        self.categories.add_children(value)

    @navforest.setter
    def navforest(self, value):
        self.__navforest.add_trees(value)

    @navtree_default.setter
    def navtree_default(self, value):
        self.__navforest.add_branch_to_default_tree(value)

    @bids.setter
    def bids(self, value):
        self.__bids.data = value

    @regions.setter
    def regions(self, value):
        self.__regions.add_children(value)

    def __init__(self):
        self.__categories = HyperCategoryTree()
        self.__navforest = NavForest()
        self.__bids = RawDataFallback()
        self.__regions = RegionTree()

        self.offers = []
        self.models = []
        self.model_stats = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, *_):
        if exc_type is not None:
            return False
        self.commit()
        return self

    def commit(self):
        print('part/offers.txt:')
        for offer in self.offers:
            offer.save(
                index=sys.stdout,
                glsc=sys.stdout,
                categories=self.categories,
                models=self.models
            )

        print('\npart/models.txt')
        for model in self.models:
            model.save(out=sys.stdout)

        print('\nCategories.xml:')
        self.categories.save(self.navforest, out=sys.stdout)

        print('\nnavigation_info.xml')
        self.navforest.save(out=sys.stdout)

        print('\nbids.txt')
        self.bids.save(out=sys.stdout)

        print('\nModelRegionalStats')
        for stat in self.model_stats:
            stat.save(out=sys.stdout)
