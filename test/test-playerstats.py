#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import nhl



class TestNhl(unittest.TestCase):

    
    def test_many(self):
        stats = nhl.PlayerStats()
        stats.season("20132014")
        stats.report("summary")
        stats.position("skaters")
        stats.gametype("regular")

        self.assertEqual(len(stats.fetch(42)), 42)


    def test_onepage(self):
        stats = nhl.PlayerStats()
        stats.season("20122013")
        stats.report("summary")
        stats.position("goalies")
        stats.gametype("playoff")

        self.assertEqual(len(stats.fetch()), 23)


    def test_skaters_summary_playoff_1314(self):
        stats = nhl.PlayerStats()
        stats.season("20132014")
        stats.report("summary")
        stats.position("skaters")
        stats.gametype("playoff")

        self.assertEqual(len(stats.fetch()), 0)



    def test_skaters_summary_regular_9798(self):
        stats = nhl.PlayerStats()
        stats.season("19971998")
        stats.report("summary")
        stats.position("skaters")
        stats.gametype("regular")

        self.assertTrue(len(stats.fetch(42)))




if __name__ == '__main__': 
    unittest.main()