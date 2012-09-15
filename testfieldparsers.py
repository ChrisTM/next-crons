import unittest
from fieldparsers import *

class TestGenericParser(unittest.TestCase):
    def setUp(self):
        self.parser = GenericParser()


    # test is_ methods

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
        self.assertFalse(self.parser.is_range('5-7-9'))
        self.assertFalse(self.parser.is_range('5-'))

    def test_is_skip(self):
        self.assertTrue(self.parser.is_skip('3-9/2'))
        self.assertFalse(self.parser.is_skip('3-9'))


    # test parse_ methods

    def test_parse_all(self):
        self.assertRaises(SyntaxError, lambda: self.parser.parse_all('*'))

    def test_parse_single(self):
        exp = [5]
        obs = self.parser.parse_single('5')
        self.assertEqual(exp, obs)

    def test_parse_range(self):
        exp = [5,6,7,8]
        obs = self.parser.parse_range('5-8')
        self.assertEqual(exp, obs)

    def test_parse_skip(self):
        exp = [5,6,7,8]
        obs = self.parser.parse_skip('5-8/1')
        self.assertEqual(exp, obs)

        exp = [2, 4, 6, 8, 10]
        obs = self.parser.parse_skip('2-10/2')
        self.assertEqual(exp, obs)

        exp = [4, 7, 10, 13]
        obs = self.parser.parse_skip('4-14/3')
        self.assertEqual(exp, obs)

        obs_fn = lambda: self.parser.parse_skip('*/2');
        self.assertRaises(SyntaxError, obs_fn)


    # test parse method

    def test_parse(self):
        field = '5-8'
        exp = [5,6,7,8]
        self.assertEqual(exp, self.parser.parse(field))

        field = '3-10/3'
        exp = [3,6,9]
        self.assertEqual(exp, self.parser.parse(field))

        field = '12'
        exp = [12]
        self.assertEqual(exp, self.parser.parse(field))

        field = '6-8,2,3,4'
        exp = [2,3,4,6,7,8]
        self.assertEqual(exp, self.parser.parse(field))

        field = '9-12,6-7'
        exp = [6,7,9,10,11,12]
        self.assertEqual(exp, self.parser.parse(field))

class TestMonthsParser(unittest.TestCase):
    def setUp(self):
        self.parse = MonthsParser().parse

    def testAll(self):
        self.assertEqual(self.parse('*'), range(1,13))

    def testNames(self):
        self.assertEqual(self.parse('jan-may'), [1,2,3,4,5])
        self.assertEqual(self.parse('JAN-MAY'), [1,2,3,4,5])
        self.assertEqual(self.parse('feb-oct/2'), [2,4,6,8,10])

class TestDaysOfWeekParser(unittest.TestCase):
    def setUp(self):
        self.parse = DaysOfWeekParser().parse

    def testNames(self):
        self.assertEqual(self.parse('mon-wed'), [1,2,3])

class TestMonthsParser(unittest.TestCase):
    def setUp(self):
        self.parse = MonthsParser().parse

    def testNames(self):
        self.assertEqual(self.parse('feb-oct/2'), [2,4,6,8,10])
