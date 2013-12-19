#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from nhl import player


PETER_FORSBERG = 8458520 #skater
COREY_CRAWFORD = 8470645 #goalie


ROWS_TO_GET = 7

class TestNhl(unittest.TestCase):

    def test0(self):
        reader = player.reader(PETER_FORSBERG)
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)

    def test1(self): 
        reader = player.reader(COREY_CRAWFORD)
        self.assertEqual(len(reader.fetch(ROWS_TO_GET)), ROWS_TO_GET)




if __name__ == '__main__': 
    unittest.main()