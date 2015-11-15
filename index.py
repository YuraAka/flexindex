import sys
from hypercategory import HyperCategoryTree
from region import RegionTree
from navcategory import NavForest
from raw import RawDataFallback

__author__ = 'Yura'

CATEGORIES_FILE = 'report-data/categories.xml'
NAVIGATION_INFO_FILE = 'report-data/navigation_info.xml'
OFFER_INDEX_FILE = 'index/offers.txt'
MODEL_INDEX_FILE = 'index/models.txt'
BIDS_FILE = 'index/bids.txt'
MRS_FILE = 'report-data/model_regional_stats.txt'
GLSC_FILE = 'report-data/guru_light_regional_stats.txt'
YACA_FILE = 'report-data/YaCa.xml'

def fillStub(out):
    return out.write('I am a stub\n')


class IndexBackend(object):
    def __init__(self):
        self.__user_files = set()
        self.__required_files = {
            CATEGORIES_FILE: fillStub,
            NAVIGATION_INFO_FILE: fillStub,
            YACA_FILE: fillStub
        }

    def create_file(self, name):
        print('Creating {0}'.format(name))
        self.__user_files.add(name)
        return sys.stdout;

    def create_stubs(self):
        stub_files = set(k for k in self.__required_files.iterkeys()).difference(self.__user_files)
        for name in stub_files:
            stub = self.create_file(name)
            self.__required_files[name](stub)


class IndexFrontend(object):
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

    def remove(self):
        # remove index files
        pass

    def commit(self):
        # check /dev/shm accessible, if yes -- use it
        # otherwise use /tmp dir
        backend = IndexBackend()

        offer_file = backend.create_file(OFFER_INDEX_FILE)
        glsc_file = backend.create_file(GLSC_FILE)
        model_file = backend.create_file(MODEL_INDEX_FILE)
        categories_file = backend.create_file(CATEGORIES_FILE)
        navforest_file = backend.create_file(NAVIGATION_INFO_FILE)
        bids_file = backend.create_file(BIDS_FILE)
        mrs_file = backend.create_file(MRS_FILE)

        for offer in self.offers:
            offer.save(
                index=offer_file,
                glsc=glsc_file,
                categories=self.categories,
                models=self.models
            )


        for model in self.models:
            model.save(out=model_file)

        self.categories.save(self.navforest, out=categories_file)
        self.navforest.save(out=navforest_file)
        self.bids.save(out=bids_file)
        for stat in self.model_stats:
            stat.save(out=mrs_file)

        backend.create_stubs()
