__author__ = 'faebser'

from status import status
from ping import do_one
import socket
from test_manager import TestClass, TestStatus, add_test


def real_ping(destination, timeout=2, count=4):
    """
    Use ICMP-Ping from ping.py

    :param string destination:
    :param int timeout:
    :param int count:
    """
    total_delay = 0
    for i in xrange(count):
        try:
            delay = do_one(destination, timeout)
        except socket.gaierror, e:
            return "Socket error: {}".format(e[1])
        except socket.error, (msg):
            return "Socket error: {}".format(msg)

        if delay is None:
            return "(timeout within {:.2f}sec.)".format(timeout)
        else:
            total_delay += delay
    return "success: {:.2f} msec average".format(total_delay / count * 1000)


class PingSwitchTest(TestClass):
    name = u'Ping Switch'
    timeout = 5

    def run_test(self):
        test = real_ping('switch.ch', self.timeout)
        if 'socket' in test or 'Socket' in test:
            return TestStatus.Error, u"I could not reach switch.ch. {}".format(test)
        elif 'timeout' in test:
            return TestStatus.Error, u"I could not reach switch.ch after {} seconds of trying. Please make sure that I'm connected to the internet".format(self.timeout)
        else:
            return TestStatus.Good, 'I pinged switch.ch'


class PingStreamServerTest(TestClass):
    name = u'Ping Streamserver'
    ip = None
    timeout = 5

    def __init__(self, ip='50.7.71.27'):
        self.ip = ip

    def run_test(self):
        if self.ip is not None:
            test = real_ping(self.ip, self.timeout)
            if 'socket' in test or 'Socket' in test:
                return TestStatus.Error, u"I could not reach the streaming server. Error: {}".format(test)
            elif 'timeout' in test:
                return TestStatus.Error, u"I could not reach streaming server after {} seconds of trying. Please make sure that I'm connected to the internet".format(self.timeout)
            else:
                return TestStatus.Good, 'I pinged {}'.format(self.ip)
