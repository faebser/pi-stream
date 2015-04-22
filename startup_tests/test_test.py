__author__ = 'faebser'

from test_manager import TestClass, TestStatus, add_test


class TestTest(TestClass):
    name = u'TestTest'

    def run_test(self):
        return TestStatus.Error, u'this is a test'