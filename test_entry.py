from unittest import TestCase
from config import Entry
import pytest

__author__ = 'faebser'


class TestEntry:

    def test_setvalue(self):
        test = Entry('test')
        test.setvalue('a word')
        assert test.value == 'a word'

    def test_getvalue(self):
        test = Entry('test')
        test.value = 'another word'
        assert test.getvalue() == 'another word'

    def test_delvalue(self):
        test = Entry('test')
        test.value = 'delete me'
        test.delvalue()
        assert test.value is None