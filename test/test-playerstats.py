#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from nhl import playerstats



class TestNhl(unittest.TestCase):

    def test_many(self):
        q = playerstats.Query()
        q.season("20132014")
        q.report("summary")
        q.position("skaters")
        q.gametype("regular")

        self.assertEqual(len(q.fetch(101)), 101)


    def test_onepage(self):
        q = playerstats.Query()
        q.season("20122013")
        q.report("summary")
        q.position("goalies")
        q.gametype("playoff")

        self.assertEqual(len(q.fetch()), 23)


    def test_goalies_regular(self):
        q = playerstats.Query()
        q.season("20132014")
        q.report("bios")
        q.position("goalies")
        q.gametype("regular")

        self.assertEqual(len(q.fetch()), 78)


    def test_empty(self):
        q = playerstats.Query()
        q.season("20132014")
        q.report("summary")
        q.position("skaters")
        q.gametype("playoff")

        self.assertEqual(len(q.fetch()), 0)



    def test_old(self):
        q = playerstats.Query()
        q.season("19971998")
        q.report("summary")
        q.position("skaters")
        q.gametype("regular")

        self.assertTrue(len(q.fetch(42)))



if __name__ == '__main__': 
    unittest.main()