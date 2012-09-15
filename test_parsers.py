import unittest
from parsers import *

class TestGenericParser(unittest.TestCase):
    def setUp(self):
        self.parser = GenericParser()

    def test_is_all(self):
        self.assertTrue(self.parser.is_all('*'))
        self.assertFalse(self.parser.is_all('*3'))
        self.assertFalse(self.parser.is_all('3'))

    def test_is_single(self):
        self.assertTrue(self.parser.is_single('8'))
        self.assertTrue(self.parser.is_single('18'))
        self.assertFalse(self.parser.is_single('*'))
        self.assertFalse(self.parser.is_single('3-7'))

    def test_is_range(self):
        self.assertTrue(self.parser.is_range('5-7'))
        self.assertTrue(self.parser.is_range('5-7-9'))
        self.assertFalse(self.parser.is_range('5-'))

    def test_is_skip(self):
        self.assertTrue(self.parser.is_skip('3-9/2'))
        self.assertFalse(self.parser.is_skip('3-9'))
