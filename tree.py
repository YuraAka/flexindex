__author__ = 'Yura'

class Tree(object):
    def __init__(self, root):
        self._index = dict()
        self._root = root
        self._index[self._get_id(self._root)] = self._root

    def add_children(self, children):
        candidates = [(k, v) for (k, v) in children.iteritems()]
        self.__make_relations(self._root, children)
        while candidates:
            node, children = candidates.pop(0)
            self.__make_relations(node, children)
            if self._get_id(node) in self._index:
                raise RuntimeError('Node with id {0} already exists'.format(self._get_id(node)))
            self._index[self._get_id(node)] = node
            candidates.extend([(k, v) for (k, v) in children.iteritems()])

    def __make_relations(self, parent, children):
        for (k, _) in children.iteritems():
            self._link_parent(parent, k)
