from autogen import Autogen
import xml.etree.ElementTree as Et
from xml.dom import minidom
from tree import Tree

__author__ = 'Yura'


class NavCategory(object):
    def __init__(self, nid, hid=0, link=None, primary=False):
        self.nid = nid
        self.hid = hid
        self.link = link if link else {}
        self.primary = primary
        self.tree = 0
        self.children = []

    def add_children(self, *nodes):
        self.children += list(nodes)
        return self

    def as_node(self, tree):
        return Et.SubElement(tree, 'node', attrib={
            'id': str(self.nid),
            'primary': str(self.primary),
            'hid': str(self.hid)
        })

    def as_link(self, links):
        if not self.link:
            return

        link = Et.SubElement(links, 'link')
        url = Et.SubElement(link, 'url')
        params = Et.SubElement(url, 'params')
        for (k, v) in self.link.iteritems():
            param = Et.SubElement(params, 'param')
            Et.SubElement(param, 'name').text = str(k)
            Et.SubElement(param, 'value').text = str(v)

class NavTree(Tree):
    def _link_parent(self, parent, child):
        if child.primary:
            if child.hid in self.__primaries:
                raise RuntimeError('Hyper category {0} already has primary nid'.format(child.hid))
            self.__primaries.add(child.hid)
        parent.children.append(child)

    @staticmethod
    def _get_id(c):
        return c.nid

    def __init__(self, id=0, **kwargs):
        Tree.__init__(self, root=NavCategory(**kwargs))
        self.__id = id
        self.__primaries = set()
        if self._root.primary:
            self.__primaries.add(self._root.hid)

    def save(self, navigation, links):
        categs = [self._root]
        root = Et.SubElement(navigation, 'navigation_tree', attrib={'id': str(self.__id)})
        xmls = [self._root.as_node(root)]
        while categs:
            topc = categs.pop()
            topx = xmls.pop()
            for child in topc.children:
                categs.append(child)
                xmls.append(child.as_node(topx))
                child.as_link(links)

    def add_primary(self, hid):
        if hid not in self.__primaries:
            self.__primaries.add(hid)
            self._root.add_children(NavCategory(Autogen.get('nid'), hid=hid, primary=True))

'''
class NavTree(object):
    def __init__(self, id=0, **kwargs):
        self.id = id
        self.root = NavCategory(**kwargs)
        self.__primaries = set()
        if self.root.primary:
            self.__primaries.add(self.root.hid)

    def add_children(self, children, index):
        self.root.children += [k for k in children.iterkeys()]
        candidates = [(k, v) for (k, v) in children.iteritems()]
        while candidates:
            cat, children = candidates.pop(0)
            index[cat.nid] = cat
            cat.children = [k for k in children.iterkeys()]
            candidates += [(k, v) for (k, v) in children.iteritems()]
            if cat.primary:
                if cat.hid in self.__primaries:
                    raise RuntimeError('Hyper category {0} already has primary nid'.format(cat.hid))
                self.__primaries.add(cat.hid)

    def save(self, navigation, links):
        categs = [self.root]
        root = Et.SubElement(navigation, 'navigation_tree', attrib={'id': str(self.id)})
        xmls = [self.root.as_node(root)]
        while categs:
            topc = categs.pop()
            topx = xmls.pop()
            for child in topc.children:
                categs.append(child)
                xmls.append(child.as_node(topx))
                child.as_link(links)

    def add_primary(self, hid):
        if hid not in self.__primaries:
            self.__primaries.add(hid)
            self.root.add_children(NavCategory(Autogen.get('nid'), hid=hid, primary=True))
'''

class NavForest(object):
    def __init__(self):
        self.__trees = []
        self.default_tree = NavTree(
            id=Autogen.default_navtree,
            nid=Autogen.get('nid'),
            hid=Autogen.root_hid,
            primary=True
        )
        self.__add_tree(self.default_tree, {})

    def __add_tree(self, tree, branches):
        self.__trees.append(tree)
        tree.add_children(branches)

    def add_trees(self, trees):
        for (t, b) in trees.iteritems():
            self.__add_tree(t, b)

    def add_branch_to_default_tree(self, branch):
        self.default_tree.add_children(branch)

    def save(self, out):
        root = Et.Element('navigation')
        links = Et.SubElement(root, 'links')
        for tree in self.__trees:
            tree.save(root, links)

        reparsed = minidom.parseString(Et.tostring(root))
        out.write(reparsed.toprettyxml(indent="  ") + '\n')

    def add_primary_in_all_trees(self, hid):
        for tree in self.__trees:
            tree.add_primary(hid)
