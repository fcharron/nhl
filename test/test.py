#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import nhl



class TestNhl(unittest.TestCase):

    def test_reader_summary(self):
        nhl_reader = nhl.reader("20132014", report='summary')
        for player in nhl_reader:
            self.assertTrue(player)

    
    def test_reader_bios(self):
        nhl_reader = nhl.reader("20132014", report='bios')
        for player in nhl_reader:
            self.assertTrue(player)



if __name__ == '__main__': 
    unittest.main()