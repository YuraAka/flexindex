import hashlib

__author__ = 'Yura'

def md5cvt(value):
    m = hashlib.md5()
    m.update(str(value))
    return m.hexdigest()

def intcvt(value):
    return value

class Autogen(object):
    @staticmethod
    def __generate(name):
        base = Autogen.__bases.get(name, 1)
        used = Autogen.__used.get(name, [])
        cvt = Autogen.__cvts.get(name, intcvt)
        result = cvt(base)
        while base in used:
            base += 1
            result = cvt(base)

        Autogen.__bases[name] = base
        return result

    @staticmethod
    def use(name, value):
        if not value:
            return
        if name not in Autogen.__used:
            Autogen.__used[name] = []
        Autogen.__used[name].append(value)

    @staticmethod
    def get(name):
        result = Autogen.__generate(name)
        Autogen.use(name, result)
        return result

    __bases = dict()    # field name => autogeneration base
    __used = dict()     # filed name => all values which have been generated
    __cvts = dict()     # int to custom-type convertor

    __cvts['cmagic'] = md5cvt

    default_hid=2406
    root_hid = 90604
    default_navtree = 12345
    root_rid = 1111
