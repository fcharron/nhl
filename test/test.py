#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from nhl import playerstats


class TestNhl(unittest.TestCase):

    def test_skater_summary(self):        
        for skater in playerstats.skater_summary_reader("20132014", "regular").run(42):
            self.assertTrue(skater)


    def test_skater_summary_fetch(self):
        skaters = playerstats.skater_summary_reader("20132014", "regular").fetch(7)
        self.assertTrue(len(skaters),7)


    def test_goalie_bios(self):        
        for goalie in playerstats.goalie_bios_reader("20132014", "regular").run(42):
            self.assertTrue(goalie)


    def test_goalie_bios_fetch(self):
        goalies = playerstats.goalie_bios_reader("20132014", "regular").fetch(7)
        self.assertTrue(len(goalies),7)


if __name__ == '__main__': 
    unittest.main()