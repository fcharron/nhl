#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import nhl



class TestNhl(unittest.TestCase):

    def test_reader_summary(self):
        nhl_reader = nhl.reader("20122013", view='summary')
        for player in nhl_reader:
            self.assertTrue(player)

    
    def test_reader_bios(self):
        nhl_reader = nhl.reader("20122013", view='bios')
        for player in nhl_reader:
            self.assertTrue(player)



if __name__ == '__main__': 
    unittest.main()