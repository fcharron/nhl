#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import nhl


class PlayerTestsMixin(object):
    def setUp(self):
        self.player = nhl.Player(self.NHL_ID).load()
 
    def test_regular_stats(self):
         self.assertTrue(self.player.regular_stats())

    def test_playoff_stats(self):
         self.assertTrue(self.player.playoff_stats())



class TestOldPlayer(PlayerTestsMixin, unittest.TestCase):
    NHL_ID = 8458520

class TestOldGoalie(PlayerTestsMixin, unittest.TestCase):
    NHL_ID = 8448853

class TestCrawford(PlayerTestsMixin, unittest.TestCase):
    NHL_ID = 8470645

class TestKessel(PlayerTestsMixin, unittest.TestCase):
    NHL_ID = 8473548




if __name__ == '__main__': 
    unittest.main()