#!/usr/bin/env python
import unittest
from index import IndexFrontend
from hypercategory import HyperCategory


class ClientBase(unittest.TestCase):
    report = None
    index = IndexFrontend
    @classmethod
    def setUpClass(cls):
        cls.index = IndexFrontend
        ClientBase.report = 'report'
        cls.prepare()
        pass

    @classmethod
    def prepare(cls):
        """
        need to be overriden
        """


class ClientTests(ClientBase):
    def test_one(self):
        self.index.categories = [
            HyperCategory(123, children=[
                HyperCategory(222, children=[
                    HyperCategory(333),
                    HyperCategory(444)
                ]),
                HyperCategory(345)
            ]
        )]

        print('test one')
        print(self.report)
        #self.report
        #self.showlog
        #self.qupdate

    def test_two(self):
        print('test two')
        print(self.report)


def clientmain():
    runner = unittest.TextTestRunner()
    test = ClientTests()
    runner.run(test)
    #loader = unittest.TestLoader()
    #tests = loader.loadTestsFromModule(sys.modules[__name__])


if __name__ == '__main__':
    #clientmain()
    unittest.main()
    '''
    runner = unittest.TextTestRunner()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromModule(sys.modules[__name__])
    with MyTestSuite() as suite:
        suite.addTests(tests)
        runner.run(suite)
    '''
