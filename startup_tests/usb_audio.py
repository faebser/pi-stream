__author__ = 'faebser'

from status import status
import subprocess
from test_manager import TestClass, TestStatus, add_test


class UsbAudioTest(TestClass):
    name = u'USB Audio'

    def run_test(self):
        audio_list = subprocess.Popen('aplay -l', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = audio_list.communicate()
        if error != '':
            return TestStatus.Error, u'There is problem related to the USB-Audio: {}'.format(error)
        for line in output.splitlines():
            if 'USB Audio' in line:
                return TestStatus.Good, u'I have a USB-Audio device connected'
        return TestStatus.Attention, u"I can't find a USB-Audio device. Please make sure that it is plugged in"
