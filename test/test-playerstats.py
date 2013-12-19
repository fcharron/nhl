#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from nhl import playerstats


TESTS = [
("20132014", "regular", "skaters", "summary"),
("20132014", "regular", "goalies", "summary"),
("20132014", "regular", "skaters", "bios"),
("20132014", "regular", "goalies", "bios"),
("19971998", "regular", "skaters", "summary"),
("19971998", "regular", "goalies", "summary"),
("19971998", "regular", "skaters", "bios"),
("19971998", "regular", "goalies", "bios")
]

ROWS_TO_GET = 3

class TestNhl(unittest.TestCase):

    def test_wrong_arg(self):
        reader = playerstats.reader("20122013", gametype="foo")
        self.assertFalse(reader)

    def test0(self):
        reader = playerstats.reader(*TESTS[0])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)

    def test1(self): 
        reader = playerstats.reader(*TESTS[1])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)

    def test2(self): 
        reader = playerstats.reader(*TESTS[2])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)

    def test4(self): 
        reader = playerstats.reader(*TESTS[3])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)

    def test5(self):
        reader = playerstats.reader(*TESTS[4])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)

    def test6(self): 
        reader = playerstats.reader(*TESTS[5])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)

    def test7(self): 
        reader = playerstats.reader(*TESTS[6])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)

    def test8(self): 
        reader = playerstats.reader(*TESTS[7])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)


if __name__ == '__main__': 
    unittest.main()