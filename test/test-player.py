#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import nhl


class TestNhl(unittest.TestCase):

    def test_old_player(self):
        forsberg = nhl.Player(8458520)
        self.assertTrue(forsberg.regular_stats())

    def test_old_goalie(self): 
        pelle = nhl.Player(8448853)
        self.assertTrue(pelle.regular_stats())        
    
    def test_crawford(self):
        crawford = nhl.Player(8470645)
        self.assertTrue(crawford.regular_stats())

    def test_kessel(self):
        kessel = nhl.Player(8473548)
        self.assertEqual(kessel.twitter(), "PKessel81")





if __name__ == '__main__': 
    unittest.main()