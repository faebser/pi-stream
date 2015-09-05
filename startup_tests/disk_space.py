__author__ = 'faebser'

import os
from test_manager import TestClass, TestStatus, add_test


class DiskSpaceTest(TestClass):
    name = u'Disk Space'

    def run_test(self):
        st = os.statvfs('/')  # root file system
        result = st.f_bavail * st.f_frsize/1024/1024
        if result < 1000:
            return TestStatus.Attention, u'There are {} MB available. Please free up some space.'.format(result)
        elif result < 10:
            return TestStatus.Error, u'There are only {} MB available. Please free up some space.'.format(result)
        else:
            return TestStatus.Good, u'There are {} MB of free space available.'.format(result)
