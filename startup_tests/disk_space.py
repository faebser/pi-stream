__author__ = 'faebser'

import os
from test_manager import TestClass, TestStatus, add_test


class DiskSpaceTest(TestClass):
    name = u'Disk Space'

    def run_test(self):
        st = os.statvfs('/')  # root file system
        result = st.f_bavail * st.f_frsize/1024/1024
        minutes = result
        if result <= 999:
            return TestStatus.Attention, \
                   u'There are {} MB available. That is enough for {} minutes of MP3'.format(result, minutes), \
                   u"{} MB left\n{} min left".format(result, minutes)
        elif result <= 99:
            return TestStatus.Error, \
                   u'There are only {} MB available, that is just {} minutes of MP*. Please free up some space.'.format(result), \
                   u"Critical only\n{}MB {}min left".format(result, minutes)
        else:
            return TestStatus.Good, u'There are {} MB of free space available.'.format(result), u""
