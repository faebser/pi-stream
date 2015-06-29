__author__ = 'faebser'

from enum import Enum
import bottle


class TestStatus(Enum):
    Error = 1
    Attention = 2
    Good = 3


class TestClass(object):
    name = None
    error_message = None

    def run_test(self):
        NotImplementedError("Class %s doesn't implement run_test()" % self.__class__.__name__)

test_manager = {}


def add_test(name, test):
    test_manager.update({name: test})

# tests
from internet_connectivity_tests import PingStreamServerTest, PingSwitchTest
add_test(u'ping_switch', PingSwitchTest())
add_test(u'ping_stream', PingStreamServerTest())

from disk_space import DiskSpaceTest
add_test(u'disk_space', DiskSpaceTest())

from ip_address import IpPrivateTest
add_test(u'ip_private', IpPrivateTest())

from usb_audio import UsbAudioTest
add_test(u'usb_audio', UsbAudioTest())

#from test_test import TestTest
#add_test(u'test', TestTest())


def run_all_tests():
    status = list()
    for name, test in test_manager.iteritems():
        result, message = test.run_test()
        status.append({
            "result": result,
            "message": message
        })
    return sorted(status, key=lambda item: item['result'].value)
