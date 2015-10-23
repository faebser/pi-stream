import socket
import fcntl
import struct
from status import status
from test_manager import TestClass, TestStatus, add_test


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


class IpPrivateTest(TestClass):
    name = u'Private IP'

    def run_test(self):
        try:
            ip = get_ip_address('eth0')
        except IOError:
            return TestStatus.Attention, \
                   u'The main network connection is not available. Please check the cable', \
                   u"No network\nconnection"
        if '192.168' in ip:
            return TestStatus.Good, 'My IP-Address in private range: {})'.format(ip), u''
        else:
            return TestStatus.Attention, \
                   'My IP-Address should start with 192.168. But it is {}'.format(ip), \
                   u"Target = 192.168\n{}".format(ip)
