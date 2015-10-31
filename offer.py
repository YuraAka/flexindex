from autogen import Autogen

__author__ = 'Yura'

class Offer(object):
    def __init__(self, **kwargs):
        self.hid = kwargs.get('hid')
        self.bid = kwargs.get('bid', 0)
        self.ts = kwargs.get('ts')
        self.title = kwargs.get('title', 'default-title')
        self.descr = kwargs.get('descr', 'default-descr')
        self.cmagic = kwargs.get('cmagic')
        self.glparams = kwargs.get('glparams', [])
        self.cpa = kwargs.get('cpa', False)
        self.hyper = kwargs.get('hyper', None)

        #manualgen register
        Autogen.use('ts', self.ts)
        Autogen.use('cmagic', self.cmagic)

    def save(self, indexfile, glscfile, categs):
        #autogen
        self.ts = self.ts if self.ts else Autogen.get('ts')
        self.cmagic = self.cmagic if self.cmagic else Autogen.get('cmagic')
        self.hid = self.hid if self.hid else Autogen.default_hid

        indexfile.write('ts:G={0}\n'.format(self.ts))
        indexfile.write('cmagic:G={0}\n'.format(self.cmagic))
        indexfile.write('_Title={0}\n'.format(self.title))
        indexfile.write('Descrutf8={0}\n'.format(self.descr))
        indexfile.write('hidd:G={0}\n'.format(self.hid))
        categs.autogen_by_hid(self.hid)
        for p in categs.get_parents(self.hid):
            indexfile.write('hyper_categ_id:S={0}\n'.format(p))

        if self.hyper:
            indexfile.write('hyper:G={0}\n'.format(self.hyper))
        indexfile.write('\n')

        for p in self.glparams:
            glscfile.write('{hid}:{param}:{value}\n'.format(hid=self.hid, param=p.id, value=str(p.value)))
