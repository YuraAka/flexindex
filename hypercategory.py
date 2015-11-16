from autogen import Autogen
from tree import Tree

__author__ = 'Yura'

class HyperCategory(object):
    def __init__(self, hid, name=None, children=[]):
        self.hid = hid
        self.name = name if name else 'HID-{0}'.format(hid)
        self.id = Autogen.get('tovar_id')
        self.parent = 0
        self.parent_hid = 0
        self.children = []

    def __str__(self):
        return '<category id="{id}" hid="{hid}" name="{name}" parent="{parent}"/>'.format(
            hid=self.hid,
            name=self.name,
            id=self.id,
            parent=self.parent
        )


class HyperCategoryTree(Tree):
    def __init__(self):
        Tree.__init__(self, root=HyperCategory(hid=Autogen.root_hid, name='All goods'))
        self.add_children({HyperCategory(hid=Autogen.default_hid, name='Default category'): {}})

    def load_file(self, name, root, default):
        # load raw file, restrict autogeneration
        pass

    def add_one(self, hid):
        if hid in self._index:
            return
        self.add_children({HyperCategory(hid=hid): {}})

    def get_parents(self, hid):
        while hid:
            yield hid
            hid = self._index[hid].parent_hid

    def save(self, navforest, out):
        out.write('<categories>\n')
        for v in self._index.itervalues():
            navforest.add_primary_in_all_trees(v.hid)
            out.write(str(v) + '\n')
        out.write('</categories>\n')

    @staticmethod
    def _link_parent(p,c):
        c.parent = p.id
        c.parent_hid = p.hid
        p.children.append(c)

    @staticmethod
    def _get_id(c):
        return c.hid

