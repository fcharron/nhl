#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from nhl import playerstats


TESTS = [
("20132014", "regular", "skaters", "summary"),
("20132014", "regular", "goalies", "summary"),
("20132014", "regular", "skaters", "bios"),
("20132014", "regular", "goalies", "bios"),
]

ROWS_TO_GET = 42

class TestNhl(unittest.TestCase):

    def test0(self):
        reader = playerstats.reader(*TESTS[0])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)

    def test1(self): 
        reader = playerstats.reader(*TESTS[1])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)

    def test2(self): 
        reader = playerstats.reader(*TESTS[2])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)

    def test3(self): 
        reader = playerstats.reader(*TESTS[3])
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)



if __name__ == '__main__': 
    unittest.main()