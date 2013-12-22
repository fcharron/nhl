#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import nhl


class TestNhl(unittest.TestCase):

    def test0(self):
 		forsberg = nhl.Player(8458520).load()
 		self.assertTrue(forsberg.stats())

    def test1(self):
        crawford = nhl.Player(8470645).load()
        self.assertTrue(crawford.stats())

    def test2(self):
		kessel = nhl.Player(8473548).load()
		self.assertEqual(kessel.twitter(), "PKessel81")



if __name__ == '__main__': 
    unittest.main()