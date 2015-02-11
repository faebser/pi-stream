__author__ = 'faebser'

import socket
from status import status
from test_manager import TestClass, TestStatus, add_test


class IpPrivateTest(TestClass):
    name = u'Private IP'

    def run_test(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if '192.168' in ip:
            return TestStatus.Good, 'My IP-Address in private range: {})'.format(ip)
        else:
            return TestStatus.Attention, 'My IP-Address should start with 192.168. but it looks like this {}'.format(ip)
