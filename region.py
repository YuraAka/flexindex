from autogen import Autogen
from tree import Tree

__author__ = 'Yura'

class Region(object):
    def __init__(self, rid, name=None, type='city', parent=Autogen.root_rid):
        self.rid = rid
        self.name = name if name else 'RID-{0}'.format(rid)
        self.type = type
        self.parent = parent

class RegionTree(Tree):
    def __init__(self):
        Tree.__init__(self, Region(name='Russia', type='country', rid=Autogen.root_rid))

    @staticmethod
    def _get_id(r):
        return r.rid

    @staticmethod
    def _link_parent(p,c):
        c.parent = p

