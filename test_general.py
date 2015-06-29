from unittest import TestCase
import config
from config import General
__author__ = 'faebser'


class TestGeneral():
    general = config.general

    def test_proplist(self):
        for prop in self.general.property_tuple:
            assert prop.name in self.general